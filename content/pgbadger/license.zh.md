---
title: "许可证与致谢"
linkTitle: "许可证"
weight: 110
description: "PostgreSQL License 条款、作者信息与内嵌第三方组件"
icon: fa-solid fa-scale-balanced
module: [PGBADGER]
categories: [参考]
aliases: [/docs/pgbadger/license/]
---

> 来源：固定源码提交中的上游 [`LICENSE`](https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/LICENSE)、`README.md` 与 `resources/LICENSE`。

pgBadger 是以 PostgreSQL License 发布的自由开源软件。只要保留版权与许可证声明，就可以免费使用、复制、修改与分发。

## PostgreSQL License 原文 {#postgresql-license}

Copyright (c) 2012-2026, Gilles Darold

Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and this paragraph and the following two paragraphs appear in all copies.

IN NO EVENT SHALL Darold BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF Darold HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Darold SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN “AS IS” BASIS, AND Darold HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

以上保留英文许可证原文，以免翻译改变法律含义。

## 作者与设计致谢 {#credits}

- pgBadger 是 Gilles Darold 的原创作品。
- pgBadger 标志由 Damien Cazeils 原创设计。
- pgBadger v4.x 的视觉设计来自 “Art is code” 公司。
- 项目网站由 Gilles Darold 制作。
- 其他贡献者在上游 ChangeLog 的对应版本中逐项致谢。

## 内嵌代码与报告资源 {#third-party-resources}

pgBadger 内嵌了修改版 `SQL::Beautify` Perl 模块，版权 © 2009 Jonas Kramer，以 Artistic License 2.0 发布。

生成报告使用的资源保留各自许可证：

| 组件 | 许可证 |
|---|---|
| bean.js、Bootstrap、jQuery、Underscore | MIT |
| jqPlot | 用户可选择 MIT 或 GPL-2.0 |
| Font Awesome 字体 | SIL Open Font License 1.1 |
| Font Awesome CSS | MIT |

本地源码快照保留了完整上游 `resources/LICENSE`。随站点打包的报告示例是历史生成物，也保留原有的内嵌声明与资源版本。

## 文档快照说明 {#documentation-snapshot}

本站把上游文档重新组织成 Hugo 页面，增加了导航与中文阅读辅助；命令帮助和 ChangeLog 等需要逐字核对的内容仍保留原文。pgBadger 源码文档继续遵循 PostgreSQL License，项目名称、作者信息与上游链接均予以保留。

