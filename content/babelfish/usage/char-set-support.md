---
title: Character Set Support in TSQL and PostgreSQL
linkTitle: Character sets
description: String encodings, code pages, and byte-length limits in T-SQL and PostgreSQL.
weight: 10
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_usage/char_set_support.md
upstream_ref: main @ f468c5ed3d38
upstream_notice: /babelfish/site/attribution/
---


> [!NOTE] Website documentation snapshot
> Upstream moved new documentation to [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) in 2023. Check the [release notes](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases) for the version you use; this page preserves the website documentation.

## Character Set Support in TSQL and PostgreSQL {#character-set-support-in-tsql-and-postgresql}


### String Encoding {#string-encoding}

TSQL and PostgreSQL each support multiple client-side string encodings and multiple server-side string encodings; however, in PostgreSQL there is only one client-side encoding and one server-side encoding, whereas in TSQL every string may specify its own encoding based on the code page of its collation. 

In TSQL, the client side encoding of the `VARCHAR` and `CHAR` data types is determined by the code page of the collation, while the client side encoding of the `NVARCHAR` and `NCHAR` data types is always `UTF-16`.  For example, if a string is declared with data type `VARCHAR(10) COLLATE sql_latin1_general_cp1_ci_as`, it will be encoded on the client using the code page of the `sql_latin1_general_cp1_ci_as` collation, which is `WIN1252`.  `WIN1252` is such a widely used encoding that it gets the special abbreviation `cp1`, which stands for `code page 1`.  The `WIN1252` encoding is a single-byte per character encoding, and can therefore represent only 256 characters.  Prior to the development of Unicode, code pages evolved to cover the characters needed to represent languages in all parts of the world, and code point order of characters in each encoding provided the culturally expected ordering of characters in each region.  This made it possible to support characters from most parts of the world with a single byte per character, and to perform sorting with efficient bytewise comparisons, but it didn’t work for case-insensitive or accent-insensitive comparisons, and having a proliferation of possible encodings led to more complexity in client-side applications, and ultimately led to the development of Unicode.  The `NVARCHAR` and `NCHAR` types represent Unicode strings encoded in `UTF-16`, which can represent characters from around the world, and new characters like emojis, with a single encoding.  Unicode separates the encoding of characters from the ordering and comparison of characters.  

Babelfish emulates TSQL string encodings by storing all strings in UTF-8 on the server, and automatically translating between `UTF-8` and the encoding of the corresponding code page, or `UTF-16`, when data is exchanged between the client and server.

### How maximum string length is interpreted in TSQL and PostgreSQL {#how-maximum-string-length-is-interpreted-in-tsql-and-postgresql}

In PostgreSQL, the `VARCHAR(n)` (or `(CHAR(n)`) datatype specifies a string that may may hold up to (exactly) `n` characters, but in TSQL, the `VARCHAR(n)` (or `CHAR(n)`) datatype specifies a string that may hold up to (exactly) `n` bytes. In Western languages and for the most common European code pages, there is no distinction between bytes and characters because the encoding is 1 byte per character, but what about languages such as Korean, Japanese, or Chinese, where the encodings are variable width?  TSQL encodes the string at `INSERT` or `UPDATE` time to determine if the string meets the maximum string length constraint, so for variable-width encodings, Babelfish must encode the string into the client-side encoding at `INSERT` or `UPDATE` time to check the maximum length in bytes before it can store the string in UTF-8 on the server. 

A peculiar consequence of TSQL’s interpretation, the fixed-length `CHAR(n)` data type can only store strings with exactly `n` bytes, even if the encoding is variable width.  This would seem to make the `CHAR(n)` data type less flexible and probably less useful in languages such as Korean, Japanese, and Chinese.

### Behavior of sys.varchar and sys.sysname data types in the PostgreSQL dialect {#behavior-of-sysvarchar-and-syssysname-data-types-in-the-postgresql-dialect}

As of Babelfish 2.2, the recommendation is to invoke the `CREATE TABLE` statement in the TSQL dialect.  In the TSQL dialect a column declared as `VARCHAR(n)` will resolve to the `sys.varchar` data type and by default will be collated as if `COLLATE DATABASE_DEFAULT` had been specified.
