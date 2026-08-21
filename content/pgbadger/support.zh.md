---
title: "支持与贡献"
linkTitle: "支持"
weight: 100
description: "报告缺陷、提出功能需求、贡献补丁并寻找 PostgreSQL 专业支持"
icon: fa-solid fa-life-ring
module: [PGBADGER]
categories: [任务]
aliases: [/docs/pgbadger/support/]
upstream_link: "https://pgbadger.darold.net/#support"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

pgBadger 是一个开放维护的项目。缺陷报告、功能建议、文档修复与代码补丁都通过上游 GitHub 仓库处理。

## 缺陷与功能需求 {#bugs-and-features}

1. 升级到最新正式版本，确认问题仍然存在。
2. 搜索[开放问题](https://github.com/darold/pgbadger/issues)与[已关闭问题](https://github.com/darold/pgbadger/issues?q=is%3Aissue+is%3Aclosed)，查看是否已有答案。
3. 把问题缩减为仍能复现的最小安全日志样本与命令行。
4. 删除凭据、敏感 SQL、绑定值、主机名、地址与业务数据。
5. 创建[新问题](https://github.com/darold/pgbadger/issues/new)，写明 pgBadger 版本、操作系统、输入格式、完整选项、实际结果与预期结果。

对于崩溃或解析错误，只应附上复现边界所需的最少脱敏日志。完整生产日志或生成报告通常不适合放在公开问题中。

## 贡献补丁 {#contribute-a-patch}

项目提供 `.editorconfig` 以统一空格与缩进。若改动影响用户可见行为，应同时保持命令帮助、POD 与生成的 Markdown 文档一致。

上游文档生成流程为：

```console
$ perl Makefile.PL
$ make README
```

`doc/pgBadger.pod` 是长篇文档的主要来源；`pgbadger --help` 提供 synopsis，README 文件则是生成视图。提交拉取请求前应运行相关测试。

- [源码仓库](https://github.com/darold/pgbadger)
- [拉取请求](https://github.com/darold/pgbadger/pulls)
- [贡献指南](https://github.com/darold/pgbadger/blob/master/CONTRIBUTING.md)
- [开发说明](https://github.com/darold/pgbadger/blob/master/HACKING.md)

## 商业支持 {#commercial-support}

pgBadger 的许可证不承诺维护或支持。如需 PostgreSQL 日志、性能分析或报告自动化方面的付费协助，请查看 [PostgreSQL 专业服务目录](https://www.postgresql.org/support/professional_support/)。

