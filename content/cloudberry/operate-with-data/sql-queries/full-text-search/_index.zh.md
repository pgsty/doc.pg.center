---
title: "全文检索"
description: "Apache Cloudberry 提供用于查询自然语言文档的数据类型、函数、运算符、索引类型和配置。"
weight: 140
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/full-text-search/index.md"
---

- **[关于全文检索](/cloudberry/operate-with-data/sql-queries/full-text-search/full-text-search-intro/)**：本主题概述 Apache Cloudberry 全文检索、基本文本检索表达式，以及文本检索的配置和定制。本文还将 Apache Cloudberry 全文检索与 Apache Cloudberry Text 进行比较。
- **[在数据库表中检索文本](/cloudberry/operate-with-data/sql-queries/full-text-search/search-text-in-db/)**：本主题介绍如何使用文本检索运算符搜索数据库表，以及如何创建索引来加快文本检索。
- **[控制文本检索](/cloudberry/operate-with-data/sql-queries/full-text-search/control-text-search/)**：本主题介绍如何创建检索向量和查询向量、如何对检索结果排名，以及如何在文本检索查询的结果中突出显示检索词。
- **[其他文本检索功能](/cloudberry/operate-with-data/sql-queries/full-text-search/additional-text-search-features/)**：Apache Cloudberry 还提供了其他函数和运算符，可用于操作检索向量和查询向量，以及重写检索查询。
- **[文本检索解析器](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-parsers/)**：本主题介绍 Apache Cloudberry 文本检索解析器从原始文本生成的词元类型。
- **[文本检索词典](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-dictionaries/)**：Apache Cloudberry 全文检索解析器生成的词元会依次经过一系列词典，生成规范化的术语或“词位”。不同类型的词典可以针对不同方式和不同语言过滤、转换词元。
- **[文本检索配置示例](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-configuration/)**：本主题介绍如何创建定制的文本检索配置，以处理文档文本和查询文本。
- **[测试与调试文本检索](/cloudberry/operate-with-data/sql-queries/full-text-search/test-and-debug-text-search/)**：本主题介绍可用于测试和调试检索配置，或配置中指定的单个解析器和词典的 Apache Cloudberry 函数。
- **[文本检索的 GiST 和 GIN 索引](/cloudberry/operate-with-data/sql-queries/full-text-search/preferred-indexes-for-full-text-search/)**：本主题介绍并比较用于全文检索的 Apache Cloudberry 索引类型。
- **[psql 支持](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-psql-support/)**：psql 命令行工具提供了一个元命令，用于显示 Apache Cloudberry 全文检索配置的信息。
- **[限制](/cloudberry/operate-with-data/sql-queries/full-text-search/full-text-search-limitations/)**：本主题列出 Apache Cloudberry 全文检索对象的限制和最大值。
