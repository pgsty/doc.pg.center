---
title: 贡献代码与文档
linkTitle: 贡献指南
description: 提交经过测试的代码、实用文档，并尊重第三方权利。
weight: 30
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_docs/contributing.md
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

## 代码与文档贡献指南 {#guidelines-for-contributing-code-or-documentation}

感谢你愿意为 Babelfish 做贡献。提交拉取请求或 issue 之前，请先阅读本指南。

Babelfish 欢迎贡献，可以通过 [GitHub 拉取请求](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)提交修改。

### 提交代码或文档 {#submitting-code-or-documentation}

确保代码遵循 [PostgreSQL 社区规范](https://www.postgresql.org/docs/current/source.html)，文档与注释符合[写作风格指南](/zh/babelfish/contributing/writing-style-guidelines/)，以减轻维护负担，使 Babelfish 代码和网站能够长期维护。

提交拉取请求前，确保代码经过充分测试，修改不会破坏现有功能。强烈建议先运行测试再提交。新增功能必须附带测试用例；没有相应测试的功能补丁不会被接受。

请为代码编写恰当的文档。如果语言表达有困难，或需要帮助，可以联系 Babelfish 社区。

为新功能编写文档时，最好提供可运行的示例，尤其是编程接口和新的 SQL 函数。

即使你不是程序员，或者不想自己编写补丁，社区也可以提供帮助。欢迎积极反馈，特别是以下方面：

- 增加新内容。
- 更正不准确之处。
- 补充缺失信息。
- 修正拼写或语法错误。
- 提高表达的清晰度。

要参与审阅，请访问 [GitHub](https://github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish)。

### 避免违反许可证 {#avoiding-license-violations}

贡献代码时，必须确保不侵犯第三方权利。社区期望贡献者事先检查知识产权问题，以免 Babelfish 及其用户遭遇第三方索赔。保持代码权属清晰，对社区和用户都有益。

Babelfish for PostgreSQL 是开源软件，可从 GitHub 免费下载，并按 [Apache 2.0 许可证](https://www.apache.org/licenses/LICENSE-2.0)和 [PostgreSQL 许可证](https://www.postgresql.org/about/licence/)使用。
