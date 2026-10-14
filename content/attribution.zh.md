---
title: "归属与授权"
linkTitle: "归属声明"
description: "本站每一页文档的来源、版权归属、授权协议，以及完整声明的保存位置。"
icon: fa-solid fa-copyright
page_width: wide
type: docs
sidebar_enabled: false
breadcrumb: false
translation_notice: false
outputs: [HTML, markdown]
---

doc.pg.center 转载并整理了六个上游项目撰写的文档。每一个文档页面的末尾都有一行署名，指明该页改编自哪份作品、
版权归属于谁、依据什么协议授权，并链接回本页对应的小节。

本页就是那份记录：说明每份材料从哪里、在什么时间、从哪个固定版本导入，依据什么协议，以及完整的上游声明保存在何处。

> [!NOTE]
> doc.pg.center 是独立的社区文档项目，与下列任何项目均无隶属关系，也未获得其背书，
> 不是它们的官方出版物，也不代表 PostgreSQL 全球开发组。

## 总览 {#summary}

| 组件 | 上游作品 | 固定版本 | 授权协议 | 保留的完整声明 |
|---|---|---|---|---|
| [Patroni](/zh/docs/patroni/) | [Patroni 文档](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [上游 `LICENSE`](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/zh/docs/pgbackrest/) | [pgBackRest 文档](https://pgbackrest.org/) | v2.59.3 | [MIT](https://opensource.org/license/mit) | [上游 `LICENSE`](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/zh/docs/pgbouncer/) | [PgBouncer 文档](https://www.pgbouncer.org/) | v1.26.0 | [ISC](https://opensource.org/license/isc-license-txt) | [上游 `COPYRIGHT`](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT) |
| [pgBadger](/zh/docs/pgbadger/) | [pgBadger 文档](https://pgbadger.darold.net/) | v13.2，提交 `a1ad95a` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/zh/docs/haproxy/) | [HAProxy 3.4 手册](https://docs.haproxy.org/3.4/) | 3.4.6-66 文档快照（稳定版 3.4.6），提交 `16acce1` | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/zh/docs/etcd/) | [etcd v3.7 文档](https://etcd.io/docs/v3.7/) | v3.7，提交 `d20f8ae` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [上游 `LICENSE`](https://github.com/etcd-io/website/blob/main/LICENSE) |

所有文档集都是**改编**而非镜像：标题、锚点、交叉链接、代码签名、页面分组与导航结构都为本站重新组织，
上游正文本身则予以保留。页末署名会明确说明这一点，并链接到本站中该页面的修改历史。

## Patroni {#patroni}

于 2026-08-15 从 [Patroni 文档](https://patroni.readthedocs.io/en/latest/) **v4.1.5** 导入。

Patroni 版权归 Compose、Zalando SE 与 Patroni Contributors 所有（Copyright (c) 2025），
依 [MIT 协议](https://opensource.org/license/mit)授权。
完整协议文本保存在[上游仓库](https://github.com/patroni/patroni/blob/master/LICENSE)。

## pgBackRest {#pgbackrest}

于 2026-08-15 从 [pgBackRest 文档站](https://pgbackrest.org/) 导入，
并于 2026-10-13 更新至 **v2.59.3**。

pgBackRest 版权归 The PostgreSQL Global Development Group 与 David Steele 所有（Copyright (c) 2015-2026），
依 [MIT 协议](https://opensource.org/license/mit)授权。
完整协议文本保存在[上游仓库](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE)。

## PgBouncer {#pgbouncer}

于 2026-08-15 从 [PgBouncer 文档站](https://www.pgbouncer.org/) **v1.25.2** 导入，
并于 2026-10-13 更新至 [**v1.26.0**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_0)。

PgBouncer 版权归 Marko Kreen 与 Skype Technologies OÜ 所有（Copyright (c) 2007-2009），
依 [ISC 协议](https://opensource.org/license/isc-license-txt)授权。
完整协议文本保存在[上游仓库](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT)。

## pgBadger {#pgbadger}

于 2026-08-15 从 <https://pgbadger.darold.net/> 以及
[`darold/pgbadger`](https://github.com/darold/pgbadger) 的提交
[`a1ad95a`](https://github.com/darold/pgbadger/commit/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae) 导入，
当时的最新发布版本为 v13.2。

pgBadger 版权归 Gilles Darold 所有（Copyright (c) 2012-2026），
依 [PostgreSQL 协议](https://opensource.org/license/postgresql)授权。
完整协议文本随离线示例一起发布于
[`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE)，
并保存在站点仓库的 `sources/pgbadger/upstream/LICENSE` 中。

> [!IMPORTANT]
> pgBadger 内置了一份修改过的 `SQL::Beautify` 模块，依 Artistic License 2.0 授权；
> 其生成的报告资源还包含 MIT、GPL-2.0 与 SIL Open Font License 1.1 组件。
> 完整的上游资源清单保存在
> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES)。
> 本站发布的[示例报告](/zh/docs/pgbadger/sample-reports/)是历史生成产物，保留其原始内嵌声明。

## HAProxy {#haproxy}

于 2026-08-16 从 HAProxy 3.4 官方维护仓库导入，并于 2026-10-13 更新至与官方英文手册一致的
`3.4.6-66` 维护分支文档快照，固定提交为
[`16acce1dac1d`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=16acce1dac1dcf1ad5d654204af3a5d45d0e3de8)。
最新稳定版另列为 `3.4.6`（标签 `v3.4.6`）；文档快照包含该稳定版发布之后的变更。
英文正文取自完整的 `doc/intro.txt`、`doc/configuration.txt` 与 `doc/management.txt` 三份手册，
分别为 1,695、33,216 与 5,305 行，共 40,216 行，重新组织为 34 个阅读页面。

HAProxy 版权归 Willy Tarreau 所有（Copyright 2000-2026），
依 [GNU 通用公共许可证第 2 版](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)授权。
HAProxy 自身的授权说明、OpenSSL 例外条款与完整 GPLv2 文本发布于
[`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) 与
[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0)。

> [!WARNING]
> HAProxy 派生页面**不**适用本站的 CC BY 4.0 协议，而适用 HAProxy 的 GPLv2 条款。

## etcd {#etcd}

从官方 etcd v3.7 文档导入，并于 2026-10-13 刷新到提交
[`d20f8ae346da`](https://github.com/etcd-io/website/commit/d20f8ae346da60ab6eb6f24f200753b328aa9fcc)。
固定的上游源码树为
[`content/en/docs/v3.7`](https://github.com/etcd-io/website/tree/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7)。

etcd 文档版权归 etcd Authors 所有（Copyright 2013-present）。其正文依
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授权，代码与代码示例依
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) 授权。
完整声明保存在[上游仓库](https://github.com/etcd-io/website/blob/main/LICENSE)。

## 本站 {#site}

为 doc.pg.center 原创撰写的内容依
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 发布；
若某页面适用上述上游协议，则以上游协议为准。


首页展示的 PostgreSQL 大象（Slonik）是 PostgreSQL 项目自身的标识，
取自 [postgresql.org 网站仓库](https://git.postgresql.org/gitweb/?p=pgweb.git)，
未经修改地依据 [PostgreSQL 商标与标识政策](https://www.postgresql.org/about/policies/trademarks/)
在此用于指代 PostgreSQL。该标识归 PostgreSQL Community Association of Canada 所有，
在此使用不代表其认可或背书。

本站由 [OINK](https://oink.pgsty.com/) v1.2.0 构建，该 Hugo 主题依
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) 授权，
其自身的上游与内置依赖声明随模块源码一并提供。

如果发现本页任何归属信息有误，欢迎通过[站点仓库](https://github.com/pgsty/doc.pg.center/issues)提出。
