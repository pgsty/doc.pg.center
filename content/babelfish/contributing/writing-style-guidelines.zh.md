---
title: 写作风格指南
linkTitle: 写作风格
description: 遵循上游关于清晰、一致与包容的技术文档写作规范。
weight: 40
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_docs/writing-style-guidelines.md
upstream_ref: main @ f468c5ed3d38
translation_notice: en
upstream_modified: true
translation_status: complete
translation_credit: PGSTY 文档项目
upstream_notice: /zh/babelfish/site/attribution/
upstream_license: LicenseRef-Babelfish-Website-ZH
---



> [!NOTE] 文档快照
> 本文译自上游网站，中文翻译由 PGSTY 文档项目整理。上游自 2023 年起将新文档迁至 [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki)；请结合所用版本的[发行说明](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases)核对功能支持。

## 写作风格指南 {#writing-style-guidelines}

向 Babelfish 指南提交内容或编写代码注释时，请遵循以下准则。

文档可以不拘正式文体，但不要闲聊。目标是提供简洁、技术准确的内容，帮助读者完成任务。不要加入未来计划、功能规划时的想法，或实现决策背后的理由；这类信息应保留在产品路线图中。

使用主动语态，假定读者就是执行操作的人，例如“你应指定与……关联的密码”，或者直接写“指定与……关联的密码”。围绕用户任务及完成任务所需的步骤展开，并链接到有帮助的页面或项目。

提到专有产品时，在页面开头首次出现处使用完整公司名和产品名，此后只用产品名。适当时可以直接使用语法或协议名称：

- Microsoft SQL Server 是完整的公司名与产品名。例如：“Babelfish 为 PostgreSQL 数据库增加接收 Microsoft SQL Server 客户端连接的能力。”
- SQL Server 指数据库、数据库内容，以及不只涉及 SQL 语法的事务、过程和函数。例如：“端口 1433 接受 SQL Server 命令，限制见本指南后文。”
- 谈论语法或语言时使用 T-SQL。例如：“编写命令时应使用正确的 T-SQL 语法。”
- 谈论 SQL Server 协议时使用 TDS。例如：“服务器在端口 1466 上监听使用 TDS 协议的客户端连接。”

为便于阅读和理解：

- 使用简短但完整的句子。
- 保持标点用法一致。
- 适当使用项目列表和表格。

避免使用：

- 行话或俚语，包括营销、开发和内部术语。
- 口头俗语。
- 问句。
- 拉丁语缩写，如 `vs.`、`e.g.`、`i.e.`、`etc.`。

Babelfish 倡导多元与平等。为促进包容性，除非用于对象名、命令等字面或严格技术语境，应避免以下词语，改用所列替代词。以下是对英文文档的用词要求：

- `execute` → `start` 或 `run`
- `abort` → `stop`
- `enable` → `turn on`、`activate` 或 `start`
- `disable` → `turn off`、`deactivate` 或 `stop`
- `kill` → `end` 或 `stop`
- `blacklist` → `deny list`
- `master` → `primary`、`main` 或 `leader`
- `hang` → `stop responding`
- `slave` → `secondary`、`replica` 或 `standby`
- `black day` → `blocked day`
- `invalid` → `not valid`
- `segregate` → `isolate` 或 `separate`
- `it is recommended` → `we recommend`

适当使用 `we’re`、`isn’t`、`can’t` 等缩写。
