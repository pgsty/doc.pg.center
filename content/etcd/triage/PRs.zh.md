---
title: PR 管理
weight: 8200
description: "etcd 拉取请求管理指南"
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/triage/PRs.md"
---

## 目的 {#purpose}

加速 PR 管理。

`etcd` 的 PR 列表位于 https://github.com/etcd-io/etcd/pulls
PR 可能包含多种标签、里程碑、评审人等。标签的详细列表可参见 https://github.com/kubernetes/kubernetes/labels

以下是 PR 中便于参考的若干搜索示例：
* [Open PRS for milestone etcd-v3.4](https://github.com/etcd-io/etcd/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+milestone%3Aetcd-v3.4)
* [PRs under investigation](https://github.com/etcd-io/etcd/labels/Investigating)

## 适用范围 {#scope}

本文指南作为管理 `etcd` 中 PR 的主要文档。欢迎所有人协助管理 PR，但本文讨论的工作与职责是针对 `etcd` 维护者及活跃贡献者设计的。

## 处理无效的 PR 请求 {#handle-inactive-prs}
若评审意见在 15 天内未得到回应，请联系 PR 提交者。若 PR 提交者在 90 天内未回复，且可能的话，请通过提交新提交更新 PR。若无法做到，则应在 180 天后关闭不活跃的 PR。

## 需时审核人审核时提醒 {#poke-reviewer-if-needed}

审阅者会及时响应，但考虑到大家工作繁忙，若未获得快速回复，请在请求审阅后稍等一段时间。若 10 天内未收到回复，可自由通过在 PR 中添加评论，或发送电子邮件，或在 Slack 上发送消息的方式联系他们。

## 验证重要标签已就位 {#verify-important-labels-are-in-place}

请确保已添加适当的评审人员至 PR。同时，请确保已指定里程碑。若缺少上述任一或其它重要标签，请予以补充。若无法确定正确标签，请留言通知维护人员酌情处理。
