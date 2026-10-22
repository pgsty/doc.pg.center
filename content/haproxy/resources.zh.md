---
title: "文档与社区"
linkTitle: "资源"
weight: 100
description: "上游手册、源码位置、支持渠道、联系方式与许可证"
icon: fa-solid fa-life-ring
module: [HAPROXY]
categories: [参考]
aliases:
  - /haproxy/intro/resources/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapters 1 and 5"
---

## 1. 可用文档 {#section-1}

HAProxy 的完整文档由以下文件组成。请先查阅与问题相关的文档，以节省时间并获得最准确的答案。如果这些文档已经给出答案，请勿再向邮件列表重复提问。

- [`intro.txt`](/zh/haproxy/load-balancing/)（本文档）：介绍负载均衡基础、HAProxy 产品及其能力边界、应避免的常见陷阱、部分操作系统特有限制、获取方式、演进过程、如何确认当前版本包含所有已知修复、升级方法，以及补充产品和替代方案。

- [`management.txt`](/zh/haproxy/prerequisites/)：介绍如何启动 HAProxy，如何在运行时及多节点环境中管理 HAProxy，以及如何执行无缝升级。

- [`configuration.txt`](/zh/haproxy/http-fundamentals/)：参考手册，详细说明所有配置关键字及其选项；需要更改配置时应查阅此文件。

- coding-style.txt：面向希望为项目贡献代码的开发者，说明代码应遵循的风格。规范并非十分严格，现有代码也没有全部遵循，但偏离过大的贡献会被拒绝。

- proxy-protocol.txt：HAProxy 及多个第三方产品所实现的 PROXY 协议事实标准规范。

- security.txt：说明如何报告安全问题，以及哪些问题属于或不属于安全漏洞。

- README：说明如何从源码构建 HAProxy。

## 5. 联系方式 {#section-5}

如需就任何问题联系开发者或社区成员，通常最合适的方式是向 <haproxy@formilux.org> 发送邮件，使用公开邮件列表。请注意，邮件列表及其归档均为公开内容，因此应避免披露敏感信息。列表中有上千名经验各异的用户，即使是最复杂的问题，通常也能较快获得高质量答复；社区同样欢迎各类建议。

不便使用电子邮件的用户可以访问 <http://discourse.haproxy.org/>。不过，该平台的读者较少，大多数问题由一个很小的团队处理。无论使用哪种渠道，都请耐心等候，并尊重利用业余时间帮助他人的社区成员。

如果认为发现了缺陷但尚不确定，最好先在邮件列表中报告。如果基本确认问题属于缺陷、所用版本已包含当前分支的最新更新，并且已有 GitHub 账户，可以直接前往 <https://github.com/haproxy/haproxy/> 创建议题，附上所有可提供的细节。议题内容同样完全公开，请勿提交日后可能后悔公开的信息。议题跟踪器以长讨论串形式呈现，因此不要直接粘贴数百行以上的长篇转储，应改用附件。

如果怀疑发现了安全问题，请参阅 doc/security.txt。该文件说明哪些问题属于或不属于 HAProxy 漏洞，以及如何通过私密渠道报告真正的安全问题。大多数疑似安全问题最终只是普通缺陷，更适合按上述方式报告。

## 本地完整手册 {#complete-local-manual-set}

- [入门指南](/zh/haproxy/load-balancing/)
- [配置手册](/zh/haproxy/http-fundamentals/)
- [管理指南](/zh/haproxy/prerequisites/)

## 版本来源 {#edition-provenance}

- **版本：** HAProxy 3.4.7-57，维护分支文档快照
- **最新稳定版：** HAProxy 3.4.7，标签 `v3.4.7`
- **源提交：** [`0faeaeda6cdb`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=0faeaeda6cdbb65c0e0cedb9a20489581bd7d4c3)
- **上游渲染文档：** [docs.haproxy.org/3.4/](https://docs.haproxy.org/3.4/)
- **本地许可副本：** [HAProxy 许可声明](/third_party/haproxy/LICENSE)与 [GPLv2](/third_party/haproxy/GPL-2.0)
