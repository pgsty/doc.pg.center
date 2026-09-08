---
title: "报告示例"
linkTitle: "报告示例"
weight: 80
description: "从本地站点快照打开完整、仅错误与增量 pgBadger 报告"
icon: fa-solid fa-chart-column
module: [PGBADGER]
categories: [参考]
aliases: [/pgbadger/sample-reports/]
upstream_link: "https://pgbadger.darold.net/#reports"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

示例内容由 pgBadger 11.8 于 2022 年 5 月生成。原始示例已与本站一起保存，因此即使无法访问上游服务器，也能继续使用报告导航、图表、样式与脚本。

| 示例 | 展示内容 | 本地副本 |
|---|---|---|
| 完整报告 | PostgreSQL 活动与 PgBouncer 统计 | [打开完整报告](/third_party/pgbadger/examples/sample.html) |
| 增量报告 | 日历索引、每周累计与每日页面 | [打开增量索引](/third_party/pgbadger/examples/report/index.html) |
| 错误与事件 | 仅包含错误和运行事件的报告 | [打开错误报告](/third_party/pgbadger/examples/errors.html) |

## 完整报告 {#complete-report}

完整报告是一份自包含 HTML 文档。可通过顶部导航查看全局统计、查询、会话、连接、临时文件、检查点、自动清理、锁，以及 PgBouncer 专用图表。

其中数据只是演示样本，不是当前基准测试。数值、PostgreSQL 版本与内嵌 pgBadger 界面都反映报告生成时的状态。

## 增量报告层级 {#incremental-hierarchy}

增量示例保留了完整链接结构：

```text
report/
├── index.html
├── 2012/
│   ├── week-49/index.html
│   ├── week-50/index.html
│   └── 12/06 … 12/index.html
└── 11/
    ├── pgbadger.min.css
    ├── pgbadger.min.js
    └── 图表与界面资源
```

顶层索引链接到两份周报和七份日报。所有相对链接均已保留，因此只移动 `index.html` 会破坏示例；应始终保持完整目录树。

## 安全与隐私 {#security-and-privacy}

真实报告可能暴露 SQL 文本、绑定值、数据库名与用户名、应用名、客户端地址、错误细节和工作负载规律。发布报告前应：

- 不需要字面量时使用 `--anonymize`；
- 在生成报告前应用 include/exclude 过滤条件；
- 检查最终 HTML 或导出数据，而不只是生成命令；
- 像保护运行日志一样保护报告的访问位置。

