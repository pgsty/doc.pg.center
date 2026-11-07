---
title: 贡献指南
linkTitle: 贡献与支持
description: 向 Percona pg_tde 贡献代码和文档的流程、CLA、测试与上游 MkDocs 构建方法。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/contribute.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 1000
upstream_source: percona
---

欢迎参与 `pg_tde`——PostgreSQL 透明数据加密扩展！

欢迎加入社区，为项目贡献力量。

可以通过以下方式参与：

1. 在 [Percona 论坛](https://forums.percona.com/c/postgresql/25)联系团队。
2. 提交缺陷报告或功能请求。
3. 提交包含代码补丁的拉取请求（PR）。
4. 为文档作贡献。

## 前置条件 {#prerequisites}

提交代码贡献之前，请完成以下事项。

### 1. 签署 CLA {#1-sign-the-cla}

贡献之前，请签署[贡献者许可协议](https://cla-assistant.percona.com)（CLA）。可以使用 GitHub 账户一键完成。

**注意：** 也可以在提交首个拉取请求时再签署。CLA 助手会验证 PR，并提示签署 CLA 后继续。

### 2. 行为准则 {#2-code-of-conduct}

请阅读并同意[行为准则](https://github.com/percona/community/blob/main/content/contribute/coc.md)。

## 提交拉取请求 {#submitting-a-pull-request}

缺陷报告、改进和功能请求在 [Jira](https://perconadev.atlassian.net/jira/software/c/projects/PG/issues) 跟踪。虽然不是强制要求，但建议先检查问题和 PR 列表，以确认缺陷是否已经处理。

对于功能请求和改进，请先创建 GitHub issue，描述想法，并与上游团队讨论设计，以便与产品发展方向保持一致。

如果缺陷尚未报告或修复，或已与团队商定改进方案，请执行：

1. [Fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) 仓库。
2. 将仓库克隆到本机。
3. 为更改创建独立分支。如果处理 Jira issue，请使用 `<PG-123>-name` 命名，便于跟踪贡献。
4. 修改代码。为提高可读性，按以下优先顺序遵循规范：

    - [PostgreSQL 编码约定](https://www.postgresql.org/docs/current/source.html)
    - [C 风格与编码规则](https://github.com/MaJerle/c-code-style)

5. 为更改编写文档，详见[编写文档](#write-the-docs)。
6. [构建代码](https://github.com/percona/postgres/wiki/Howtos)，并[在本地测试](#run-local-tests)。
7. 提交更改，可参考[提交信息指南](https://gist.github.com/robertpainsi/b632364184e70900af4ab688decf6f53)。
8. 向 Percona 发起拉取请求。
9. 上游团队审核代码和文档。通过后合并；否则会联系你补充信息或修改。

### 运行本地测试 {#run-local-tests}

工作期间应定期运行测试，确认修改没有破坏已有代码。

运行测试：

```sh
ci_scripts/test.sh all
```

可以使用本机的任意操作系统运行测试。提交 PR 后，上游会在多个操作系统上检查补丁。

## 为文档作贡献 {#contribute-to-documentation}

`pg_tde` 文档以 Markdown 编写。可以[为代码修改编写文档](#write-the-docs)，或[通过 GitHub 在线编辑现有文档](#edit-documentation-online-via-github)。如果希望更完整地控制文档流程，也可以[在本地编辑](#edit-documentation-locally)。

开始之前，请了解 [Markdown] 及其写法，也可以参考 [Markdown 语法指南](https://daringfireball.net/projects/markdown/syntax)。

文档文件位于 `documentation/docs` 目录。

### 编写文档 {#write-the-docs}

编写代码时，也要为用户编写相应说明。作者最了解代码如何工作，说明功能或改进时应包含：

1. 功能描述：功能是什么，用户为什么需要它？
2. 用户任务：它能帮助用户解决哪些任务？
3. 工作方式：功能如何运行？
4. 配置要求：如何配置？是否需要已有设置或外部配置，例如新的密钥管理服务（KMS）需要先做哪些设置？
5. 配置步骤：介绍具体步骤、命令和函数参数，提供使用示例及命令输出。
6. 限制与不兼容变更：是否引入已知限制或不兼容变更？

### 通过 GitHub 在线编辑文档 {#edit-documentation-online-via-github}

1. 在上游文档页标题旁点击 **Edit this page**。浏览器会在 GitHub 编辑器中打开该页的 `.md` 文件。如果此前没有参与该仓库，GitHub 会为你创建一个 [fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo)。
2. 编辑页面，在 **Preview** 标签中检查修改。
3. 提交修改。
    * 在 _Commit changes_ 中描述变更。
    * 选择 **Create a new branch for this commit** 并发起拉取请求。
    * 点击 **Propose changes**。
4. GitHub 为变更创建分支和提交，并打开可向 Percona 发起 PR 的页面。页面显示目标分支、提交信息和变更差异，便于最后检查。准备好后点击 **Create pull request**。
5. 上游团队审核 PR，通过后合并到文档并发布到上游站点。

### 在本地编辑文档 {#edit-documentation-locally}

这种方式适合偏好在本机工作，或希望完整控制文档流程的用户。

步骤如下：

1. Fork 仓库。
2. 将仓库克隆到本机：

```sh
git clone --recursive git@github.com:<your-name>/postgres.git
```

3. 进入 `contrib/pg_tde`，添加远程上游仓库：

```sh
git remote add upstream git@github.com:percona/postgres.git
```

4. 拉取上游最新变更：

```sh
git fetch upstream
```

5. 创建独立分支：

```sh
git checkout -b <PG-123-my_branch> upstream/release-2.2.2
```

6. 修改文档。
7. 提交更改，可参考[提交信息指南](https://gist.github.com/robertpainsi/b632364184e70900af4ab688decf6f53)。
8. 向 Percona 发起 PR。

#### 构建文档 {#building-the-documentation}

为检查修改后的效果，需要生成文档静态站点，这个过程称为*构建*。可以选择：

- [使用 Docker](#use-docker)
- [安装 MkDocs 并在本地构建](#install-mkdocs-and-build-locally)

##### 使用 Docker {#use-docker}

1. [安装 Docker](https://docs.docker.com/get-docker/)。
2. 上游使用[文档 Docker 镜像](https://hub.docker.com/repository/docker/perconalab/pmm-doc-md)构建文档，执行：

```sh
cd contrib/pg_tde/documentation
docker run --rm -v $(pwd):/docs perconalab/pmm-doc-md mkdocs build
```

   如果本地找不到镜像，Docker 会先下载，再运行它构建文档。

3. 进入 `site` 目录，打开 `index.html` 查看文档。

要在编辑时实时查看效果，改用：

```sh
cd contrib/pg_tde/documentation
docker run --rm -v $(pwd):/docs -p 8000:8000 perconalab/pmm-doc-md mkdocs serve --dev-addr=0.0.0.0:8000
```

看到 `INFO    -  Start detecting changes` 后，在浏览器地址栏输入 `0.0.0.0:8000`。保存源文件后，文档会自动重新加载。

##### 安装 MkDocs 并在本地构建 {#install-mkdocs-and-build-locally}

1. 安装 [Python]。
2. 安装 MkDocs 和所需扩展：

    ```sh
    pip install -r requirements.txt
    ```

3. 构建站点：

    ```sh
    cd contrib/pg_tde/documentation
    mkdocs build
    ```

4. 打开 `site/index.html`。

也可以运行内置 Web 服务器：

```sh
cd contrib/pg_tde/documentation
mkdocs serve
```

通过 <http://0.0.0.0:8000> 查看站点。

#### 构建 PDF 文件 {#build-pdf-file}

生成 PDF 版本文档的步骤如下：

1. 关闭页面最后修改时间显示：

    ```sh
    export ENABLED_GIT_REVISION_DATE=false
    ```

2. 构建 PDF：

    ```sh
    ENABLE_PDF_EXPORT=1 mkdocs build -f mkdocs-pdf.yml
    ``` 

    PDF 文档位于 `site/pdf` 目录。

[MkDocs]: https://www.mkdocs.org/
[Markdown]: https://daringfireball.net/projects/markdown/
[Git]: https://git-scm.com
[Python]: https://www.python.org/downloads/
[Docker]: https://docs.docker.com/get-docker/
