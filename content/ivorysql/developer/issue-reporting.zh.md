---
title: 问题提交指南
linkTitle: 问题提交指南
description: IvorySQL v5.6 文档：问题提交指南。
type: docs
weight: 560
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/33.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

本文详细描述如何提交一个问题。

以IvorySQL为例，提交一个bug report

## 1. 确认问题所属仓库 {#确认问题所属仓库}

IvorySQL仓库： <a href="https://github.com/IvorySQL/IvorySQL" class="bare">https://github.com/IvorySQL/IvorySQL</a>

## 2. **创建新的Issue** {#创建新的issue}

### 2.1. 第1步 进入New issue 页面： {#第1步-进入new-issue-页面}

点击New issue

![p3](/ivorysql/assets/images/upstream/8413f3ab712dab5baf51bf0d23f03b470b99835933d742721e29bd45afa3263c.png)

### 2.2. 第2步：选择需要填写的issue类型 {#第2步选择需要填写的issue类型}

**1、bug report**

```
Title: 标题
```

```
## Bug Report
对bug进行描述


### IvorySQL Version
在IvorySQL哪个版本发现的问题

### OS Version (uname -a)
系统版本

### Configuration options  ( config.status --config )
配置参数

### Current Behavior
当前的结果

### Expected behavior/code
期望的结果

### Step to reproduce
复现步骤

### Additional context that can be helpful for identifying the problem
有助于识别问题的其它信息
```

**2、Enhancement**

```
Title: 标题
```

```
## Enhancement
对于期望强化的功能作一个描述
```

**3、Feature Request**

```
Title: 标题
```

```
## Feature Request
描述你期望实现的一个功能
```

### 2.3. 第3步：提交 {#第3步提交}

点击 submit new issue 按钮, 提交即可。

提交问题以后，如果问题的描述和复现步骤清晰明确和可定位，会有人直接定位和解决该问题。但也有可能会出现，负责跟进该问题的开发者需要您提供更加详细的信息的情况，也感谢您的配合。
