---
title: 贡献代码
description: 准备开发环境、提交修改，并参与 PolarDB PostgreSQL 内核贡献。
weight: 450
upstream_link: https://github.com/polardb/polardb-pg-docs/blob/b4733b0350888242afeba432a6837458c348a937/docs/zh/contributing/contributing-polardb-kernel.md
upstream_source: polardb
upstream_modified: true
type: docs
---


PolarDB for PostgreSQL 基于 PostgreSQL 和其它开源项目进行开发，我们的主要目标是为 PostgreSQL 建立一个更大的社区。我们欢迎来自社区的贡献者提交他们的代码或想法。在更远的未来，我们希望这个项目能够被来自阿里云内部和外部的开发者共同管理。

<span id="分支说明与管理方式"></span>

## 分支说明与管理方式 {#branch-description-and-management}

- `POLARDB_15_STABLE` 是 PolarDB-PG 的稳定分支

<span id="贡献代码之前"></span>

## 贡献代码之前 {#before-contributing}

- 签署 PolarDB for PostgreSQL 的 [CLA](https://gist.github.com/alibaba-oss/151a13b0a72e44ba471119c7eb737d74)

<span id="贡献流程"></span>

## 贡献流程 {#contributing}

- 在 `polardb/PolarDB-for-PostgreSQL` 仓库点击 `fork` 复制一个属于您自己的仓库
- 查阅 [进阶部署](/zh/polardb/deploying/deploy/) 了解如何从源码编译开发 PolarDB-PG
- 确保运行 `make stylecheck` 对代码进行格式化，然后向您的仓库推送代码
- 编译详细的提交信息，向上游仓库发起 Pull Request
- 等待所有的 CI 测试通过
- 等待维护者评审您的代码，讨论并解决所有的评审意见
- 等待维护者合并您的代码

<span id="代码提交实例说明"></span>

## 代码提交实例说明 {#an-example-of-submitting-code-change}

<span id="复制您自己的仓库"></span>

### 复制您自己的仓库 {#fork-your-own-repository}

在 [PolarDB for PostgreSQL](https://github.com/polardb/PolarDB-for-PostgreSQL) 的代码仓库页面上，点击右上角的 **fork** 按钮复制您自己的 PolarDB 仓库。

<span id="克隆您的仓库到本地"></span>

### 克隆您的仓库到本地 {#create-local-repository}

```bash
git clone https://github.com/<your-github>/PolarDB-for-PostgreSQL.git
```

<span id="创建本地开发分支"></span>

### 创建本地开发分支 {#create-a-local-development-branch}

从主干分支 `POLARDB_15_STABLE` 上检出一个新的开发分支，假设这个分支名为 `dev`：

```bash
git checkout POLARDB_15_STABLE
git checkout -b dev
```

<span id="在本地仓库修改代码并提交"></span>

### 在本地仓库修改代码并提交 {#make-changes-and-commit-locally}

```bash
git status
git add <files-to-change>
git commit -m "modification for dev"
```

<span id="变基并提交到远程仓库"></span>

### 变基并提交到远程仓库 {#rebase-and-commit-to-remote-repository}

首先点击您自己仓库页面上的 `Fetch upstream` 确保您的开发分支与 PolarDB-PG 上游仓库的稳定分支一致。然后将稳定分支上的最新修改拉取到本地：

```bash
git checkout POLARDB_15_STABLE
git pull
```

接下来将您的开发分支变基到目前的稳定分支，并解决冲突：

```bash
git checkout dev
git rebase POLARDB_15_STABLE
-- 解决冲突 --
git push -f dev
```

<span id="创建-pull-request"></span>

### 创建 Pull Request {#create-a-pull-request}

点击 **New pull request** 或 **Compare & pull request** 按钮，选择对 `polardb/PolarDB-for-PostgreSQL:POLARDB_15_STABLE` 分支和 `<your-github>/PolarDB-for-PostgreSQL:dev` 分支进行比较，并撰写 PR 描述。

GitHub 会对您的 PR 进行自动化的回归测试，您的 PR 需要 100% 通过这些测试。

<span id="解决代码评审中的问题"></span>

### 解决代码评审中的问题 {#address-reviewers-comments}

您可以与维护者就代码中的问题进行讨论，并解决他们提出的评审意见。

<span id="代码合并"></span>

### 代码合并 {#merge}

如果您的代码通过了测试和评审，PolarDB-PG 的维护者将会把您的 PR 合并到稳定分支上。
