---
title: Issue 分类处置指南
weight: 8100
description: "etcd Issue 分类处置指南"
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/triage/issues.md"
aliases: [/etcd/triage/issues/]
---

## 目的 {#purpose}

加快问题管理。

`etcd` 问题列于 https://github.com/etcd-io/etcd/issues，并以标签标识。例如，被识别为缺陷的问题最终将被标记为 `area/bug `。新创建的问题初始时无标签，但通常由 `etcd` 维护者和活跃贡献者根据其分析结果添加标签。标签的详细列表可参见 https://github.com/kubernetes/kubernetes/labels

以下是为方便起见预设的若干问题搜索：
* [缺陷](https://github.com/etcd-io/etcd/labels/area%2Fbug)
* [Help Wanted](https://github.com/etcd-io/etcd/labels/Help%20Wanted)
* [长期未分类处置的问题](https://github.com/etcd-io/etcd/issues?utf8=%E2%9C%93&q=is%3Aopen+sort%3Aupdated-asc+)
* [Issue 分类处置会议](https://etcd.io/community/#community-meetings)

## 适用范围 {#scope}

本文指南作为对 `etcd` 新提交问题进行分类处置的首要文档。欢迎所有人协助管理问题和拉取请求，但本文讨论的工作与职责是针对 `etcd` 维护者及活跃贡献者设计的。

## 验证问题是否为 bug {#validate-if-an-issue-is-a-bug}

请验证该问题是否确实为 bug。若否，请添加带有分析结论的评论，并关闭无关紧要的问题。对于非无关紧要的问题，等待问题报告者回复，确认是否存在异议。若问题报告者 30 天内未回复，关闭该问题。若问题无法复现或需要更多信息，请向问题报告者留言说明。

## 不活跃的问题 {#inactive-issues}

若问题报告者在 60 天内未提供足够信息，则应关闭该问题。

## 重复问题 {#duplicate-issues}

如果问题为重复问题，请添加评论说明情况，并附上原始问题的引用链接，然后关闭该问题。

## 不属于 etcd 的问题 {#issues-that-dont-belong-to-etcd}

有时报告的问题实际上属于 `etcd` 所使用的其他项目，例如 `grpc` 或 `golang` 的问题。此类问题应要求报告者在相应的其他项目中提交。除非维护者与问题报告者认为有必要保留该问题以用于追踪，否则应关闭问题。

## 验证重要标签已就位 {#verify-important-labels-are-in-place}

请确保问题已添加所属领域标签，已正确分配负责人，并已确定里程碑。若缺少任一标签，请补充添加。若因权限受限无法分配标签，或无法确定正确标签，亦可接受，必要时请联系维护者。

## 必要时催促问题负责人 {#poke-issue-owner-if-needed}

若某开发者负责的问题在 30 天内未提交任何 PR，应联系问题负责人，要求其提交 PR 或在必要时释放所有权。
