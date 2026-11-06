---
title: "全文检索的限制"
description: "本文列出 Apache Cloudberry 全文检索对象的限制和最大值。"
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/full-text-search/full-text-search-limitations.md"
---

Apache Cloudberry 当前文本检索功能的限制如下：

- `tsvector` 和 `tsquery` 类型不支持用作 Apache Cloudberry 表的分布键
- 每个词位的长度必须小于 2K 字节
- `tsvector` 的长度（词位 + 位置）必须小于 1 MB
- `<N>`（FOLLOWED BY）`tsquery` 运算符中的匹配距离不能超过 16,384
- 词位数量必须小于 2^64
- `tsvector` 中的位置值必须大于 0 且不超过 16,383
- 每个词位最多包含 256 个位置
- tsquery 中的节点数（词位 + 运算符）必须小于 32,768

作为比较，PostgreSQL 8.1 文档包含 10,441 个不重复的单词，共 335,420 个单词；出现频率最高的单词“postgresql”在 655 份文档中出现了 6,127 次。

另一个例子是：PostgreSQL 邮件列表存档包含 910,989 个不重复的单词，在 461,020 条消息中共有 57,491,343 个词位。
