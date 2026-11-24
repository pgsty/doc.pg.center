---
title: 维护与覆盖范围
description: 阅读功能、翻译覆盖与验证范围。
weight: 30
upstream_source: pgedge
upstream_link: https://github.com/pgEdge/spock/tree/4ac1aec2f0807dc7ee806ab99a6e99a4556186df
type: docs
---


## 阅读与反馈 {#reading}

通过搜索查询函数名、参数或中文关键词。页面菜单可切换明暗、Paper / Slate / Ink / Terminal 四种外观，打开 Markdown 或打印视图。已有对应译文的页面支持双语对照。

本站只整理文档，不提供 pgEdge 软件支持。软件问题请到对应上游仓库提交；文档更新需先比较固定快照与新版本，再更新导入清单。

## 覆盖范围 {#coverage}

四套固定版本的手册共有 118 对中英文页面，包括章节入口、函数参考、发布说明和来源说明。本轮将技术示例与英文 Markdown 对照核验。部署过程尚未在数据库上实测。

## 已知上游问题 {#upstream-issues}

- [双节点教程](/zh/pgedge/spock/two-node/)第三步要求编辑 `pg_hba.conf`，括号中的示例路径却以 `postgresql.conf` 结尾。认证规则应写入实例实际使用的 `pg_hba.conf`；可用 `SHOW hba_file;` 查询路径。
- [使用限制](/zh/pgedge/spock/limitations/#ddl-statements-not-replicated)把 `CREATE TABLE...AS...` 列入“不复制”的语句列表，紧接着又写明它会被复制。本站保留这一原文矛盾；实际行为需核对所用版本。

这些是固定快照中的问题，尚未作为修订提交给上游。本站校注与原文分开标识。
