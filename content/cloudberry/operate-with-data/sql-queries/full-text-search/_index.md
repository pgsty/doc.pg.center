---
title: "Full Text Search"
description: "Apache Cloudberry provides data types, functions, operators, index types, and configurations for querying natural language documents."
weight: 140
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/full-text-search/index.md"
---

- **[About Full Text Search](/cloudberry/operate-with-data/sql-queries/full-text-search/full-text-search-intro/)**: This topic provides an overview of Apache Cloudberry full text search, basic text search expressions, configuring, and customizing text search. Apache Cloudberry full text search is compared with Apache Cloudberry Text.
- **[Search Text in Database Tables](/cloudberry/operate-with-data/sql-queries/full-text-search/search-text-in-db/)**: This topic shows how to use text search operators to search database tables and how to create indexes to speed up text searches.
- **[Control Text Search](/cloudberry/operate-with-data/sql-queries/full-text-search/control-text-search/)**: This topic shows how to create search and query vectors, how to rank search results, and how to highlight search terms in the results of text search queries.
- **[Additional Text Search Features](/cloudberry/operate-with-data/sql-queries/full-text-search/additional-text-search-features/)**: Apache Cloudberry has additional functions and operators you can use to manipulate search and query vectors, and to rewrite search queries.
- **[Text Search Parsers](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-parsers/)**: This topic describes the types of tokens the Apache Cloudberry text search parser produces from raw text.
- **[Text Search Dictionaries](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-dictionaries/)**: Tokens produced by the Apache Cloudberry full text search parser are passed through a chain of dictionaries to produce a normalized term or "lexeme". Different kinds of dictionaries are available to filter and transform tokens in different ways and for different languages.
- **[Text Search Configuration Example](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-configuration/)**: This topic shows how to create a customized text search configuration to process document and query text.
- **[Test and Debug Text Search](/cloudberry/operate-with-data/sql-queries/full-text-search/test-and-debug-text-search/)**: This topic introduces the Apache Cloudberry functions you can use to test and debug a search configuration or the individual parser and dictionaries specified in a configuration.
- **[GiST and GIN Indexes for Text Search](/cloudberry/operate-with-data/sql-queries/full-text-search/preferred-indexes-for-full-text-search/)**: This topic describes and compares the Apache Cloudberry index types that are used for full text searching.
- **[psql Support](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-psql-support/)**: The psql command-line utility provides a meta-command to display information about Apache Cloudberry full text search configurations.
- **[Limitations](/cloudberry/operate-with-data/sql-queries/full-text-search/full-text-search-limitations/)**: This topic lists limitations and maximums for Apache Cloudberry full text search objects.
