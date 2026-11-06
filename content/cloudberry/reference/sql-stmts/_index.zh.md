---
title: "SQL 语句索引"
linkTitle: "SQL 语句"
description: "按数据库对象和操作整理 Apache Cloudberry SQL 语句。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/index.md"
---

## 访问方法 {#access-method}

- [CREATE ACCESS METHOD](/cloudberry/reference/sql-stmts/create-access-method/) - 定义一个新的访问方法。
- [DROP ACCESS METHOD](/cloudberry/reference/sql-stmts/drop-access-method/) - 删除访问方法。

## 类型转换 {#cast}

- [CREATE CAST](/cloudberry/reference/sql-stmts/create-cast/) - 定义一个新的类型转换。
- [DROP CAST](/cloudberry/reference/sql-stmts/drop-cast/) - 删除类型转换。

## 排序规则 {#collation}

- [CREATE COLLATION](/cloudberry/reference/sql-stmts/create-collation/) - 定义一个新的排序规则。
- [ALTER COLLATION](/cloudberry/reference/sql-stmts/alter-collation/) - 更改一个排序规则的定义。
- [DROP COLLATION](/cloudberry/reference/sql-stmts/drop-collation/) - 删除先前定义的排序规则。

## 编码转换 {#conversion}

- [CREATE CONVERSION](/cloudberry/reference/sql-stmts/create-conversion/) - 定义一个新的编码转换。
- [ALTER CONVERSION](/cloudberry/reference/sql-stmts/alter-conversion/) - 更改一个编码转换的定义。
- [DROP CONVERSION](/cloudberry/reference/sql-stmts/drop-conversion/) - 删除编码转换。

## 游标 {#cursor}

- [DECLARE](/cloudberry/reference/sql-stmts/declare/) - 定义游标。
- [CLOSE](/cloudberry/reference/sql-stmts/close/) - 关闭一个游标。
- [FETCH](/cloudberry/reference/sql-stmts/fetch/) - 使用游标从查询中检索行。
- [MOVE](/cloudberry/reference/sql-stmts/move/) - 定位游标。
- [RETRIEVE](/cloudberry/reference/sql-stmts/retrieve/) - 使用并行检索游标从查询中检索行。

## 数据库 {#database}

- [CREATE DATABASE](/cloudberry/reference/sql-stmts/create-database/) - 创建一个新数据库。
- [ALTER DATABASE](/cloudberry/reference/sql-stmts/alter-database/) - 更改一个数据库的属性。
- [DROP DATABASE](/cloudberry/reference/sql-stmts/drop-database/) - 删除数据库。
- [ANALYZE](/cloudberry/reference/sql-stmts/analyze/) - 收集数据库的统计信息。
- [VACUUM](/cloudberry/reference/sql-stmts/vacuum/) - 回收数据库中的垃圾，并可选择执行分析。
- [CHECKPOINT](/cloudberry/reference/sql-stmts/checkpoint/) - 强制执行一次预写式日志检查点。
- [COMMENT](/cloudberry/reference/sql-stmts/comment/) - 定义或更改对象的注释。
- [COPY](/cloudberry/reference/sql-stmts/copy/) - 在文件和表之间复制数据。
- [LOAD](/cloudberry/reference/sql-stmts/load/) - 加载或重新加载共享库文件。

## 域 {#domain}

- [CREATE DOMAIN](/cloudberry/reference/sql-stmts/create-domain/) - 定义一个新的域。
- [ALTER DOMAIN](/cloudberry/reference/sql-stmts/alter-domain/) - 更改一个域的定义。
- [DROP DOMAIN](/cloudberry/reference/sql-stmts/drop-domain/) - 删除域。

## 扩展 {#extension}

- [CREATE EXTENSION](/cloudberry/reference/sql-stmts/create-extension/) - 在 Apache Cloudberry 中注册一个扩展。
- [ALTER EXTENSION](/cloudberry/reference/sql-stmts/alter-extension/) - 更改一个扩展的定义。
- [DROP EXTENSION](/cloudberry/reference/sql-stmts/drop-extension/) - 从 Apache Cloudberry 中删除扩展。

## 外部表 {#external-table}

- [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) - 定义新的外部表。
- [ALTER EXTERNAL TABLE](/cloudberry/reference/sql-stmts/alter-external-table/) - 更改一个外部表的定义。
- [DROP EXTERNAL TABLE](/cloudberry/reference/sql-stmts/drop-external-table/) - 删除外部表定义。

## 外部数据包装器 {#foreign-data-wrapper}

- [CREATE FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/create-foreign-data-wrapper/) - 定义新的外部数据包装器。
- [ALTER FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/alter-foreign-data-wrapper/) - 更改一个外部数据包装器的定义。
- [DROP FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/drop-foreign-data-wrapper/) - 删除外部数据包装器。

## 函数与聚合函数 {#function--aggregate-function}

### 函数 {#function}

- [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/) - 定义一个新函数。
- [ALTER FUNCTION](/cloudberry/reference/sql-stmts/alter-function/) - 更改函数的定义。
- [DROP FUNCTION](/cloudberry/reference/sql-stmts/drop-function/) - 删除函数。

### 聚合函数 {#aggregate-function}

- [CREATE AGGREGATE](/cloudberry/reference/sql-stmts/create-aggregate/) - 定义一个新的聚合函数。
- [ALTER AGGREGATE](/cloudberry/reference/sql-stmts/alter-aggregate/) - 更改一个聚合函数的定义。
- [DROP AGGREGATE](/cloudberry/reference/sql-stmts/drop-aggregate/) - 删除聚合函数。

## 外表 {#foreign-table}

- [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/) - 定义新的外表。
- [ALTER FOREIGN TABLE](/cloudberry/reference/sql-stmts/alter-foreign-table/) - 更改一个外表的定义。
- [DROP FOREIGN TABLE](/cloudberry/reference/sql-stmts/drop-foreign-table/) - 删除外表。

## 用户与组 {#user--group}

- [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/) - 定义新的数据库角色（用户或组）。
- [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/) - 修改数据库角色（用户或组）。
- [SET ROLE](/cloudberry/reference/sql-stmts/set-role/) - 设置当前会话的当前角色标识符。
- [DROP ROLE](/cloudberry/reference/sql-stmts/drop-role/) - 删除数据库角色。
- [CREATE USER](/cloudberry/reference/sql-stmts/create-user/) - 定义新的数据库角色。
- [ALTER USER](/cloudberry/reference/sql-stmts/alter-user/) - 更改数据库角色的定义。
- [DROP USER](/cloudberry/reference/sql-stmts/drop-user/) - 删除数据库角色。
- [CREATE GROUP](/cloudberry/reference/sql-stmts/create-group/) - 定义新的数据库角色。
- [ALTER GROUP](/cloudberry/reference/sql-stmts/alter-group/) - 更改角色名称或成员关系。
- [DROP GROUP](/cloudberry/reference/sql-stmts/drop-group/) - 删除数据库角色。
- [DROP OWNED](/cloudberry/reference/sql-stmts/drop-owned/) - 删除数据库角色拥有的数据库对象。
- [REASSIGN OWNED](/cloudberry/reference/sql-stmts/reassign-owned/) - 更改数据库角色所拥有的数据库对象的所有权。

## 索引 {#index}

- [CREATE INDEX](/cloudberry/reference/sql-stmts/create-index/) - 定义新的索引。
- [ALTER INDEX](/cloudberry/reference/sql-stmts/alter-index/) - 更改索引的定义。
- [REINDEX](/cloudberry/reference/sql-stmts/reindex/) - 重建索引。
- [DROP INDEX](/cloudberry/reference/sql-stmts/drop-index/) - 删除索引。

## 通知 {#notification}

- [NOTIFY](/cloudberry/reference/sql-stmts/notify/) - 生成通知。
- [LISTEN](/cloudberry/reference/sql-stmts/listen/) - 监听通知。
- [UNLISTEN](/cloudberry/reference/sql-stmts/unlisten/) - 停止监听通知。

## 过程语言 {#procedural-language}

- [CREATE LANGUAGE](/cloudberry/reference/sql-stmts/create-language/) - 定义新的过程语言。
- [ALTER LANGUAGE](/cloudberry/reference/sql-stmts/alter-language/) - 更改过程语言的定义。
- [DROP LANGUAGE](/cloudberry/reference/sql-stmts/drop-language/) - 删除过程语言。
- [DO](/cloudberry/reference/sql-stmts/do/) - 将匿名代码块作为临时匿名函数执行。

## 视图与物化视图 {#view-and-materialized-view}

- [CREATE VIEW](/cloudberry/reference/sql-stmts/create-view/) - 定义新的视图。
- [ALTER VIEW](/cloudberry/reference/sql-stmts/alter-view/) - 更改视图的属性。
- [DROP VIEW](/cloudberry/reference/sql-stmts/drop-view/) - 删除视图。
- [CREATE MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/create-materialized-view/) - 定义新的物化视图。
- [ALTER MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/alter-materialized-view/) - 更改物化视图的定义。
- [DROP MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/drop-materialized-view/) - 删除物化视图。
- [REFRESH MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/refresh-materialized-view/) - 替换物化视图的内容。

## 操作符、操作符类与操作符族 {#operator--operator-class--operator-family}

### 操作符 {#operator}

- [CREATE OPERATOR](/cloudberry/reference/sql-stmts/create-operator/) - 定义新的操作符。
- [ALTER OPERATOR](/cloudberry/reference/sql-stmts/alter-operator/) - 更改操作符的定义。
- [DROP OPERATOR](/cloudberry/reference/sql-stmts/drop-operator/) - 删除操作符。

### 操作符类 {#operator-class}

- [CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/) - 定义新的操作符类。
- [ALTER OPERATOR CLASS](/cloudberry/reference/sql-stmts/alter-operator-class/) - 更改一个操作符类的定义。
- [DROP OPERATOR CLASS](/cloudberry/reference/sql-stmts/drop-operator-class/) - 移除一个操作符类。

### 操作符族 {#operator-family}

- [CREATE OPERATOR FAMILY](/cloudberry/reference/sql-stmts/create-operator-family/) - 定义新的操作符族。
- [ALTER OPERATOR FAMILY](/cloudberry/reference/sql-stmts/alter-operator-family/) - 更改操作符族的定义。
- [DROP OPERATOR FAMILY](/cloudberry/reference/sql-stmts/drop-operator-family/) - 移除一个操作符族。

## 权限与安全 {#privilege--security}

### 权限 {#privilege}

- [GRANT](/cloudberry/reference/sql-stmts/grant/) - 定义访问权限。
- [ALTER DEFAULT PRIVILEGES](/cloudberry/reference/sql-stmts/alter-default-privileges/) - 更改默认访问权限。
- [REVOKE](/cloudberry/reference/sql-stmts/revoke/) - 移除访问权限。

### 行级安全策略 {#row-level-security-policy}

- [CREATE POLICY](/cloudberry/reference/sql-stmts/create-policy/) - 为表定义新的行级安全策略。
- [ALTER POLICY](/cloudberry/reference/sql-stmts/alter-policy/) - 更改行级安全策略的定义。
- [DROP POLICY](/cloudberry/reference/sql-stmts/drop-policy/) - 从表中删除行级安全策略。

## 过程 {#procedure}

- [CREATE PROCEDURE](/cloudberry/reference/sql-stmts/create-procedure/) - 定义新的过程。
- [ALTER PROCEDURE](/cloudberry/reference/sql-stmts/alter-procedure/) - 更改存储过程的定义。
- [DROP PROCEDURE](/cloudberry/reference/sql-stmts/drop-procedure/) - 删除过程。
- [CALL](/cloudberry/reference/sql-stmts/call/) - 调用一个过程。

## 协议 {#protocol}

- [CREATE PROTOCOL](/cloudberry/reference/sql-stmts/create-protocol/) - 注册自定义数据访问协议，供定义 Apache Cloudberry 外部表时使用。
- [ALTER PROTOCOL](/cloudberry/reference/sql-stmts/alter-protocol/) - 更改协议的定义。
- [DROP PROTOCOL](/cloudberry/reference/sql-stmts/drop-protocol/) - 从数据库中删除数据访问协议。

## 资源管理 {#resource-management}

### 资源组 {#resource-group}

- [CREATE RESOURCE GROUP](/cloudberry/reference/sql-stmts/create-resource-group/) - 定义新的资源组。
- [ALTER RESOURCE GROUP](/cloudberry/reference/sql-stmts/alter-resource-group/) - 修改资源组的限制。
- [DROP RESOURCE GROUP](/cloudberry/reference/sql-stmts/drop-resource-group/) - 删除资源组。

### 资源队列 {#resource-queue}

- [CREATE RESOURCE QUEUE](/cloudberry/reference/sql-stmts/create-resource-queue/) - 定义新的资源队列。
- [ALTER RESOURCE QUEUE](/cloudberry/reference/sql-stmts/alter-resource-queue/) - 修改资源队列的限制。
- [DROP RESOURCE QUEUE](/cloudberry/reference/sql-stmts/drop-resource-queue/) - 删除资源队列。

## 例程 {#routine}

- [ALTER ROUTINE](/cloudberry/reference/sql-stmts/alter-routine/) - 修改例程的定义。
- [DROP ROUTINE](/cloudberry/reference/sql-stmts/drop-routine/) - 删除例程。

## 规则 {#rule}

- [CREATE RULE](/cloudberry/reference/sql-stmts/create-rule/) - 定义新的重写规则。
- [ALTER RULE](/cloudberry/reference/sql-stmts/alter-rule/) - 修改规则的定义。
- [DROP RULE](/cloudberry/reference/sql-stmts/drop-rule/) - 删除重写规则。

## 行 {#row}

- [INSERT](/cloudberry/reference/sql-stmts/insert/) - 在表中创建新行。
- [SELECT](/cloudberry/reference/sql-stmts/select/) - 从表或视图中检索行。
- [UPDATE](/cloudberry/reference/sql-stmts/update/) - 更新表中的行。
- [VALUES](/cloudberry/reference/sql-stmts/values/) - 计算一组行。

## 模式 {#schema}

- [CREATE SCHEMA](/cloudberry/reference/sql-stmts/create-schema/) - 定义新的模式。
- [ALTER SCHEMA](/cloudberry/reference/sql-stmts/alter-schema/) - 修改模式的定义。
- [DROP SCHEMA](/cloudberry/reference/sql-stmts/drop-schema/) - 删除模式。

## 序列 {#sequence}

- [CREATE SEQUENCE](/cloudberry/reference/sql-stmts/create-sequence/) - 定义新的序列生成器。
- [ALTER SEQUENCE](/cloudberry/reference/sql-stmts/alter-sequence/) - 修改序列生成器的定义。
- [DROP SEQUENCE](/cloudberry/reference/sql-stmts/drop-sequence/) - 删除序列。

## 会话 {#session}

- [SET SESSION AUTHORIZATION](/cloudberry/reference/sql-stmts/set-session-authorization/) - 设置当前会话的会话角色标识符和当前角色标识符。
- [DISCARD](/cloudberry/reference/sql-stmts/discard/) - 丢弃会话状态。

## 外部服务器 {#foreign-server}

- [CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/) - 定义新的外部服务器。
- [ALTER SERVER](/cloudberry/reference/sql-stmts/alter-server/) - 修改外部服务器的定义。
- [DROP SERVER](/cloudberry/reference/sql-stmts/drop-server/) - 删除外部服务器描述符。
- [CREATE USER MAPPING](/cloudberry/reference/sql-stmts/create-user-mapping/) - 定义用户到外部服务器的新映射。
- [ALTER USER MAPPING](/cloudberry/reference/sql-stmts/alter-user-mapping/) - 更改外部服务器的用户映射的定义。
- [DROP USER MAPPING](/cloudberry/reference/sql-stmts/drop-user-mapping/) - 删除外部服务器的用户映射。

## 统计对象 {#statistics-object}

- [CREATE STATISTICS](/cloudberry/reference/sql-stmts/create-statistics/) - 定义扩展统计信息。
- [ALTER STATISTICS](/cloudberry/reference/sql-stmts/alter-statistics/) - 修改扩展统计信息对象的定义。
- [DROP STATISTICS](/cloudberry/reference/sql-stmts/drop-statistics/) - 删除扩展统计信息。

## 表 {#table}

- [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/) - 定义新的表。
- [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) - 修改表的定义。
- [DROP TABLE](/cloudberry/reference/sql-stmts/drop-table/) - 删除表。
- [CLUSTER](/cloudberry/reference/sql-stmts/cluster/) - 根据索引在磁盘上对表进行物理重排序。
- [CREATE TABLE AS](/cloudberry/reference/sql-stmts/create-table-as/) - 根据查询结果定义新表。
- [DELETE](/cloudberry/reference/sql-stmts/delete/) - 从表中删除行。
- [TRUNCATE](/cloudberry/reference/sql-stmts/truncate/) - 清空一个表或一组表中的所有行。
- [IMPORT FOREIGN SCHEMA](/cloudberry/reference/sql-stmts/import-foreign-schema/) - 从外部服务器导入表定义。
- [SELECT INTO](/cloudberry/reference/sql-stmts/select-into/) - 根据查询结果定义新表。

## 表空间 {#tablespace}

- [CREATE TABLESPACE](/cloudberry/reference/sql-stmts/create-tablespace/) - 定义新的表空间。
- [ALTER TABLESPACE](/cloudberry/reference/sql-stmts/alter-tablespace/) - 更改表空间的定义。
- [DROP TABLESPACE](/cloudberry/reference/sql-stmts/drop-tablespace/) - 删除表空间。

## 文本检索 {#text-search}

### 文本检索配置 {#text-search-configuration}

- [CREATE TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/create-text-search-configuration/) - 定义新的文本检索配置。
- [ALTER TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/alter-text-search-configuration/) - 更改文本检索配置的定义。
- [DROP TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/drop-text-search-configuration/) - 删除文本检索配置。

### 文本检索字典 {#text-search-dictionary}

- [CREATE TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/create-text-search-dictionary/) - 定义新的文本检索字典。
- [ALTER TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/alter-text-search-dictionary/) - 更改文本检索词典的定义。
- [DROP TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/drop-text-search-dictionary/) - 删除文本检索字典。

### 文本检索解析器 {#text-search-parser}

- [CREATE TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/create-text-search-parser/) - 定义新的文本检索解析器。
- [ALTER TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/alter-text-search-parser/) - 更改文本检索解析器的定义。
- [DROP TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/drop-text-search-parser/) - 删除文本检索解析器。

### 文本检索模板 {#text-search-template}

- [CREATE TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/create-text-search-template/) - 定义新的文本检索模板。
- [ALTER TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/alter-text-search-template/) - 更改文本检索模板的定义。
- [DROP TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/drop-text-search-template/) - 删除文本检索模板。

## 转换 {#transform}

- [CREATE TRANSFORM](/cloudberry/reference/sql-stmts/create-transform/) - 定义新的转换。
- [DROP TRANSFORM](/cloudberry/reference/sql-stmts/drop-transform/) - 删除转换。

## 触发器 {#trigger}

- [CREATE TRIGGER](/cloudberry/reference/sql-stmts/create-trigger/) - 定义新的触发器。
- [ALTER TRIGGER](/cloudberry/reference/sql-stmts/alter-trigger/) - 更改触发器的定义。
- [DROP TRIGGER](/cloudberry/reference/sql-stmts/drop-trigger/) - 删除触发器。

## 数据类型 {#data-type}

- [CREATE TYPE](/cloudberry/reference/sql-stmts/create-type/) - 定义新的数据类型。
- [ALTER TYPE](/cloudberry/reference/sql-stmts/alter-type/) - 更改数据类型的定义。
- [DROP TYPE](/cloudberry/reference/sql-stmts/drop-type/) - 删除数据类型。

## 事务 {#transaction}

- [BEGIN](/cloudberry/reference/sql-stmts/begin/) - 开始一个事务块。
- [ABORT](/cloudberry/reference/sql-stmts/abort/) - 终止当前事务。
- [COMMIT](/cloudberry/reference/sql-stmts/commit/) - 提交当前事务。
- [END](/cloudberry/reference/sql-stmts/end/) - 提交当前事务。
- [ROLLBACK](/cloudberry/reference/sql-stmts/rollback/) - 停止当前事务。
- [START TRANSACTION](/cloudberry/reference/sql-stmts/start-transaction/) - 启动事务块。
- [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/) - 设置当前事务的特性。
- [SAVEPOINT](/cloudberry/reference/sql-stmts/savepoint/) - 在当前事务中定义新的保存点。
- [RELEASE SAVEPOINT](/cloudberry/reference/sql-stmts/release-savepoint/) - 销毁先前定义的保存点。
- [ROLLBACK TO SAVEPOINT](/cloudberry/reference/sql-stmts/rollback-to-savepoint/) - 将当前事务回滚到保存点。
- [LOCK](/cloudberry/reference/sql-stmts/lock/) - 锁定表。
- [SET CONSTRAINTS](/cloudberry/reference/sql-stmts/set-constraints/) - 设置当前事务的约束检查时机。

## 配置参数 {#configuration-parameter}

- [SET](/cloudberry/reference/sql-stmts/set/) - 更改 Apache Cloudberry 运行时配置参数的值。
- [RESET](/cloudberry/reference/sql-stmts/reset/) - 将运行时系统配置参数的值恢复为默认值。
- [SHOW](/cloudberry/reference/sql-stmts/show/) - 显示运行时系统配置参数的值。

## SQL 语句 {#sql-statement}

- [PREPARE](/cloudberry/reference/sql-stmts/prepare/) - 准备要执行的语句。
- [DEALLOCATE](/cloudberry/reference/sql-stmts/deallocate/) - 释放预备语句。
- [EXECUTE](/cloudberry/reference/sql-stmts/execute/) - 执行预备 SQL 语句。
- [EXPLAIN](/cloudberry/reference/sql-stmts/explain/) - 显示语句的查询计划。
