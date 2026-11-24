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

PG.CENTER 转载并整理了PostgreSQL 运维工具和数据库内核项目的文档。每一个文档页面的末尾都有一行署名，指明该页改编自哪份作品、
版权归属于谁、依据什么协议授权，并链接回本页对应的小节。

本页就是那份记录：说明每份材料从哪里、在什么时间、从哪个固定版本导入，依据什么协议，以及完整的上游声明保存在何处。

> [!NOTE]
> PG.CENTER 是独立的社区文档项目，与下列任何项目均无隶属关系，也未获得其背书，
> 不是它们的官方出版物，也不代表 PostgreSQL 全球开发组。

## 总览 {#summary}

以下英文更新于 **2026 年 11 月 21 日**完成审阅；中文增量于 **2026 年 11 月 22 日**完成三轮自审。其他已审校语种已包含下列运维手册更新。`data/upstreams.yaml` 分别记录各语言的基线，页面中的来源链接指向对应修订。11 月 23 日的后续自审补齐了登记的 117 页中文欠项，另补全 4 个 pgEdge 章节入口。

| 组件 | 上游作品 | 固定版本 | 授权协议 | 保留的完整声明 |
|---|---|---|---|---|
| [Patroni](/zh/patroni/) | [Patroni 文档](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [上游 `LICENSE`](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/zh/pgbackrest/) | [pgBackRest 文档](https://pgbackrest.org/) | v2.60.1 | [MIT](https://opensource.org/license/mit) | [上游 `LICENSE`](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/zh/pgbouncer/) | [PgBouncer 文档](https://www.pgbouncer.org/) | v1.26.1 | [ISC](https://opensource.org/license/isc-license-txt) | [上游 `COPYRIGHT`](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT) |
| [pgBadger](/zh/pgbadger/) | [pgBadger 文档](https://pgbadger.darold.net/) | v13.3，提交 `0514893` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/zh/haproxy/) | [HAProxy 3.4 手册](https://docs.haproxy.org/3.4/) | v3.4.8 LTS | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/zh/etcd/) | [etcd v3.7 文档](https://etcd.io/docs/v3.7/) | v3.7 文档，提交 `e60635a`；软件版本 v3.7.4 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [上游 `LICENSE`](https://github.com/etcd-io/website/blob/main/LICENSE) |
| [Apache Cloudberry](/zh/cloudberry/) | [Apache Cloudberry 2.x 文档](https://cloudberry.apache.org/docs/) | 2.x 文档，提交 `e3a102d`；软件版本 2.2.0-incubating | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [上游 `LICENSE`](https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/LICENSE) 与 [`NOTICE`](https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/NOTICE) |
| [PXF](/cloudberry/pxf/) | [Apache Cloudberry PXF](https://cloudberry.apache.org/pxf/) | 文档 `6683faa3`；软件版本 2.2.0-incubating | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [LICENSE](/third_party/pxf/LICENSE)、[NOTICE](/third_party/pxf/NOTICE) |
| [内核原理](/cloudberry/core-internals/) | [Apache Cloudberry 内核原理](https://cloudberry.apache.org/core-internals/) | Main `c2baef0`；3.0.0-devel / PostgreSQL 16.9 | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)、PostgreSQL | [LICENSE](/third_party/core-internals/LICENSE)、[NOTICE](/third_party/core-internals/NOTICE) |
| [PolarDB](/polardb/) | [PolarDB for PostgreSQL Documentation](https://github.com/polardb/polardb-pg-docs) | b4733b0 | Apache-2.0 | [来源与完整声明](/polardb/site/attribution/) |
| [IvorySQL](/ivorysql/) | [IvorySQL Documentation](https://github.com/IvorySQL/ivorysql_docs) | v5.6 · 7c3f4a67e7d3 | LicenseRef-IvorySQL-Docs | [来源与完整声明](/ivorysql/site/license/) |
| [OpenHalo 18](/openhalo/18/) | [PGSTY OpenHalo 18 源码与最终验收](https://github.com/pgsty/openhalo) | v18.6.1（`2627e6f`，aux_mysql 1.9）；2026-11-10 于 `6a93e8f` 验收 | GPL-3.0-only | [来源与完整声明](#openhalo) |
| [OpenHalo（PG14 历史版）](/openhalo/quick-start/) | [OpenHalo documentation](https://github.com/HaloTech-Co-Ltd/openHalo) | master 90fc8d7 | GPL-3.0-only | [来源与完整声明](/openhalo/assets/LICENSE.txt) |
| [Halo Database MySQL 参考](/openhalo/mysql-compatibility/) | [Halo Database 官方文档](https://doc.halodbtech.com/multi-mode-compatibility/mysql) | 1.0.16；2026-11-07 快照 | LicenseRef-HaloDB-Docs | [来源与条款](#halodb) |
| [OpenHalo 测试证据](/openhalo/mysql-compatibility-gaps/) | [OpenHalo MySQL 兼容性测试报告](https://github.com/fxcollot/openHaloDocumentation) | OpenHalo 1.0.14.18；提交 80a8d07 | LicenseRef-OpenHalo-Test-Report | [来源与条款](#openhalo-tests) |
| [Babelfish](/babelfish/) | [Babelfish project website](https://github.com/babelfish-for-postgresql/babelfish_project_website) | main @ f468c5ed3d38 | LicenseRef-Babelfish-Website | [来源与完整声明](/babelfish/site/attribution/) |
| [Percona TDE](/percona/) | [Percona pg_tde documentation](https://github.com/percona/pg_tde) | 2.3.0；文档 5dd7a9e4 | LicenseRef-pg-tde | [来源与完整声明](/percona/assets/legal/pg_tde-COPYRIGHT.txt) |
| [AgensGraph](/agensgraph/) | [AgensGraph documentation](https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/index.html) | 2.18.6.1 | Apache-2.0 | [来源与完整声明](/agensgraph/site/attribution/) |
| [pgEdge](/pgedge/) | [pgEdge extension documentation](https://github.com/pgEdge) | Spock beta.2；LOLOR 开发快照；SafeSession 1.1；Snowflake 2.6.1 | PostgreSQL | [来源与完整声明](/pgedge/about/attribution/) |
| [DocumentDB](/documentdb/) | [DocumentDB documentation](https://github.com/documentdb/docs) | DocumentDB 1.2.0；文档 8fb7fda；网站 4a83a07 | LicenseRef-DocumentDB-Docs | [来源与完整声明](https://github.com/documentdb/docs/tree/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5) |
| [OrioleDB](/orioledb/) | [OrioleDB 文档与基准测试](https://www.orioledb.com/docs) | 2026-11-06 网站快照 | PostgreSQL；网站材料保留上游条款 | [来源与完整声明](/orioledb/attribution/) |
| [Citus](/zh/citus/) | [Microsoft Learn Citus 14](https://learn.microsoft.com/en-us/postgresql/citus/?view=citus-14) | 2026-11-07；逐页记录修订 | CC BY 4.0；代码 MIT | [来源与完整声明](/zh/citus/attribution/) |
{.wide .expand}

所有文档集都是**改编**而非镜像：标题、锚点、交叉链接、代码签名、页面分组与导航结构都为本站重新组织，
上游正文本身则予以保留。页末署名会明确说明这一点，并链接到本站中该页面的修改历史。

## Patroni {#patroni}

于 2026-08-15 从 [Patroni 文档](https://patroni.readthedocs.io/en/latest/) **v4.1.5** 导入。

Patroni 版权归 Compose、Zalando SE 与 Patroni Contributors 所有（Copyright (c) 2025），
依 [MIT 协议](https://opensource.org/license/mit)授权。
完整协议文本保存在[上游仓库](https://github.com/patroni/patroni/blob/master/LICENSE)。

## pgBackRest {#pgbackrest}

于 2026-08-15 从 [pgBackRest 文档站](https://pgbackrest.org/) 导入，英文于 2026-11-21 更新、中文随后同步至 **v2.60.1**，标签为 `release/2.60.1`，提交为 [`7aeba29`](https://github.com/pgbackrest/pgbackrest/commit/7aeba299c49abd768ca741506569007a5cab0870)。

pgBackRest 版权归 The PostgreSQL Global Development Group 与 David Steele 所有（Copyright (c) 2015-2026），
依 [MIT 协议](https://opensource.org/license/mit)授权。
完整协议文本保存在[上游仓库](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE)。

## PgBouncer {#pgbouncer}

于 2026-08-15 从 [PgBouncer 文档站](https://www.pgbouncer.org/) **v1.25.2** 导入，
并于 2026-10-23 更新至 [**v1.26.1**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_1)。

PgBouncer 版权归 Marko Kreen 与 Skype Technologies OÜ 所有（Copyright (c) 2007-2009），
依 [ISC 协议](https://opensource.org/license/isc-license-txt)授权。
完整协议文本保存在[上游仓库](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT)。

## pgBadger {#pgbadger}

于 2026-08-15 从 <https://pgbadger.darold.net/> 以及 [`darold/pgbadger`](https://github.com/darold/pgbadger) 导入，英文于 2026-11-21 更新、中文随后同步至 v13.3，固定提交为 [`0514893`](https://github.com/darold/pgbadger/commit/0514893e97296695c77755fa36c59288c3afef3e)。
这是 2026 年 11 月 3 日正式发布的 v13.3。历史官网摘录与示例报告保留各自的来源。

pgBadger 版权归 Gilles Darold 所有（Copyright (c) 2012-2026），
依 [PostgreSQL 协议](https://opensource.org/license/postgresql)授权。
完整协议文本随离线示例一起发布于
[`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE)，
并保存在站点仓库的 `static/third_party/pgbadger/LICENSE` 中。

> [!IMPORTANT]
> pgBadger 内置了一份修改过的 `SQL::Beautify` 模块，依 Artistic License 2.0 授权；
> 其生成的报告资源还包含 MIT、GPL-2.0 与 SIL Open Font License 1.1 组件。
> 完整的上游资源清单保存在
> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES)。
> 本站发布的[示例报告](/zh/pgbadger/sample-reports/)是历史生成产物，保留其原始内嵌声明。

## HAProxy {#haproxy}

于 2026-08-16 导入，英文于 2026-11-21 更新至官方 [HAProxy v3.4.8 发布版](https://git.haproxy.org/?p=haproxy-3.4.git;a=tag;h=v3.4.8)。完整的 `doc/intro.txt`、`doc/configuration.txt` 和 `doc/management.txt` 三份手册重新组织为 34 个阅读页面。入门与管理手册的来源相比上一快照未变，配置手册的变化记录在更新 diff 中。已审校译文均包含 v3.4.8 更新。

HAProxy 版权归 Willy Tarreau 所有（Copyright 2000-2026），
依 [GNU 通用公共许可证第 2 版](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)授权。
HAProxy 自身的授权说明、OpenSSL 例外条款与完整 GPLv2 文本发布于
[`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) 与
[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0)。

> [!WARNING]
> HAProxy 派生页面**不**适用本站的 CC BY 4.0 协议，而适用 HAProxy 的 GPLv2 条款。

## etcd {#etcd}

英文 v3.7 手册于 2026-11-21 根据 [`etcd-io/website@e60635a46b57`](https://github.com/etcd-io/website/tree/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7) 刷新，中文已同步。安装示例与版本摘要对应 [v3.7.4](https://github.com/etcd-io/etcd/releases/tag/v3.7.4)，提交为 `2e8a5c99e4982c8d4c521be15364ea4c5c68a489`，使用 Go 1.26.11 构建。单独固定的更新日志仍以“v3.7.4 (TBC)”为标题，发布标签则确认该版本已发布。文档与软件来源的校验和分别记录在 `data/upstreams.yaml` 中。

etcd 文档版权归 etcd Authors 所有（Copyright 2013-present）。其正文依
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授权，代码与代码示例依
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) 授权。
完整声明保存在[上游仓库](https://github.com/etcd-io/website/blob/main/LICENSE)。

## Apache Cloudberry {#cloudberry}

英文于 2026-11-21 从 Apache Cloudberry 网站仓库的提交
[`e3a102d15d0e`](https://github.com/apache/cloudberry-site/commit/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c) 导入。来源是
[`versioned_docs/version-2.x`](https://github.com/apache/cloudberry-site/tree/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x) 中的 2.x 文档，上游将其发布于
<https://cloudberry.apache.org/docs/>，对应 2.2.0-incubating 版本。

文档快照与软件发布版本分别记录。Cloudberry `2.2.0-incubating` 采用 PostgreSQL `14.10`，`2.0` 与 `2.1` 采用 `14.4`。较早录制的示例保留原有版本输出。本站保留了上游 [LICENSE](/third_party/cloudberry/LICENSE) 与 [NOTICE](/third_party/cloudberry/NOTICE) 的完整原文。

导航结构沿用上游 2.x 侧边栏。Docusaurus 的提示块、标签页和折叠块改写为 OINK 的提示框与标签页，
图片与使用它的页面放在一起。上游发布但未列入侧边栏的三个页面（TPC-H、TPC-DS 基准测试与 `pg_restore`）
也已收录。上游 19 个失效链接（遗留的 Greenplum 路径与拼写错误）改为指向其所指的页面，一处未闭合的提示块
已闭合，一处拼写错误的标题已更正。中英文版现各有 672 页，包含本轮新增的 31 页与更新的 PXF 指南，覆盖 2.x 文档、PXF 与内核原理手册。中文
保留代码、命令、程序输出和英文标题锚点。另据 2.2 发布版源码，区分了需显式激活的 Coordinator
故障切换与自动提升的 Segment 镜像，并更正了 AO 压实阈值条件；这些修正已同时用于中英文版。

Apache Cloudberry 网站版权归 Apache 软件基金会所有（Copyright 2024-2025 The Apache Software Foundation），
依 [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) 授权。其
[`NOTICE`](https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/NOTICE) 说明，该产品有相当部分最初基于 VMware, Inc. 或其关联公司的
Greenplum Database（Copyright (c) 2004-2020），同样依 Apache License 2.0 授权。页末署名与本节说明这些页面
经过修改。

Apache Cloudberry、Apache 以及 Apache 羽毛标识是 Apache 软件基金会的商标。Apache Cloudberry 是一个在
Apache 孵化器赞助下、于 Apache 软件基金会（ASF）孵化中的项目。所有新接收的项目都需要经历孵化，直到进一步
评审表明其基础设施、沟通与决策流程已稳定到与其他成功的 ASF 项目一致的程度。孵化状态不一定反映代码的完整性
或稳定性，但表明该项目尚未获得 ASF 的完全认可。

## Apache Cloudberry PXF {#pxf}

PXF 文档取自 [`apache/cloudberry-pxf@6683faa38ce4`](https://github.com/apache/cloudberry-pxf/commit/6683faa38ce4e2d146a77197991518aacb4b24e8) 的 `docs/`，由当前 Cloudberry 网站固定。该开发文档包含 Java 17/21 要求，以及比已发布的 [`2.2.0-incubating`](https://github.com/apache/cloudberry-pxf/releases/tag/2.2.0-incubating) 更新的连接器变更。中文已同步至这一快照。

源文档的版权声明为 Copyright 2024-2026 The Apache Software Foundation，依 Apache License 2.0 授权。上游 [NOTICE](https://github.com/apache/cloudberry-pxf/blob/6683faa38ce4e2d146a77197991518aacb4b24e8/NOTICE) 说明，产品包含最初由 Apache HAWQ 开发的软件，并保留 Copyright 2017 The Apache Software Foundation。[LICENSE](https://github.com/apache/cloudberry-pxf/blob/6683faa38ce4e2d146a77197991518aacb4b24e8/LICENSE) 还保留了 Greenplum Platform Extension Framework 的版权声明：Copyright 2018-Present VMware, Inc. or its affiliates。上游[文档首页](https://github.com/apache/cloudberry-pxf/blob/6683faa38ce4e2d146a77197991518aacb4b24e8/docs/index.md#L26-L32) 明确说明，文档源自 `greenplum-db/pxf-archive` 6.10.1；软件分支的来源则单独标为 6.10.1-SNAPSHOT。本社区版调整了格式、导航与链接，并保留上游声明。

本站保留上游 [LICENSE](/third_party/pxf/LICENSE) 与 [NOTICE](/third_party/pxf/NOTICE) 的完整原文。

## Apache Cloudberry 内核原理 {#core-internals}

Core Internals 内核原理手册取自 [`apache/cloudberry@c2baef0`](https://github.com/apache/cloudberry/commit/c2baef068a6f9f8b3c8110f9fdf5758306207693) 的 `doc/core-internals`，这是 Cloudberry 网站固定的子模块版本。它对应 `main` 分支的开发快照：[configure.ac](https://github.com/apache/cloudberry/blob/c2baef068a6f9f8b3c8110f9fdf5758306207693/configure.ac#L23-L24) 标明 Cloudberry `3.0.0-devel` 与 PostgreSQL `16.9`。阅读其中的实现细节时，应以该提交为准。Cloudberry `2.2.0-incubating` 则使用 PostgreSQL `14.10` 内核线。

手册保留 ASF 许可证头，依 Apache License 2.0 授权。仓库 [NOTICE](https://github.com/apache/cloudberry/blob/c2baef068a6f9f8b3c8110f9fdf5758306207693/NOTICE) 声明 Copyright 2024-2026 The Apache Software Foundation，并保留 Greenplum Database 的归属：Copyright (c) 2004-2020 VMware, Inc. or its affiliates。[LICENSE](https://github.com/apache/cloudberry/blob/c2baef068a6f9f8b3c8110f9fdf5758306207693/LICENSE#L203-L206) 将源自 PostgreSQL 的材料单独列为 [PostgreSQL 协议](https://github.com/apache/cloudberry/blob/c2baef068a6f9f8b3c8110f9fdf5758306207693/licenses/LICENSE-postgresql.txt)授权，保留 PostgreSQL 全球开发组与加利福尼亚大学的版权声明。代码摘录继续适用其所引用源文件的授权条款。本社区版调整了格式、导航与链接，并保留手册中的源码引用与致谢。

本站保留上游 [LICENSE](/third_party/core-internals/LICENSE)、[NOTICE](/third_party/core-internals/NOTICE) 与 [PostgreSQL 协议](/third_party/core-internals/LICENSE-postgresql.txt) 的完整原文。

## 本站 {#site}

为 PG.CENTER 原创撰写的内容依
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 发布；
若某页面适用上述上游协议，则以上游协议为准。


首页展示的 PostgreSQL 大象（Slonik）是 PostgreSQL 项目自身的标识，
取自 [postgresql.org 网站仓库](https://git.postgresql.org/gitweb/?p=pgweb.git)，
未经修改地依据 [PostgreSQL 商标与标识政策](https://www.postgresql.org/about/policies/trademarks/)
在此用于指代 PostgreSQL。该标识归 PostgreSQL Community Association of Canada 所有，
在此使用不代表其认可或背书。

环绕大象的各文档集标识均为对应项目自身的 Logo，仅用于指代该项目的文档；
DocumentDB 文档集以 FerretDB 标识呈现，AgensGraph 以 AGEDB 字标中的字母 A 呈现。
这些标识仍归各自所有者所有，在此使用不代表其认可或背书。
PgBouncer 项目没有发布 Logo，本站所用的 PgBouncer 标识是为本站绘制的原创图形，并非 PgBouncer 官方标识。
各标识的具体来源见仓库中的 [NOTICE](https://github.com/pgsty/doc.pg.center/blob/main/NOTICE.md)。

本站由 [OINK](https://oink.pgsty.com/) v1.5.1 构建，该 Hugo 主题依
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) 授权，
其自身的上游与内置依赖声明随模块源码一并提供。

如果发现本页任何归属信息有误，欢迎通过[站点仓库](https://github.com/pgsty/doc.pg.center/issues)提出。


## PolarDB {#polardb}

从固定的 `polardb/polardb-pg-docs` 快照 `b4733b0350888242afeba432a6837458c348a937` 恢复原有 OINK 整理版，保留 8 篇英文、55 篇中文上游正文，以及本站补译的编码风格指南和栏目导读。上游两种语言的内容本来就不对称。Copyright © Alibaba Group, Inc.；上游站点声明采用 Apache 2.0。图片保留原始字节。

[来源与完整声明](/polardb/site/attribution/)。

## IvorySQL {#ivorysql}

迁入现有 IvorySQL 整理版，来源为 `IvorySQL/ivorysql_docs` v5.6，提交 `7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1`。含 75 篇英文、80 篇中文上游正文及栏目、来源声明，两种语言均来自上游各自版本。本次文档快照没有独立 LICENSE 或 NOTICE；不能把软件的 Apache 2.0 许可证扩展解释为全部文档或第三方图片的统一授权。

[来源与完整声明](/ivorysql/site/license/)。

## OpenHalo {#openhalo}

栏目首页现为持续维护的版本导读。[OpenHalo 18 手册](/openhalo/18/)描述 [PGSTY 分支](https://github.com/pgsty/openhalo)的源码标签 `v18.6.1`（`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`，`aux_mysql 1.9`）以及固定在提交 `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a` 的 2026-11-10 独立最终验收原始证据（`6a93e8f..2627e6f` 的 4 个提交仅补充版权注释头、`.gitignore` 规则与文档修订）。`v18.6.1` 多平台二进制安装包仍待完成包级验收，本手册不暗示存在公开安装包下载链接。新增说明与译文由 PGSTY 维护，改编材料保留上游权利。

历史 PG14 构建指南来自 `HaloTech-Co-Ltd/openHalo` 提交 `90fc8d777c3f111d4c8d236625bb15b5d4b19d7c` 的 README，保留原命令与两张原图。PG18 初次复核仍明确对应 `9dc937f`；当前手册不覆盖其历史证据，也不混同另行归属的商业 Halo Database 资料。

保留 GPLv3、PostgreSQL 版权与第三方声明。PostgreSQL 及维护分支的协议钩子采用 PostgreSQL License 条款（部分版权归 PostgreSQL Global Development Group，1996–2025）；`aux_mysql` 派生自 GPLv3 OpenHalo（版权归易景科技 Halo Tech Co., Ltd.，2025；部分修改版权归 PGSTY PTE. LTD.，2026），包含它的构建按 GPLv3 分发。产品商标归原权利人所有。源码指纹与页面溯源记录在 `data/imports/openhalo.json`、`data/imports/openhalo-pgsty.json`。

[来源与完整声明](/openhalo/assets/LICENSE.txt)。

## Halo Database 文档 {#halodb}

MySQL 兼容指南整理自 [Halo Database 官方文档](https://doc.halodbtech.com/multi-mode-compatibility/mysql)，产品版本为 **1.0.16**，快照日期为 2026-11-07。上游页面覆盖 MySQL 模式、SQL 语法、数据类型、函数、操作符、其他兼容特性和引擎参数。本栏目是带有原文链接的短篇原创指南，没有复制完整手册。当前快照未在官方站点识别到公开的文档许可证，相关权利仍以原权利人和官方站点条款为准。

[来源与条款](#halodb)。

## OpenHalo 测试证据 {#openhalo-tests}

兼容边界页整理了独立的 [OpenHalo MySQL 兼容性测试报告](https://github.com/fxcollot/openHaloDocumentation/blob/80a8d077b1d329e397b251fa8c64dbded303bba2/TestingReport/OpenHaloMySQLCompatibilityTestingReport.md)，固定提交为 `80a8d077b1d329e397b251fa8c64dbded303bba2`。报告测试的是 OpenHalo 1.0.14.18，不是 Halo Database 1.0.16。本站只将其作为历史证据并链接原文；固定快照中未识别到仓库许可证，也没有复制报告正文。

[来源与条款](#openhalo-tests)。

## Babelfish {#babelfish}

迁入 `babelfish-for-postgresql/babelfish_project_website` 提交 `f468c5ed3d38849502ee924cb3e236357404d14d` 的双语社区整理版，涵盖文档、历史设计、发布文章、贡献者和来源声明。上游网站的许可记录与 Babelfish 软件的双许可证分别保留，不混为同一授权范围。

[来源与完整声明](/babelfish/site/attribution/)。

## Percona TDE {#percona}

Percona 英文栏目现收录 pg_tde 2.3.0，固定于 `percona/pg_tde@5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a`，在原有 66 篇正文、栏目索引和 PGSTY 编辑导读之外，新增了 2.3.0 发行说明。中文已完成 2.3.0 增量的翻译与审校。这里并非全部 Percona 产品文档；pg_tde 版权文本中的 PostgreSQL、加州大学与 Percona 各部分条款均完整保留。

[来源与完整声明](/percona/assets/legal/pg_tde-COPYRIGHT.txt)。

## AgensGraph {#agensgraph}

迁入现有 AgensGraph 2.18.6.1 整理版。文档版权为 Copyright 2014–2026 SKAI Worldwide Co., Ltd.，采用 Apache 2.0，并保留 PostgreSQL 版权声明。全部 113 个英文页面均有对应中文。本轮对照英文补齐了备份指南、升级演练和 16 篇 Cypher 子句参考。

[来源与完整声明](/agensgraph/site/attribution/)。

## pgEdge {#pgedge}

迁入现有 OINK 站中的 Spock、LOLOR、SafeSession 和 Snowflake 四套文档。本轮英文来源为 Spock v6.0.0-beta.2、LOLOR 1.3.0 开发快照、SafeSession v1.1 和 Snowflake v2.6.1。本轮新增 66 篇中文，按英文逐篇译校 32 篇初稿，并补齐 4 个章节入口的正文。全部 118 个英文页面均有对应中文。SafeSession 手册、变更日志及 LOLOR 发布说明中的安全段落按管理员视角改编。完整保留 PostgreSQL 许可证及各项目版权声明，固定提交见下表。

[来源与完整声明](/pgedge/about/attribution/)。

| 扩展 | 固定提交 |
| --- | --- |
| spock | [d05e2e2b6a82](https://github.com/pgEdge/spock/tree/d05e2e2b6a82) |
| lolor | [1548836b0df0](https://github.com/pgEdge/lolor/tree/1548836b0df0) |
| safesession | [d66225fcceef](https://github.com/pgEdge/pgedge-safesession/tree/d66225fcceef) |
| snowflake | [9506e1bd5c1f](https://github.com/pgEdge/snowflake/tree/9506e1bd5c1f) |

## DocumentDB {#documentdb}

来源为官方 `documentdb/docs` 提交 `8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5`，以及发布网站 `documentdb/documentdb.github.io` 提交 `4a83a0712149e101a2bbb38934bed36497cdf40f`，快照日期为 2026 年 11 月 21 日。306 份文档 Markdown 记录与 20 份网站文章正文合并为 310 页英文，全部提供完整简体中文，其中包括本轮新增的十页。收录范围包括网站生成的 Docker、软件包、运维与离线安装指南、安装引导、分类描述，以及上游架构专章尚未发布的提示。已被替代的来源指南保留正文和提示。独立版本的 Kubernetes Operator 手册链接到其官方网站。

原有中文依据 11 月 7 日的固定英文版本完成 AI 辅助翻译与审校。本轮更新对照 11 月 21 日的英文变更进行了三轮自审，并检查了示例、字面量、链接和标题 ID。代码、命令、输出和上游错误消息保留原文。40 页附有双语编者注，明确指出原文说明或示例中的不一致。文档与网站仓库在这些快照中没有独立的文档许可证；DocumentDB 软件采用 MIT，并不据此另行宣称全部文档获得统一授权。具体权利与许可说明以上游为准。

[文档源文件](https://github.com/documentdb/docs/tree/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5) · [网站源文件](https://github.com/documentdb/documentdb.github.io/tree/4a83a0712149e101a2bbb38934bed36497cdf40f)。

## OrioleDB {#orioledb}

导入 PGSTY 已整理的 OrioleDB 双语社区版本，依据 **2026-11-06** 的上游在线网站快照。收录全部 18 篇文档、两份基准测试指南，加上章节索引与来源说明，中英文各 26 页。`data/imports/orioledb.json` 记录原始 HTML、Markdown、代码和资源的校验值。该网站快照不对应单一软件发布版本，基准测试指南使用 beta18。

项目文档保留 **Copyright (c) 2025-2026, Supabase Inc.**，沿用来源版本从 Apache-2.0 OR PostgreSQL 双重授权中选择的 PostgreSQL 许可证，完整[许可证与免责声明](/third_party/orioledb/LICENSE-POSTGRESQL.txt)已保留。网站与基准测试材料保留 **Copyright © 2026 Supabase Inc** 及原有条款，未核实独立通用的网站内容许可。中文翻译与社区整理署名为 PGSTY；本次导入保留原有译文状态。

[覆盖范围、权利与原文差异](/orioledb/attribution/)。


## Citus {#citus}

[Citus 14 文档集](/zh/citus/)依据 2026-11-07 的 Microsoft Learn 快照整理，
导入 59 个页面（含十篇技术文章），保留本地配图，并提供中英文 OINK 导航。
版权归 Microsoft Corporation 及贡献者所有；文档采用 CC BY 4.0，代码采用 MIT。
完整许可与商标声明、逐页修订、仓库存档和翻译原则见[来源与许可](/zh/citus/attribution/)。
英文原文为准，上游中文机器译文仅作参考。
