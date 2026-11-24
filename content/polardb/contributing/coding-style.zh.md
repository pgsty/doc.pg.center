---
title: "编码风格"
description: "PolarDB 贡献者编写和评审代码时应遵循的编码约定、设计原则和测试要求。"
weight: 470
upstream_link: https://github.com/polardb/polardb-pg-docs/blob/b4733b0350888242afeba432a6837458c348a937/docs/contributing/coding-style.md
upstream_source: polardb
upstream_modified: true
type: docs
translation_notice: en
translation_status: translated
---


## 开发语言 {#languages}

- PostgreSQL 内核、扩展以及内核相关工具使用 C，以便与社区版本保持兼容，方便后续升级。
- 管理工具可使用 shell、Go 或 Python，以提高开发效率。

## 编码约定 {#style}

- C 代码遵循 PostgreSQL 的编程风格，包括命名、错误消息格式、控制语句、行长、注释格式、函数长度和全局变量的使用。详情见 [PostgreSQL 编码约定](https://www.postgresql.org/docs/15/source.html)。以下是其中几项要求。

  - PostgreSQL 代码只应依赖 C99 标准提供的语言特性。
  - 注释不要使用 `//`。
  - 带参数的宏和静态内联函数都可以使用。按 PolarDB 原文的表述，仅当宏能简化编码时，才优先使用静态内联函数。
  - 遵循 BSD 的 C 编程约定。

- Shell 程序可遵循 [Google Shell 风格指南](https://google.github.io/styleguide/shellguide.html)。
- Perl 程序可遵循[官方 Perl 风格指南](https://perldoc.perl.org/perlstyle)。

## 代码设计与评审 {#code-design-and-review}

我们采用 [Google 开源代码评审指南](https://github.com/google/eng-practices/blob/master/review/index.md)的理念与规则。

提交代码评审前，请运行单元测试，并确保 `src/test` 下的所有测试均通过，包括回归测试和隔离测试。提交代码改动时应一并提交单元测试或功能测试。

这份指南还覆盖从设计、实现、测试和文档编写到准备代码评审的整个开发过程。它针对关键环节提出问题，涉及设计、功能、复杂度、测试、命名、文档和代码评审。评审时应逐项确认以下事项。

- 代码设计合理。
- 功能对使用者有益。
- 界面改动合理，外观得当。
- 并行代码能够安全执行。
- 代码的复杂度没有超出实际需要。
- 开发者没有为了将来可能出现、眼下尚不确定的需求预先实现功能。
- 代码配有适当的单元测试。
- 测试设计合理。
- 所有名称都清晰明确。
- 注释清楚、有用，主要说明这样做的原因。
- 代码配有适当的文档。
- 代码符合项目的风格指南。
