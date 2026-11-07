---
title: 归属与署名
linkTitle: 归属与署名
description: 本站 AgensGraph 内容的版权、许可、来源版本与改写边界。
type: docs
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/index.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
---

本站改编自 [SKAI Worldwide](https://skaiworldwide.com/)（原 Bitnine）发布的 **AgensGraph 2.18.6.1** 文档。产品行为、语法、示例、兼容性和版本边界以上游手册为准。

## 上游资料 {#upstream-material}

| 项目 | 记录 |
| --- | --- |
| 作品 | AgensGraph 2.18.6.1 文档 |
| 版权 | Copyright 2014–2026 SKAI Worldwide Co., Ltd. |
| 许可 | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| 来源 | [文档门户](https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/) |
| 源码 | [skaiworldwide-oss/agensgraph](https://github.com/skaiworldwide-oss/agensgraph) |
| 抓取时间 | 2026-11-06，Asia/Shanghai |

每个导入页面都通过 Oink 页尾署名显示原始来源、版权人、SPDX 许可和本页声明。标记为改编的页面会显示本地改写提示。英文手册来自上游提供的 Markdown 视图；章节索引和本站博客是本地编写，并链接回相关上游页面。

[机器可读的来源清单](/agensgraph/assets/source-manifest.json)记录了 90 个 Markdown 叶子页和 14 个章节索引源文件的来源 URL、字节数与 SHA-256 校验和。

## 本站做了哪些变化 {#change-boundary}

- Hugo / Oink 外壳、视觉设计、导航、搜索、页脚和首页数据是本站内容；
- 英文手册被转换为 Oink Markdown 路由，相对链接改写为本站路由，同时在 front matter 中保留上游来源；
- 本文档集发布英文及已有中文页面。中文草稿保留原有状态，正文未完成的导读页提供英文入口，不计入翻译覆盖率。代码、查询关键字、产品名和版本号保持原样；
- 博客是 PGSTY 根据指定上游页面整理的编辑文章，不代表 SKAI Worldwide 发布公告。

## 上游 NOTICE {#upstream-notice}

上游仓库的 NOTICE 原文如下：

```text
AgensGraph
Copyright 2014-2026 SKAI Worldwide Co., Ltd.

This product is licensed under the Apache License, Version 2.0.
See the LICENSE file.

This product is based on PostgreSQL.
Portions Copyright (c) 1996-2026, PostgreSQL Global Development Group
Portions Copyright (c) 1994, The Regents of the University of California
The PostgreSQL copyright notice, permission notice and disclaimers
are contained in the COPYRIGHT file.
```

上游原文保存在 `static/agensgraph/assets/licenses/`，可下载 [Apache 2.0 许可](/agensgraph/assets/licenses/agensgraph-Apache-2.0.txt)、[AgensGraph NOTICE](/agensgraph/assets/licenses/agensgraph-NOTICE.txt) 与 [PostgreSQL COPYRIGHT](/agensgraph/assets/licenses/PostgreSQL-COPYRIGHT.txt)。

## 纠错方式 {#corrections}

产品问题请查看上游 [issue tracker](https://github.com/skaiworldwide-oss/agensgraph/issues)；本站的路由、翻译或来源信息变更后，请更新源文件并重新运行 `make check`。
