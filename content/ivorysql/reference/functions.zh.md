---
title: PostgreSQL 函数参考手册
linkTitle: PG函数参考手册
description: IvorySQL v5.6 文档：PostgreSQL 函数参考手册。
type: docs
weight: 790
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/110.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---


## 1. PostgreSQL 函数参考手册 {#postgresql-函数参考手册}

### 1.1. current_catalog {#current_catalog}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>current_catalog</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得当前的database 名称。<br />
注意：在SQL标准中，databases被称之为catalogs。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select current_catalog;
 current_catalog
-----------------
 postgres
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.2. current_database() {#current_database}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>current_database()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得当前的database 名称。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select current_database();
 current_database
------------------
 postgres
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.3. current_query() {#current_query}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>current_query()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得client端提交的当前执行的SQL语句的文本</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=#   BEGIN;
BEGIN
postgres=*# select 1,current_query();
 ?column? |       current_query
----------+---------------------------
        1 | select 1,current_query();
(1 row)
&#10;postgres=*# select 2,current_query();
 ?column? |       current_query
----------+---------------------------
        2 | select 2,current_query();
(1 row)
&#10;postgres=*# ROLLBACK;
ROLLBACK
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.4. current_role {#current_role}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>current_role</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>与current_user作用相同，获得当前执行上下文的username</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select current_role;
 current_role
--------------
 pg131
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.5. current_schema {#current_schema}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>current_schema</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得search path中的第一个schema名称（当search path为空时，返回空值）。当表或者其他对象建立不带schema名称时，本函数返回的schema就是该表或者该对象的schema</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select current_schema;
 current_schema
----------------
 public
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.6. current_schema() {#current_schema-2}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>current_schema()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>作用与current_schema函数相同：获得search path中的第一个schema名称（当search path为空时，返回空值）。当表或者其他对象建立不带schema名称时，本函数返回的schema就是该表或者该对象的schema</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select current_schema();
 current_schema
----------------
 public
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.7. current_schemas(include_implicit boolean) {#current_schemasinclude_implicit-boolean}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>current_schemas(include_implicit boolean)</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>bool</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>以优先级顺序返回有效search_path中当前所有模式名称，如果入参为true，那么在函数返回结果中会包括隐式搜索的系统模式pg_catalog</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select current_schemas(false);
 current_schemas
-----------------
 {public}
(1 row)
&#10;postgres=# select current_schemas(true);
   current_schemas
---------------------
 {pg_catalog,public}
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.8. current_user {#current_user}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>current_user</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得当前执行上下文的username</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select current_user;
 current_user
--------------
 pg131
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.9. inet_client_addr() {#inet_client_addr}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>inet_client_addr()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得当前client的ip地址。如果返回值为空，表示当前连接是经过Unix-domain socket的</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select inet_client_addr();
 inet_client_addr
------------------
&#10;(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.10. inet_client_port() {#inet_client_port}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>inet_client_port()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得当前client的端口号。如果返回值为空，表示当前连接是经过Unix-domain socket的</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select inet_client_port();
 inet_client_port
------------------
&#10;(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.11. inet_server_addr() {#inet_server_addr}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>inet_server_addr()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得当前连接的pg数据库服务器的ip地址。如果返回值为空，表示当前连接是经过Unix-domain socket的。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select inet_server_port();
 inet_server_port
------------------
&#10;(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.12. inet_server_port() {#inet_server_port}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>inet_server_port()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得当前连接的pg数据库服务器的端口号。如果返回值为空，表示当前连接是经过Unix-domain socket的。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select inet_server_port();
 inet_server_port
------------------
&#10;(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.13. pg_backend_pid() {#pg_backend_pid}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_backend_pid()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得附加到当前session的backend进程的进程ID</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_backend_pid();
 pg_backend_pid
----------------
           4068
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.14. pg_blocking_pids(integer) {#pg_blocking_pidsinteger}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_blocking_pids(integer)</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Integer[]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回入参pid的blocking pid(即:阻塞者pid)若是本函数返回空值，表示不存在阻塞者若是本函数返回值是零，那么表示阻塞者是prepared transacion，见下面的输出：</p>
<pre class="sql"><code>postgres=# select pg_blocking_pids(12947); pg_blocking_pids
------------------
{0}
(1 row)
 postgres=#</code></pre>
<p>频繁调用本函数会对数据库性能有影响，因为本函数在短时间内对lock manager’s shared state进行排他访问(exclusive accesss)</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>Session1：
postgres=# SELECT pg_backend_pid();
 pg_backend_pid
----------------
          32262
(1 row)
&#10;postgres=# CREATE TABLE tbl_students(rno int, name character varying(10));
CREATE TABLE
postgres=# BEGIN TRANSACTION;
BEGIN
postgres=*# LOCK tbl_students IN ACCESS EXCLUSIVE MODE;
LOCK TABLE
postgres=*#
&#10;
session2：
postgres=# SELECT pg_backend_pid();
 pg_backend_pid
----------------
          32439
(1 row)
&#10;postgres=# INSERT INTO tbl_students VALUES (1,&#39;Anvesh&#39;);
&#10;
session3:
postgres=# SELECT pg_blocking_pids(32439);
 pg_blocking_pids
------------------
 {32262}
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.15. pg_conf_load_time() {#pg_conf_load_time}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_conf_load_time()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>timestamp with time zone</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回PG配置参数文件最后一次被reload的时间</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_conf_load_time();
       pg_conf_load_time
-------------------------------
 2021-03-22 12:46:18.962643+08
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.16. pg_current_logfile(&#91;text&#93;); {#pg_current_logfiletext}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_current_logfile([text]);</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数或者text型输入参数 (csvlog、stderr)</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回正在被logging collector进程使用的log file的path(是log_directory的值)和文件名。当logging collector是被禁用时，本函数返回结果是null。当有不同格式的多种log files存在时，不带任何参数的pg_current_logfile()函数返回有序列表(stderr、csvlog)中找到的第一种格式的文件path和文件名。当没有这两个格式的文件时，本函数返回NULL</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_current_logfile();
          pg_current_logfile
--------------------------------------
 log/postgresql-2021-03-22_124618.log
(1 row)
&#10;postgres=# select pg_current_logfile(&#39;stderr&#39;);
          pg_current_logfile
--------------------------------------
 log/postgresql-2021-03-22_124618.log
(1 row)
&#10;postgres=# select pg_current_logfile(&#39;csvlog&#39;);
 pg_current_logfile
--------------------
&#10;(1 row)
&#10;postgres=# show log_destination ;
 log_destination
-----------------
 stderr
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.17. pg_my_temp_schema() {#pg_my_temp_schema}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_my_temp_schema()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回当前会话的临时schema的OID，如果没有临时schema，本函数返回0（即：数字零）</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_my_temp_schema();
 pg_my_temp_schema
-------------------
 0
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.18. pg_is_other_temp_schema(oid) {#pg_is_other_temp_schemaoid}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_is_other_temp_schema(oid)</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>当入参的oid是其他session中临时schema的oid时，本函数返回true。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_is_other_temp_schema(16426);
 pg_is_other_temp_schema
-------------------------
 f
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.19. pg_jit_available() {#pg_jit_available}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_jit_available()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>如果jit编译器扩展是可用的并且jit配置参数设置为on的话，本函数返回true</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_jit_available();
 pg_jit_available
------------------
 f
(1 row)
&#10;postgres=# select * from pg_config where name=&#39;CONFIGURE&#39; AND SETTING LIKE &#39;%--with-llvm%&#39;;
 name | setting
------+---------
(0 rows)
&#10;postgres=# show jit;
 jit
-----
 on
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.20. pg_listening_channels() {#pg_listening_channels}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_listening_channels()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>setof text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>当前session正在监听的异步通知通道的名称</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_listening_channels();
 pg_listening_channels
-----------------------
(0 rows)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.21. pg_notification_queue_usage() {#pg_notification_queue_usage}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_notification_queue_usage()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>double precision</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回被正在等待处理的通知占据的异步通知队列最大大小的比例。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_notification_queue_usage();
 pg_notification_queue_usage
-----------------------------
                           0
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.22. pg_postmaster_start_time() {#pg_postmaster_start_time}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_postmaster_start_time()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>timestamp with time zone</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回PG intance 启动的时间点</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_postmaster_start_time();
   pg_postmaster_start_time
-------------------------------
 2021-03-23 14:01:33.352011+08
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.23. pg_safe_snapshot_blocking_pids(integer) {#pg_safe_snapshot_blocking_pidsinteger}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_safe_snapshot_blocking_pids(integer)</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>integer[]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回阻止指定服务器进程ID获取安全快照的进程ID若是没有阻塞，则返回空array。一个运行SERIALIZABLE事务的session阻塞了一个SERIALIZABLE READ ONLY DEFERRABLE事务，防止后者获得snapshot，直到后者确认可以安全的避免获取任何谓词锁。频繁调用本函数会对数据库性能有影响，因为它在短时间内需要访问谓词锁管理器的共享状态(predicate lock manager’s shared state)</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_safe_snapshot_blocking_pids(1234);
 pg_safe_snapshot_blocking_pids
--------------------------------
 {}
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.24. pg_trigger_depth() {#pg_trigger_depth}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_trigger_depth()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回PostgreSQL触发器的当前嵌套级别(如果没有从触发器内部直接或间接调用，则为返回值为0)</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_trigger_depth();
 pg_trigger_depth
------------------
                0
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.25. user {#user}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>user</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得当前执行上下文的username，等同于current_user函数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select user;
 user
-------
 pg131
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.26. Version() {#version}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>Version()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回带有数据库版本号的字符串，您也可以查询server_version配置参数获得数据库版本号。对于机器可读的版本，请使用server_version_num配置参数。在软件开发过程中应该使用server_version_num配置参数或者PqserverVersion，而不是去解析文本的版本号(见下面的使用举例)</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select version();
                                                 version
---------------------------------------------------------------------------------------------------------
 PostgreSQL 13.1 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-44), 64-bit
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.27. has_any_column_privilege(user, table, privilege) {#has_any_column_privilegeuser-table-privilege}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>has_any_column_privilege(user, table, privilege)</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, table, privilege或者table, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>确定一个user是否对当前PG database中的某个table任一列有列权限确定当前user是否对当前PG database中的某个table任一列有列权限权限类型是SELECT, INSERT, UPDATE,REFERENCES的组合。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>[pg131@VM-0-8-centos ~]$ psql -d cwbase3 -U lc0039999
psql (13.1)
Type &quot;help&quot; for help.
&#10;cwbase3=&gt; \d
         List of relations
 Schema | Name  | Type  |   Owner
--------+-------+-------+-----------
 public | test1 | table | lc0039999
(1 row)
&#10;cwbase3=&gt; select has_any_column_privilege(&#39;lc0039999&#39;,&#39;test1&#39;,&#39;select&#39;);
 has_any_column_privilege
--------------------------
 t
(1 row)
&#10;cwbase3=&gt;
cwbase3=&gt; select has_any_column_privilege(&#39;test1&#39;,&#39;select,insert&#39;);
 has_any_column_privilege
--------------------------
 t
(1 row)
&#10;cwbase3=&gt;
&#10;cwbase3=&gt; select has_any_column_privilege(&#39;test1&#39;,&#39;select&#39;);
 has_any_column_privilege
--------------------------
 t
(1 row)
&#10;cwbase3=&gt;</code></pre></td>
</tr>
</tbody>
</table>

### 1.28. has_column_privilege(user, table, column, privilege) {#has_column_privilegeuser-table-column-privilege}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>has_column_privilege(user, table, column, privilege);</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, table, column, privilege或者table, column, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>特定user对特定表的某一列是否具有某种权限当前user对特定表的某一列是否具有某种权限权限类型是SELECT, INSERT, UPDATE,REFERENCES的组合。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>cwbase3=&gt; \d test1
               Table &quot;public.test1&quot;
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 id     | integer |           |          |
&#10;cwbase3=&gt;
cwbase3=&gt; select has_column_privilege(&#39;lc0039999&#39;,&#39;test1&#39;,&#39;id&#39;,&#39;select&#39;);
 has_column_privilege
----------------------
 t
(1 row)
&#10;cwbase3=&gt;
cwbase3=&gt; select has_column_privilege(&#39;test1&#39;,&#39;id&#39;,&#39;select&#39;);
 has_column_privilege
----------------------
 t
(1 row)
&#10;cwbase3=&gt;</code></pre></td>
</tr>
</tbody>
</table>

### 1.29. has_database_privilege {#has_database_privilege}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>has_database_privilege</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, database, privilege或者database, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>特定user是否对特定database有某种权限当前user是否对特定database有某种权限权限类型是CREATE, CONNECT, TEMPORARY, or TEMP的组合。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select has_database_privilege(&#39;lc0039999&#39;,&#39;cwbase3&#39;,&#39;create,connect,temp&#39;);
 has_database_privilege
------------------------
 t
(1 row)
&#10;postgres=# select has_database_privilege(&#39;lc0019999&#39;,&#39;cwbase3&#39;,&#39;create,connect,temp&#39;);
 has_database_privilege
------------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.30. has_foreign_data_wrapper_privilege {#has_foreign_data_wrapper_privilege}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>has_foreign_data_wrapper_privilege</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, fdw, privilege或者fdw, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>特定user是否对特定fdw有usage权限当前user是否对特定fdw有usage权限此处的权限只能指定usage</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select  has_foreign_data_wrapper_privilege(&#39;lc0019999&#39;,&#39;file_fdw&#39;,&#39;usage&#39;);
 has_foreign_data_wrapper_privilege
------------------------------------
 f
(1 row)
&#10;postgres=#
postgres=# select  has_foreign_data_wrapper_privilege(&#39;file_fdw&#39;,&#39;usage&#39;);
 has_foreign_data_wrapper_privilege
------------------------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.31. has_function_privilege {#has_function_privilege}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>has_function_privilege</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, function, privilege或者function, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>特定user是否对特定function有EXECUTE权限当前user是否对特定function有EXECUTE权限此处的权限只能是EXECUTE</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select has_function_privilege(&#39;lc0039999&#39;,&#39;version()&#39;,&#39;execute&#39;);
has_function_privilege
------------------------
t
(1 row)
 postgres=# postgres=# select has_function_privilege(&#39;version()&#39;,&#39;execute&#39;);
 has_function_privilege
 ------------------------
 t
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.32. has_language_privilege {#has_language_privilege}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>has_language_privilege</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, language, privilege或者language, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>特定user是否对特定procedural language有usage权限当前user是否对特定procedural language有usage权限此处的权限必须是usage</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select has_language_privilege(&#39;lc0019999&#39;,&#39;sql&#39;,&#39;usage&#39;);
has_language_privilege
------------------------
t
(1 row)
 postgres=# select has_language_privilege(&#39;plpgsql&#39;,&#39;usage&#39;);
 has_language_privilege
  ------------------------
   t
   (1 row)
 postgres=#</code></pre>
<p>注意：此处的language可以从pg_language系统表查询到。</p></td>
</tr>
</tbody>
</table>

### 1.33. has_schema_privilege {#has_schema_privilege}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>has_schema_privilege</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, schema, privilege或者schema, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>特定user是否对特定schema有usage或者create权限当前user是否对特定schema有usage或者create权限此处的权限必须是create或者usage的组合</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# \dnS
      List of schemas
        Name        | Owner
--------------------+-------
 information_schema | pg131
 pg_catalog         | pg131
 pg_toast           | pg131
 public             | pg131
 s_abc              | pg131
(5 rows)
&#10;postgres=# select has_schema_privilege(&#39;lc0019999&#39;,&#39;s_abc&#39;,&#39;usage&#39;);
 has_schema_privilege
----------------------
 f
(1 row)
&#10;postgres=# select has_schema_privilege(&#39;lc0019999&#39;,&#39;s_abc&#39;,&#39;usage,create&#39;);
 has_schema_privilege
----------------------
 f
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.34. has_sequence_privilege {#has_sequence_privilege}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>has_sequence_privilege</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, sequence, privilege或者sequence, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>特定user是否对特定sequence有特定权限当前user是否对特定sequence有特定权限此处的权限是USAGE, SELECT, UPDATE的组合。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# \ds+
                                 List of relations
 Schema |     Name     |   Type   | Owner | Persistence |    Size    | Description
--------+--------------+----------+-------+-------------+------------+-------------
 public | gen_y_c1_seq | sequence | pg131 | permanent   | 8192 bytes |
(1 row)
&#10;postgres=# select has_sequence_privilege(&#39;pg131&#39;,&#39;gen_y_c1_seq&#39;,&#39;usage&#39;);
 has_sequence_privilege
------------------------
 t
(1 row)
&#10;postgres=# select has_sequence_privilege(&#39;lc0039999&#39;,&#39;gen_y_c1_seq&#39;,&#39;usage&#39;);
 has_sequence_privilege
------------------------
 f
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.35. has_server_privilege {#has_server_privilege}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>has_server_privilege</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, server, privilege或者server, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>特定user是否对特定foreign server有usage权限特定user是否对特定foreign server有usage权限此处的权限必须是usage</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select has_server_privilege(&#39;s1&#39;,&#39;usage&#39;);
has_server_privilege
----------------------
t
(1 row)
postgres=# select has_server_privilege(&#39;s1&#39;,&#39;USAGE&#39;);
has_server_privilege
----------------------
t
(1 row)
postgres=# select has_server_privilege(&#39;pg123&#39;,&#39;s1&#39;,&#39;USAGE&#39;);
has_server_privilege
----------------------
t
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.36. has_table_privilege {#has_table_privilege}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>has_table_privilege</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, table, privilege或者table, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>特定user是否对特定table有特定权限当前user是否对特定table有特定权限此处的权限是指如下的组合： SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER，还可以带有WITH GRANT OPTION用来测试privilege是否带有grant option。当权限字符串有多个值(比如’insert, select')时,只要有任何一个权限是满足的，本函数会返回t有关对权限字符串的说明：权限字符串不区分大小写权限字符串的前后可以有一个或者多个空格（权限名字内部不能有空格）</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select has_table_privilege(&#39;t1&#39;,&#39;  select,  insert &#39;);
 has_table_privilege
---------------------
 t
(1 row)
&#10;postgres=#
[pg131@VM-0-8-centos ~]$ psql -d cwbase3 -U lc0039999
psql (13.1)
Type &quot;help&quot; for help.
&#10;cwbase3=&gt;
cwbase3=&gt; grant select on test1 to lc0019999;
GRANT
cwbase3=&gt; exit
[pg131@VM-0-8-centos ~]$ psql -d cwbase3 -U lc0019999
psql (13.1)
Type &quot;help&quot; for help.
&#10;cwbase3=&gt; select * from test1;
 id
 ----
  1
  2
  3
&#10;  4
  5
(6 rows)
&#10;cwbase3=&gt; select has_table_privilege(&#39;test1&#39;,&#39;insert, select &#39;);
 has_table_privilege
---------------------
 t
(1 row)
&#10;cwbase3=&gt; select has_table_privilege(&#39;test1&#39;,&#39;insert&#39;);
 has_table_privilege
---------------------
 f
(1 row)
&#10;cwbase3=&gt; select has_table_privilege(&#39;test1&#39;,&#39; insert &#39;);
 has_table_privilege
---------------------
 f
(1 row)
&#10;cwbase3=&gt; insert into test1 values(6);
ERROR:  permission denied for table test1
cwbase3=&gt;</code></pre></td>
</tr>
</tbody>
</table>

### 1.37. has_tablespace_privilege {#has_tablespace_privilege}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>has_tablespace_privilege</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, tablespace, privilege或者tablespace, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>特定user是否对特定tablesapce有特定权限当前user是否对特定tablespace有特定权限此处的权限必须是create</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select has_tablespace_privilege(&#39;ts1&#39;,&#39;create &#39;);
has_tablespace_privilege
--------------------------
t
(1 row)
postgres=# select has_tablespace_privilege(&#39;lc0019999&#39;,&#39;ts1&#39;,&#39;create &#39;);
has_tablespace_privilege
--------------------------
f
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.38. has_type_privilege {#has_type_privilege}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>has_type_privilege</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, type, privilege或者type, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>特定user是否对特定type有特定权限当前user是否对特定type有特定权限特定type可以使用type的name，也可以使用oid::regtype的形式此处的权限必须是USAGE</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select has_type_privilege(&#39;bytea&#39;,&#39;usage&#39;);
has_type_privilege
--------------------
t
(1 row)
postgres=# select has_type_privilege(&#39;lc0019999&#39;,&#39;bytea&#39;,&#39;usage&#39;);
has_type_privilege
--------------------
t
(1 row)
postgres=# select has_type_privilege(&#39;lc0019999&#39;,&#39;17:regtype&#39;,&#39;usage&#39;);
ERROR: syntax error at or near &quot;17&quot;
CONTEXT: invalid type name &quot;17:regtype&quot;
postgres=# select has_type_privilege(&#39;lc0019999&#39;,17::regtype,&#39;usage&#39;);
has_type_privilege
--------------------
t
(1 row)
postgres=# select has_type_privilege(&#39;lc0019999&#39;,&#39;17::regtype&#39;,&#39;usage&#39;);
ERROR: syntax error at or near &quot;17&quot;
CONTEXT: invalid type name &quot;17::regtype&quot;
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.39. pg_has_role {#pg_has_role}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_has_role</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>user, role, privilege或者role, privilege</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>特定user是否对特定role group有特定权限当前user是否对特定role group有特定权限此处的权限必须是member或者usage当权限是member时，表示特定user是否是特定role group的member当权限是usage时，表示在不执行set role时，特定user是否有特定role的权限</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# create role editors;
CREATE ROLE
postgres=# create user maxwell;
CREATE ROLE
postgres=# create user ernest;
CREATE ROLE
postgres=# grant authors to editors; --editors can do what authors can do
GRANT ROLE
postgres=# grant editors to maxwell; --maxwell is an editor
GRANT ROLE
postgres=# grant authors to ernest; --ernest is an author
GRANT ROLE
postgres=# select pg_has_role(&#39;maxwll&#39;,&#39;editors&#39;,&#39;member&#39;);
ERROR:  role &quot;maxwll&quot; does not exist
postgres=# select pg_has_role(&#39;maxwell&#39;,&#39;editors&#39;,&#39;member&#39;);
 pg_has_role
-------------
 t
(1 row)
&#10;postgres=# select pg_has_role(&#39;maxwell&#39;,&#39;editors&#39;,&#39;usage&#39;);
 pg_has_role
-------------
 t
(1 row)
&#10;postgres=# select pg_has_role(&#39;maxwell&#39;,&#39;ernest&#39;,&#39;usage&#39;);
 pg_has_role
-------------
 f
(1 row)
&#10;postgres=# select pg_has_role(&#39;maxwell&#39;,&#39;ernest&#39;,&#39;member&#39;);
 pg_has_role
-------------
 f
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.40. row_security_active {#row_security_active}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>row_security_active</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Table，可以是table name，也可以是table的oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在current_user的上下文中，特定table是否已开启row security</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid from pg_class where relname=&#39;test&#39;;
  oid
-------
 16860
(1 row)
&#10;postgres=# select row_security_active(&#39;test&#39;);
 row_security_active
---------------------
 f
(1 row)
&#10;postgres=# select row_security_active(16860);
 row_security_active
---------------------
 f
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.41. acldefault {#acldefault}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>acldefault</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>type, ownerId</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>aclitem[]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回属于某个user oid对象的默认访问权限。当一个对象的ACL条目为null时这些访问权限是该对象的默认权限Type参数的取值如下：'c' for COLUMN’r' for TABLE 以及类似对象’s' for SEQUENCE’d' for DATABASE’f' for FUNCTION 或者PROCEDURE’l' for LANGUAGE’L' for LARGE OBJECT’n' for SCHEMA’t' for TABLESPACE’F' for FOREIGN DATA WRAPPER’S' for FOREIGN SERVER’T' for TYPE or DOMAIN</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select acldefault(&#39;f&#39;,16877);
acldefault
--------------------------------------
{=X/lc0039999,lc0039999=X/lc0039999}
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.42. aclexplode {#aclexplode}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>aclexplode</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>aclitem[]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>setof record</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>解析 acl 权限</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select aclexplode(&#39;{=X/lc0039999,lc0039999=X/lc0039999}&#39;);
 aclexplode
-------------------------
 (16877,0,EXECUTE,f)
 (16877,16877,EXECUTE,f)
 (2 rows)
postgres=# postgres=# select \* from aclexplode(&#39;{=X/lc0039999,lc0039999=X/lc0039999}&#39;);
 grantor | grantee | privilege_type | is_grantable
---------+---------+----------------+--------------
 16877 | 0 | EXECUTE | f
 16877 | 16877 | EXECUTE | f
(2 rows)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.43. makeaclitem {#makeaclitem}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>makeaclitem</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>grantee, grantor, privilege, grantable</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>aclitem</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>构建aclitem</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select \* from makeaclitem(16877,16877,&#39;EXECUTE&#39;,false);
makeaclitem
-----------------------
lc0039999=X/lc0039999
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.44. pg_collation_is_visible {#pg_collation_is_visible}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_collation_is_visible</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>collation_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在当前schema search path中，特定collation是否可见。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select * from pg_collation where collname = &#39;zh_CN&#39;;
  oid  | collname | collnamespace | collowner | collprovider | collisdeterministic | collencoding | collcollate | collctype  | collversion
-------+----------+---------------+-----------+--------------+---------------------+--------------+-------------+------------+-------------
 13086 | zh_CN    |            11 |        10 | c            | t                   |            2 | zh_CN       | zh_CN      | 2.17
 13243 | zh_CN    |            11 |        10 | c            | t                   |            6 | zh_CN.utf8  | zh_CN.utf8 | 2.17
(2 rows)
&#10;postgres=# select  pg_collation_is_visible(13086);
 pg_collation_is_visible
-------------------------
 f
(1 row)
&#10;postgres=# select  pg_collation_is_visible(13243);
 pg_collation_is_visible
-------------------------
 t
(1 row)
&#10;postgres=#
postgres=# select  pg_collation_is_visible(&#39;&quot;zh_CN&quot;&#39;::regcollation);
 pg_collation_is_visible
-------------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.45. pg_conversion_is_visible {#pg_conversion_is_visible}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_conversion_is_visible</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>conversion_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在当前schema search path中，特定conversion是否可见</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select *  from pg_conversion  where conname like &#39;%cn%&#39;;
 oid  |    conname     | connamespace | conowner | conforencoding | contoencoding |    conproc     | condefault
------+----------------+--------------+----------+----------------+---------------+----------------+------------
 4422 | euc_cn_to_mic  |           11 |       10 |              2 |             7 | euc_cn_to_mic  | t
 4423 | mic_to_euc_cn  |           11 |       10 |              7 |             2 | mic_to_euc_cn  | t
 4480 | euc_cn_to_utf8 |           11 |       10 |              2 |             6 | euc_cn_to_utf8 | t
 4481 | utf8_to_euc_cn |           11 |       10 |              6 |             2 | utf8_to_euc_cn | t
(4 rows)
&#10;postgres=# select pg_conversion_is_visible(4480);
 pg_conversion_is_visible
--------------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.46. pg_function_is_visible {#pg_function_is_visible}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_function_is_visible</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>function_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在当前schema search path中，特定function、procedures、aggregates是否可见。对于函数，如果路径前面没有相同名称和参数数据类型的对象，则搜索路径中的对象可见</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid from pg_proc where proname=&#39;version&#39;;
 oid
-----
  89
(1 row)
&#10;postgres=# select pg_function_is_visible(89);
 pg_function_is_visible
------------------------
 t
(1 row)
&#10;postgres=#
postgres=# select pg_function_is_visible(&#39;version&#39;::regproc);
 pg_function_is_visible
------------------------
 t
(1 row)
&#10;postgres=# select pg_function_is_visible(&#39;version()&#39;::regprocedure);
 pg_function_is_visible
------------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.47. pg_opclass_is_visible {#pg_opclass_is_visible}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_opclass_is_visible</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>opclass_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在当前schema search path中，特定operator class是否可见考虑因素是operator class name和相关的索引访问方法。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid from pg_opclass where opcname=&#39;array_ops&#39;;
  oid
-------
 10000
 10001
 10063
(3 rows)
&#10;postgres=# select pg_opclass_is_visible(10000);
 pg_opclass_is_visible
-----------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.48. pg_operator_is_visible {#pg_operator_is_visible}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_operator_is_visible</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>operator_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在当前schema search path中，特定operator 是否可见对于运算符，如果路径前面没有相同名称和参数数据类型的对象，则搜索路径中的对象可见</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oprname from pg_operator where oid=15;
 oprname
---------
 =
(1 row)
&#10;postgres=# select pg_operator_is_visible(15);
 pg_operator_is_visible
------------------------
 t
(1 row)
&#10;postgres=#
postgres=#  select pg_operator_is_visible(&#39;=(integer,integer)&#39;::regoperator);
 pg_operator_is_visible
------------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.49. pg_opfamily_is_visible {#pg_opfamily_is_visible}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_opfamily_is_visible</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>opclass_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在当前schema search path中，特定operator family是否可见</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select *  from pg_opfamily where oid=&#39;397&#39;;
 oid | opfmethod |  opfname  | opfnamespace | opfowner
-----+-----------+-----------+--------------+----------
 397 |       403 | array_ops |           11 |       10
(1 row)
&#10;postgres=# select pg_opfamily_is_visible(397);
 pg_opfamily_is_visible
------------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.50. pg_statistics_obj_is_visible {#pg_statistics_obj_is_visible}

|                    |                                                        |
|--------------------|--------------------------------------------------------|
| 函数名称           | pg_statistics_obj_is_visible                           |
| 参数数据类型       | stat_oid                                               |
| 函数返回值数据类型 | boolean                                                |
| 函数含义           | 在当前schema search path中，特定operator class是否可见 |
| 使用举例           |                                                        |

### 1.51. pg_table_is_visible {#pg_table_is_visible}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_table_is_visible</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>table_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在当前schema search path中，特定的table、views、materialized views、 indexes、 sequences、foreign tables是否可见</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid from pg_class where relname=&#39;data1&#39;;
  oid
-------
 16384
(1 row)
&#10;postgres=# select pg_table_is_visible(16384);
 pg_table_is_visible
---------------------
 t
(1 row)
&#10;postgres=#
postgres=# SELECT pg_table_is_visible(&#39;public.data1&#39;::regclass);
 pg_table_is_visible
---------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.52. pg_ts_config_is_visible {#pg_ts_config_is_visible}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_ts_config_is_visible</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>config_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在当前schema search path中，特定text search configuration是否可见</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid from pg_ts_config where cfgname=&#39;greek&#39;;
  oid
-------
 13861
(1 row)
&#10;postgres=# select pg_ts_config_is_visible(13861);
 pg_ts_config_is_visible
-------------------------
 t
(1 row)
&#10;postgres=#
postgres=# select pg_ts_config_is_visible(&#39;greek&#39;::regconfig);
 pg_ts_config_is_visible
-------------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.53. pg_ts_dict_is_visible {#pg_ts_dict_is_visible}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_ts_dict_is_visible</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p><em>dict_oid</em></p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在当前schema search path中，特定text search dictionary是否可见</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid,dictname,dictinitoption from pg_ts_dict where dictname=&#39;greek_stem&#39;;
  oid  |  dictname  |   dictinitoption
-------+------------+--------------------
 13860 | greek_stem | language = &#39;greek&#39;
(1 row)
&#10;postgres=# select pg_ts_dict_is_visible(13860);
 pg_ts_dict_is_visible
-----------------------
 t
(1 row)
&#10;postgres=#
postgres=#  select pg_ts_dict_is_visible(&#39;greek_stem&#39;::regdictionary);
 pg_ts_dict_is_visible
-----------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.54. pg_ts_parser_is_visible {#pg_ts_parser_is_visible}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_ts_parser_is_visible</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>parser_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在当前schema search path中，特定text search parser是否可见</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select * from pg_ts_parser ;
 oid  | prsname | prsnamespace |  prsstart  |    prstoken    |  prsend  |  prsheadline  |  prslextype
------+---------+--------------+------------+----------------+----------+---------------+--------------
 3722 | default |           11 | prsd_start | prsd_nexttoken | prsd_end | prsd_headline | prsd_lextype
(1 row)
&#10;postgres=# select pg_ts_parser_is_visible(3722);
 pg_ts_parser_is_visible
-------------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.55. pg_ts_template_is_visible {#pg_ts_template_is_visible}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_ts_template_is_visible</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>template_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在当前schema search path中，特定text search template是否可见</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select * from pg_ts_template ;
  oid  | tmplname  | tmplnamespace |    tmplinit    |    tmpllexize
-------+-----------+---------------+----------------+------------------
  3727 | simple    |            11 | dsimple_init   | dsimple_lexize
  3730 | synonym   |            11 | dsynonym_init  | dsynonym_lexize
  3733 | ispell    |            11 | dispell_init   | dispell_lexize
  3742 | thesaurus |            11 | thesaurus_init | thesaurus_lexize
 13845 | snowball  |            11 | dsnowball_init | dsnowball_lexize
(5 rows)
&#10;postgres=# select pg_ts_temp
&#10;postgres=# select pg_ts_template_is_visible(3730);
 pg_ts_template_is_visible
---------------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.56. pg_type_is_visible {#pg_type_is_visible}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_type_is_visible</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>type_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>在当前schema search path中，特定type、domain是否可见</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid,typname from pg_type where typname=&#39;bool&#39;;
 oid | typname
-----+---------
  16 | bool
(1 row)
&#10;postgres=# select pg_type_is_visible(16);
 pg_type_is_visible
--------------------
 t
(1 row)
&#10;postgres=#
postgres=# SELECT pg_type_is_visible(&#39;pg_catalog.bool&#39;::regtype);
 pg_type_is_visible
--------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.57. format_type {#format_type}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>format_type</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>type_oid, typemod</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>得到一个data type的SQL Name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select * from pg_type where typname=&#39;bool&#39;;
-[ RECORD 1 ]--+---------
oid            | 16
typname        | bool
typnamespace   | 11
typowner       | 10
typlen         | 1
typbyval       | t
typtype        | b
typcategory    | B
typispreferred | t
typisdefined   | t
typdelim       | ,
typrelid       | 0
typelem        | 0
typarray       | 1000
typinput       | boolin
typoutput      | boolout
typreceive     | boolrecv
typsend        | boolsend
typmodin       | -
typmodout      | -
typanalyze     | -
typalign       | c
typstorage     | p
typnotnull     | f
typbasetype    | 0
typtypmod      | -1
typndims       | 0
typcollation   | 0
typdefaultbin  |
typdefault     |
typacl         |
&#10;postgres=#
postgres=# select format_type(16,0);
 format_type
-------------
 boolean
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.58. pg_get_constraintdef {#pg_get_constraintdef}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_constraintdef</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>constraint_oid或者constraint_oid, pretty_bool</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>得到一个constraint的定义</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_get_constraintdef(16918);
pg_get_constraintdef
----------------------
PRIMARY KEY (c1)
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.59. pg_get_expr {#pg_get_expr}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_expr</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>pg_node_tree, relation_oid,或者<br />
pg_node_tree, relation_oid, pretty_bool</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>反编译指定expression的内部格式，假设：其中的任何变量引用第二个参数指示的relation</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# CREATE TABLE tab1 (a int, b int) PARTITION BY RANGE(a);
CREATE TABLE
postgres=# CREATE TABLE tab1_p1 PARTITION OF tab1 FOR VALUES FROM (0) TO (100);
CREATE TABLE
postgres=# CREATE TABLE tab1_p2 PARTITION OF tab1 FOR VALUES FROM (100) TO (200);
CREATE TABLE
postgres=# select relname, pg_get_expr(relpartbound, oid) from pg_class where relispartition and relname ~ &#39;tab1&#39; order by relname;
 relname |          pg_get_expr
---------+--------------------------------
 tab1_p1 | FOR VALUES FROM (0) TO (100)
 tab1_p2 | FOR VALUES FROM (100) TO (200)
(2 rows)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.60. pg_get_functiondef {#pg_get_functiondef}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_functiondef</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>func_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得function或者procedure的定义<br />
<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_get_functiondef(89);
pg_get_functiondef
-------------------------------------------------
CREATE OR REPLACE FUNCTION pg_catalog.version()+ RETURNS text + LANGUAGE internal + STABLE PARALLEL SAFE STRICT + AS $function$pgsql_version$function$
&#10;(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.61. pg_get_function_arguments {#pg_get_function_arguments}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_function_arguments</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>func_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得function或者procedure的传入参数清单<br />
<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid from pg_proc where proname=&#39;has_database_privilege&#39;;
-[ RECORD 1 ]
oid | 2250
-[ RECORD 2 ]
oid | 2251
-[ RECORD 3 ]
oid | 2252
-[ RECORD 4 ]
oid | 2253
-[ RECORD 5 ]
oid | 2254
-[ RECORD 6 ]
oid | 2255
&#10;postgres=# select pg_get_function_arguments(2250);
-[ RECORD 1 ]-------------+-----------------
pg_get_function_arguments | name, text, text
&#10;postgres=# \x
Expanded display is off.
postgres=# select pg_get_function_arguments(2250);
 pg_get_function_arguments
---------------------------
 name, text, text
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.62. pg_get_function_identity_arguments {#pg_get_function_identity_arguments}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_function_identity_arguments</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>func_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得参数清单以标识出function或者procedure<br />
<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_get_function_identity_arguments(2250);
pg_get_function_identity_arguments ------------------------------------
name, text, text
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.63. pg_get_function_result {#pg_get_function_result}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_function_result</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>func_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得function，若是procedure，返回null</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_get_function_result(89);
pg_get_function_result
------------------------
text
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.64. pg_get_indexdef {#pg_get_indexdef}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_indexdef</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>index_oid或者index_oid, column_no, pretty_bool</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得索引的定义语句获得某个索引上第n个索引列的名称</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid from pg_class where relname=&#39;idx_2&#39;;
  oid
-------
 16427
(1 row)
&#10;postgres=# select pg_get_indexdef(16427);
                     pg_get_indexdef
---------------------------------------------------------
 CREATE INDEX idx_2 ON public.data1 USING btree (c1, c3)
(1 row)
&#10;postgres=#
&#10;postgres=# select pg_get_indexdef(16427,2,true);
 pg_get_indexdef
-----------------
 c3
(1 row)
&#10;postgres=# select pg_get_indexdef(16427,1,true);
 pg_get_indexdef
-----------------
 c1
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.65. pg_get_keywords {#pg_get_keywords}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_keywords</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>setof record</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回PostgreSQL数据库中的SQL关键字清单返回结果中有3列(以逗号分隔)，第一列是关键字名称，第二列catcode是category code U for unreserved C for column name T for type or function name R for reserved第三列catdesc是描述</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_get_keywords();
pg_get_keywords
------------------------------------------------------------------
 (abort,U,unreserved)
 (absolute,U,unreserved)
 (access,U,unreserved)
 (action,U,unreserved)
 (add,U,unreserved)
 (admin,U,unreserved)
 (after,U,unreserved)
 (aggregate,U,unreserved)
 (all,R,reserved)
 (also,U,unreserved)
 (alter,U,unreserved)
 (always,U,unreserved)
 (analyse,R,reserved)
 (analyze,R,reserved)
 (and,R,reserved)
限于篇幅，本函数的输出仅摘录到此处</code></pre></td>
</tr>
</tbody>
</table>

### 1.66. pg_get_ruledef {#pg_get_ruledef}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_ruledef</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>rule_oid或者rule_oid, pretty_bool</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得rule的create rule语句</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid ,rulename from pg_rewrite where rulename=&#39;pg_settings_u&#39;;
  oid  |   rulename
-------+---------------
 12168 | pg_settings_u
(1 row)
&#10;postgres=# select pg_get_ruledef(12168);
                                          pg_get_ruledef
---------------------------------------------------------------------------------------------------
 CREATE RULE pg_settings_u AS                                                                     +
     ON UPDATE TO pg_catalog.pg_settings                                                          +
    WHERE (new.name = old.name) DO  SELECT set_config(old.name, new.setting, false) AS set_config;
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.67. pg_get_serial_sequence {#pg_get_serial_sequence}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_serial_sequence</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>table_name, column_name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得自增列或者标识列使用的sequence的name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_get_serial_sequence(&#39;gen_y&#39;,&#39;c1&#39;);
pg_get_serial_sequence
------------------------
public.gen_y_c1_seq
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.68. pg_get_statisticsobjdef {#pg_get_statisticsobjdef}

|  |  |
|----|----|
| 函数名称 | pg_get_statisticsobjdef |
| 参数数据类型 | statobj_oid |
| 函数返回值数据类型 | text |
| 函数含义 | 获得extended statistics object的CREATE STATISTICS语句。 |
| 使用举例 |  |

### 1.69. pg_get_triggerdef {#pg_get_triggerdef}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_triggerdef</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>trigger_oid 或者trigger_oid, pretty_bool</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得trigger的create trigger语句</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_get_triggerdef(16992);
pg_get_triggerdef
------------------------------------------------------------------------------------------------------------
CREATE TRIGGER example_trigger AFTER INSERT ON public.company FOR EACH ROW EXECUTE FUNCTION auditlogfunc()
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.70. pg_get_userbyid {#pg_get_userbyid}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_userbyid</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>role_oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p><sub>name</sub></p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得特定role oid的role name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_get_userbyid(16426);
pg_get_userbyid
-----------------
lc0029999
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.71. pg_get_viewdef {#pg_get_viewdef}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_viewdef</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>view_name 或者 view_name, pretty_bool或者 view_oid或者 view_oid, pretty_bool或者view_oid, wrap_column_int</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获得view的定义</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_get_viewdef(&#39;company_view&#39;);
pg_get_viewdef
---------------------
SELECT company.id,+ company.name, + company.age + FROM company;
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.72. pg_index_column_has_property {#pg_index_column_has_property}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_index_column_has_property</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>index regclass, column integer, property text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>测试索引列是否有特定的索引列属性。索引列属性见下： asc 索引列升序 desc 索引列降序 nulls_first null值在前 nulls_last null值在后 orderable 列是否具有任何定义的排序顺序？ distance_orderable 列是否可以被"distance" operator 顺序扫描到, 比如 ORDER BY col &lt;→ constant ? returnable index-only扫描是否可以返回列值 search_array 列是否原生支持 col = ANY(array)搜索 search_nulls 列是否支持IS NULL 和IS NOT NULL 搜索<br />
注意：extension的访问方法可以为它们的indexes定义额外的属性名称。<br />
本函数在如下情况下会返回NULL：属性名称未知(not known)或者不适用于特定的对象Oid或者column number不能标识出一个有效的对象。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_index_column_has_property(&#39;idx_2&#39;::regclass,1,&#39;desc&#39;);
pg_index_column_has_property
------------------------------
f
(1 row)
postgres=# select pg_index_column_has_property(&#39;idx_2&#39;::regclass,1,&#39;asc&#39;);
pg_index_column_has_property
------------------------------
t
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.73. pg_index_has_property {#pg_index_has_property}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_index_has_property</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>index regclass, property text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>测试一个index是否具有特定的索引属性。如下是索引属性的清单 clusterable 在cluster命令中是否可以用到index index_scan index 是否支持 plain (non-bitmap) scans? bitmap_scan index 是否支持 bitmap scans? backward_scan Can the scan direction be changed in mid-scan (to support FETCH BACKWARD on a cursor without needing materialization)?<br />
注意：extension的访问方法可以为它们的indexes定义额外的属性名称。<br />
本函数在如下情况下会返回NULL：属性名称未知(not known)或者不适用于特定的对象oid不能标识出一个有效的对象。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_index_has_property(&#39;idx_2&#39;::regclass,&#39;index_scan&#39;);
pg_index_has_property
-----------------------
t
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.74. pg_indexam_has_property {#pg_indexam_has_property}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_indexam_has_property</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>am oid, property text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>测试一个index访问方法是否具有特定的属性。如下是索引访问方法属性清单： can_order 访问方法是否支持 ASC, DESC 以及CREATE INDEX的related keywords can_unique 访问方法是否支持unique indexes? can_multi_col 访问方法是否支持多列indexes? can_exclude 访问方法是否支持exclusion constraints? can_include 访问方法是否支持CREATE INDEX的 INCLUDE 子句<br />
<br />
本函数在如下情况下会返回NULL：属性名称未知(not known)或者不适用于特定的对象 oid不能标识出一个有效的对象。<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select * from pg_am;
 oid  | amname |      amhandler       | amtype
------+--------+----------------------+--------
    2 | heap   | heap_tableam_handler | t
  403 | btree  | bthandler            | i
  405 | hash   | hashhandler          | i
  783 | gist   | gisthandler          | i
 2742 | gin    | ginhandler           | i
 4000 | spgist | spghandler           | i
 3580 | brin   | brinhandler          | i
(7 rows)
&#10;postgres=#
postgres=# select pg_indexam_has_property(4000,&#39;can_multi_col&#39;);
 pg_indexam_has_property
-------------------------
 f
(1 row)
&#10;postgres=#
postgres=# select pg_indexam_has_property(403,&#39;can_unique&#39;);
 pg_indexam_has_property
-------------------------
 t
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.75. pg_options_to_table {#pg_options_to_table}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_options_to_table</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>options_array text[]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>setof record ( option_name text, option_value text )</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回pg_class.reloptions或者pg_attribute.attoptions表示的存储选项</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_options_to_table(reloptions) from pg_class where oid=&#39;16384&#39;;
pg_options_to_table
---------------------------------------------
(autovacuum_vacuum_insert_threshold,10000)
(autovacuum_vacuum_insert_scale_factor,0.1)
(2 rows)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.76. pg_tablespace_databases {#pg_tablespace_databases}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_tablespace_databases</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tablespace oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>setof oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回特定tablespace中保存的object的database的oid，如果本函数返回任何值，那么就表示tablespace不为空并且不能被drop掉。若想查出在该表空间内有哪些对象，你需要连接到本函数返回的database中，并查询pg_class获得这些对象。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_tablespace_databases(1663);
pg_tablespace_databases
-------------------------
16424
1
16878
14174
14173
(5 rows)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.77. pg_tablespace_location {#pg_tablespace_location}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_tablespace_location</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tablespace oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回指定tablespace的文件系统路径</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_tablespace_location(16391);
pg_tablespace_location
------------------------
/home/pg131/ts1
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.78. pg_typeof {#pg_typeof}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_typeof</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>any</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regtype</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>指定值的数据类型的oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# SELECT pg_typeof(33.339999);
-[ RECORD 1 ]------
pg_typeof | numeric
&#10;postgres=# SELECT typlen FROM pg_type WHERE oid = pg_typeof(33.339999);
-[ RECORD 1 ]
typlen | -1
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.79. COLLATION FOR {#collation-for}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>COLLATION FOR</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>"any"</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回指定值的collation的name，本函数的返回值是被双引号引起来的，如果入参表达式不能派生出collation，则返回null如果传入的参数不是可以collatable的data type，则会抛出错误</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select collation for(datname) from pg_database;
pg_collation_for
------------------
&quot;C&quot;
&quot;C&quot;
&quot;C&quot;
&quot;C&quot;
&quot;C&quot;
(5 rows)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.80. to_regclass {#to_regclass}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>to_regclass</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Regclass</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将文本形式的relation name转换为oid，本函数的输入参数不可以是数字形式的oid。如果本函数未找到输入参数指定的name，本函数会返回NULL</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select to_regclass(&#39;public.data1&#39;);
-[ RECORD 1 ]------
to_regclass | data1
&#10;postgres=# \x
Expanded display is off.
postgres=# select oid, relname from pg_class where oid=to_regclass(&#39;public.data1&#39;);
  oid  | relname
-------+---------
 16384 | data1
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.81. to_regcollation {#to_regcollation}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>to_regcollation</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regcollation</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将文本形式的collation name转换为oid，本函数的输入参数不可以是数字形式的oid。如果本函数未找到输入参数指定的name，本函数会返回NULL</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select to_regcollation(&#39;&quot;POSIX&quot;&#39;);
 to_regcollation
-----------------
 &quot;POSIX&quot;
(1 行记录)
&#10;postgres=# select * from pg_collation where oid=to_regcollation(&#39;&quot;POSIX&quot;&#39;);
 oid | collname | collnamespace | collowner | collprovider | collisdeterministic | collencoding | collcollate | collctype | collversion
-----+----------+---------------+-----------+--------------+---------------------+--------------+-------------+-----------+-------------
 951 | POSIX    |            11 |        10 | c            | t                   |           -1 | POSIX       | POSIX     |
(1 行记录)
&#10;postgres=# select oid,collname from pg_collation where oid=to_regcollation(&#39;&quot;POSIX&quot;&#39;);
 oid | collname
-----+----------
 951 | POSIX
(1 行记录)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.82. to_regnamespace {#to_regnamespace}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>to_regnamespace</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regnamespace</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将文本形式的schema name转换为oid，本函数的输入参数不可以是数字形式的oid。如果本函数未找到输入参数指定的name，本函数会返回NULL</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select to_regnamespace(&#39;public&#39;);
to_regnamespace
-----------------
public
(1 行记录)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.83. to_regoper {#to_regoper}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>to_regoper</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regoper</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将文本形式的operator name转换为oid，本函数的输入参数不可以是数字形式的oid。如果本函数未找到输入参数指定的name或者含义不明确，本函数会返回NULL</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid, oprname  from pg_operator where oid=to_regoper(&#39;!&#39;);
 oid | oprname
-----+---------
 388 | !
(1 row)
&#10;postgres=# select  to_regoper(&#39;!&#39;);
 to_regoper
------------
 !
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.84. to_regoperator {#to_regoperator}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>to_regoperator</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regoperator</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将文本形式的operator name(带参数类型)转换为oid，本函数的输入参数不可以是数字形式的oid。如果本函数未找到输入参数指定的name，本函数会返回NULL.</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid, oprname from pg_operator where oid=to_regoperator(&#39;+(integer,integer)&#39;);
 oid | oprname
-----+---------
 551 | +
(1 row)
&#10;postgres=#  select  to_regoperator(&#39;+(int4,int4)&#39;);
   to_regoperator
--------------------
 +(integer,integer)
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.85. to_regproc {#to_regproc}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>to_regproc</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regproc</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将文本的function或者procedure转换为其oid。如果本函数未找到输入参数指定的name或者含义不明确，本函数会返回NULL。本函数的输入参数不可以是数字形式的oid。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select to_regproc(&#39;pg_stat_statements&#39;);
     to_regproc
--------------------
 pg_stat_statements
(1 row)
&#10;postgres=# select oid,proname from pg_proc where oid=to_regproc(&#39;pg_stat_statements&#39;);
  oid  |      proname
-------+--------------------
 16401 | pg_stat_statements
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.86. to_regprocedure {#to_regprocedure}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>to_regprocedure</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regprocedure</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将文本的function或者procedure(带参数)转换为其oid。如果本函数未找到输入参数指定的name，本函数会返回NULL。本函数的输入参数不可以是数字形式的oid。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select to_regprocedure(&#39;pg_get_viewdef(text)&#39;);
   to_regprocedure
----------------------
 pg_get_viewdef(text)
(1 row)
&#10;postgres=# select oid, proname from pg_proc where oid= to_regprocedure(&#39;pg_get_viewdef(text)&#39;);
 oid  |    proname
------+----------------
 1640 | pg_get_viewdef
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.87. to_regrole {#to_regrole}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>to_regrole</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regrole</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将文本的role name转换为其oid。如果本函数未找到输入参数指定的name，本函数会返回NULL。本函数的输入参数不可以是数字形式的oid。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid,rolname from pg_roles where oid=to_regrole(&#39;lc0039999&#39;);
  oid  |  rolname
-------+-----------
 16877 | lc0039999
(1 row)
&#10;postgres=# select to_regrole(&#39;lc0039999&#39;);
 to_regrole
------------
 lc0039999
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.88. to_regtype {#to_regtype}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>to_regtype</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regtype</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将文本的type name转换为其oid。如果本函数未找到输入参数指定的name，本函数会返回NULL。本函数的输入参数不可以是数字形式的oid。<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select to_regtype(&#39;int4&#39;);
to_regtype
------------
integer
(1 row)
postgres=# select oid, typname from pg_type where oid=to_regtype(&#39;int4&#39;);
oid | typname
-----+---------
23 | int4
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.89. pg_describe_object {#pg_describe_object}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_describe_object</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>classid oid, objid oid, objsubid integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>用于描述pg_depend系统表中保存的依赖对象。<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select oid,relname from pg_class where oid in (select distinct classid from pg_depend) order by oid;
 oid  |         relname
------+-------------------------
 1247 | pg_type
 1255 | pg_proc
 1259 | pg_class
 2328 | pg_foreign_data_wrapper
 2602 | pg_amop
 2603 | pg_amproc
 2606 | pg_constraint
 2612 | pg_language
 2616 | pg_opclass
 2617 | pg_operator
 2618 | pg_rewrite
 2620 | pg_trigger
 2753 | pg_opfamily
 3079 | pg_extension
 3600 | pg_ts_dict
 3602 | pg_ts_config
 3764 | pg_ts_template
(17 rows)
&#10;postgres=# select * from pg_foreign_data_wrapper ;
  oid  | fdwname  | fdwowner | fdwhandler | fdwvalidator | fdwacl | fdwoptions
-------+----------+----------+------------+--------------+--------+------------
 16954 | file_fdw |       10 |      16952 |        16953 |        |
(1 row)
&#10;postgres=# select pg_describe_object(2328,16954,0);
      pg_describe_object
-------------------------------
 foreign-data wrapper file_fdw
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.90. pg_identify_object {#pg_identify_object}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_identify_object</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>classid oid, objid oid, objsubid integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>record ( type text, schema text, name text, identity text )</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回一个数据库对象的详细信息<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_identify_object(2328,16954,0);
pg_identify_object
---------------------------------------------
(&quot;foreign-data wrapper&quot;,,file_fdw,file_fdw)
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.91. pg_identify_object_as_address {#pg_identify_object_as_address}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_identify_object_as_address</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>classid oid, objid oid, objsubid integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>record ( type text, object_names text[], object_args text[] )</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回一个数据库对象的足够信息以标识出数据库对象<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_identify_object_as_address(2328,16954,0);
pg_identify_object_as_address
----------------------------------------
(&quot;foreign-data wrapper&quot;,{file_fdw},{})
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.92. pg_get_object_address {#pg_get_object_address}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_get_object_address</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>type text, object_names text[], object_args text[]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>record ( classid oid, objid oid, objsubid integer )</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>本函数是pg_identify_object_as_address的反函数<br />
<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_get_object_address(&#39;foreign-data wrapper&#39;,&#39;{file_fdw}&#39;,&#39;{}&#39;);
pg_get_object_address
-----------------------
(2328,16954,0)
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.93. col_description {#col_description}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>col_description</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>table oid, column integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获取某个表的某个列的comment<br />
<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# create table t_comment(c1 int );
CREATE TABLE
postgres=# comment on column t_comment.c1 is &#39;this is c1 comment!&#39;;
COMMENT
postgres=# select oid from pg_class where oid=to_regclass(&#39;t_comment&#39;)
postgres-# ;
  oid
-------
 17001
(1 row)
postgres=# select col_description(17001,1);
   col_description
---------------------
 this is c1 comment!
(1 row)
postgres=#
postgres=# select col_description(to_regclass(&#39;t_comment&#39;),1);
   col_description
---------------------
 this is c1 comment!
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.94. obj_description {#obj_description}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>obj_description</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>object oid, catalog name 或者object oid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回特定数据库对象的注释信息<br />
<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# comment on table t_comment is  &#39; table-level test comment&#39;;
COMMENT
postgres=# \dt+ data1
                         List of relations
 Schema | Name  | Type  | Owner | Persistence | Size  | Description
--------+-------+-------+-------+-------------+-------+-------------
 public | data1 | table | pg131 | permanent   | 42 MB |
(1 row)
&#10;postgres=# \dt+ t_comment;
                                   List of relations
 Schema |   Name    | Type  | Owner | Persistence |  Size   |        Description
--------+-----------+-------+-------+-------------+---------+---------------------------
 public | t_comment | table | pg131 | permanent   | 0 bytes |  table-level test comment
(1 row)
&#10;postgres=# select obj_description(17001);
      obj_description
---------------------------
  table-level test comment
(1 row)
&#10;postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.95. shobj_description {#shobj_description}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>shobj_description</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>object oid, catalog name</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回特定共享数据库对象(如databases, roles, and tablespaces)的注释信息.</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select shobj_description(14174,&#39;pg_database&#39;);
shobj_description
--------------------------------------------
default administrative connection database
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.96. pg_current_xact_id {#pg_current_xact_id}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_current_xact_id</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>xid8</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回当前的事务id，若是没有当前事务id，系统会自动指派一个新的事务id</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_current_xact_id();
pg_current_xact_id
--------------------
720
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.97. pg_current_xact_id_if_assigned() {#pg_current_xact_id_if_assigned}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_current_xact_id_if_assigned()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>xid8</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回当前的current transaction’s ID，若是没有transaction’s ID被指派，本函数返回NULL。如果事务可能是只读的，最好使用本函数，以避免不必要的XID消耗。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=*# select pg_current_xact_id_if_assigned();
pg_current_xact_id_if_assigned
--------------------------------
(1 row)
postgres=*# update data1 set c2=&#39;data1_1&#39; where c1=1;
UPDATE 1
postgres=*# select pg_current_xact_id_if_assigned();
pg_current_xact_id_if_assigned
--------------------------------
722
(1 row)
postgres=*#</code></pre></td>
</tr>
</tbody>
</table>

### 1.98. pg_xact_status {#pg_xact_status}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_xact_status</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>xid8</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回近期事务的提交状态。本函数的执行结果是下面三个中的一个:in progress、commited、aborted。当事务足够老而没有在PostgreSQL中保存下来时，commit status会被丢弃，此时本函数返回结果为NULL。请注意，针对prepared transactions，本函数的返回结果为in progress,应用程序必须检查pg_prepared_xacts以确定一个transaction ID是否属于prepared transaction</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_xact_status(pg_current_xact_id());
pg_xact_status
----------------
in progress
(1 row)
postgres=# postgres=# select pg_xact_status(722::text::xid8);
pg_xact_status
----------------
committed
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.99. pg_current_snapshot {#pg_current_snapshot}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_current_snapshot</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>pg_snapshot</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回当前的snapshot,这是一种显示哪个transaction id是正处于in-progress状态的数据结构。注意：有关pg_snapshot数据类型： pg_snapshot数据类型用于存储在一个特定时间点上的transaction ID visibility信息。 pg_snapshot数据类型的表示方法是xmin:xmax:xip_list这个xmin:xmax:xip_list就是pg_snapshot数据类型组成。见下： xmin:处于active状态的最小的transaction id，所有小于xmin的transaction id要么是committed (visible),要么是rolled back(dead) xmax:大于或者等于本xmax值的transaction id是在snapshot结束时未完成的，因此，xmax是不可见的。 xip_list:在生成snapshot时，处于in progress状态的transactions。在xmin ⇐ X &lt; xmax范围内并且不在本xip_list中的transaction ID 表示在snapshot生成时是已经完成的transaction ID,因此，根据commit status，要么是visible的要么是dead，本列表中不包括subtransactions的transaction IDs<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_current_snapshot();
pg_current_snapshot
---------------------
727:727:
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.100. pg_snapshot_xip {#pg_snapshot_xip}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_snapshot_xip</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>pg_snapshot</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>setof xid8</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回snapshot中处于in-progress状态的transaction id</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_snapshot_xip(&#39;10:20:10,14,15&#39;);
pg_snapshot_xip
-----------------
10
14
15
(3 rows)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.101. pg_snapshot_xmax {#pg_snapshot_xmax}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_snapshot_xmax</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>pg_snapshot</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>xid8</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回snapshot的xmax</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_snapshot_xmax(&#39;10:20:10,14,15&#39;);
pg_snapshot_xmax
------------------
20
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.102. pg_snapshot_xmin {#pg_snapshot_xmin}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_snapshot_xmin</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>pg_snapshot</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>xid8</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回snapshot的xmin</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_snapshot_xmin(&#39;10:20:10,14,15&#39;);
pg_snapshot_xmin
------------------
10
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.103. pg_visible_in_snapshot {#pg_visible_in_snapshot}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_visible_in_snapshot</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>xid8, pg_snapshot</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>bool</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>给定的事务ID是否对snapshot可见，即：给定的事务ID是否在生成snapshot之前完成。本函数对subtransaction ID不能给出正确的结果。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_visible_in_snapshot(722::text::xid8,&#39;10:20:10,14,15&#39;);
pg_visible_in_snapshot
------------------------
f
(1 row)
postgres=# select pg_visible_in_snapshot(12::text::xid8,&#39;10:20:10,14,15&#39;);
pg_visible_in_snapshot
------------------------
t
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.104. txid_current {#txid_current}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>txid_current</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>bigint</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回当前的事务id，若是没有当前事务id，系统会自动指派一个新的事务id。本函数（返回值是bigint数据类型）的作用与pg_current_xact_id(返回值是xid8数据类型)的作用是类似的，只是两个函数的返回值数据类型不同。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select txid_current();
txid_current
--------------
735
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.105. txid_current_if_assigned() {#txid_current_if_assigned}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>txid_current_if_assigned()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>bigint</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>本函数（注意：返回值是bigint数据类型）的作用与pg_current_xact_id_if_assigned(注意：返回值是xid8数据类型)的作用是类似的，只是两个函数的返回值数据类型不同。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>[pg131@VM-0-8-centos ~]$ psql -d postgres psql (13.1)
Type &quot;help&quot; for help.
postgres=# select txid_current_if_assigned();
txid_current_if_assigned
--------------------------
(1 row)
postgres=# begin;
BEGIN
postgres=*# select txid_current_if_assigned();
txid_current_if_assigned
--------------------------
(1 row)
postgres=*# select txid_current();
txid_current
--------------
738
(1 row)
postgres=*# select txid_current_if_assigned();
txid_current_if_assigned
--------------------------
738
(1 row)</code></pre></td>
</tr>
</tbody>
</table>

### 1.106. txid_current_snapshot() {#txid_current_snapshot}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>txid_current_snapshot()</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>txid_snapshot</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回当前的snapshot,这是一种显示哪个transaction id是正处于in-progress状态的数据结构。本函数（注意：返回值是txid_snapshot数据类型）的作用与pg_current_snapshot (注意：返回值是pg_snapshot数据类型)的作用是类似的，只是两个函数的返回值数据类型不同。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select txid_current_snapshot();
txid_current_snapshot
-----------------------
741:741:
(1 row)
 postgres=# \gdesc
 Column | Type
 -----------------------+---------------
 txid_current_snapshot | txid_snapshot
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.107. txid_snapshot_xip(txid_snapshot) {#txid_snapshot_xiptxid_snapshot}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>txid_snapshot_xip(txid_snapshot)</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>txid_snapshot</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>setof bigint</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回snapshot中处于in-progress状态的transaction id。本函数（注意：返回值是txid_snapshot数据类型）的作用与pg_snapshot_xip (注意：返回值是pg_snapshot数据类型)的作用是类似的，只是两个函数的返回值数据类型不同。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select txid_snapshot_xip(&#39;10:20:10,14,15&#39;);
txid_snapshot_xip
-------------------
10
14
15
(3 rows)
 postgres=# \gdesc
 Column | Type
 -------------------+--------
 txid_snapshot_xip | bigint
 (1 row)</code></pre></td>
</tr>
</tbody>
</table>

### 1.108. txid_snapshot_xmax {#txid_snapshot_xmax}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>txid_snapshot_xmax</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>txid_snapshot</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>bigint</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回snapshot的xmax。本函数（注意：返回值是bigint数据类型）的作用与pg_snapshot_xmax (注意：返回值是pg_snapshot数据类型)的作用是类似的，只是两个函数的返回值数据类型不同。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select txid_snapshot_xmax(&#39;10:20:10,14,15&#39;);
txid_snapshot_xmax
--------------------
20
(1 row)
 postgres=# \gdesc
 Column | Type
 --------------------+--------
 txid_snapshot_xmax | bigint
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.109. txid_snapshot_xmin {#txid_snapshot_xmin}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>txid_snapshot_xmin</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>txid_snapshot</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>bigint</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回snapshot的xmin。本函数（注意：返回值是bigint数据类型）的作用与pg_snapshot_xmin(注意：返回值是pg_snapshot数据类型)的作用是类似的，只是两个函数的返回值数据类型不同。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select txid_snapshot_xmin(&#39;10:20:10,14,15&#39;);
txid_snapshot_xmin
--------------------
10
(1 row)
 postgres=# \gdesc
 Column | Type
 --------------------+--------
 txid_snapshot_xmin | bigint
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.110. txid_visible_in_snapshot {#txid_visible_in_snapshot}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>txid_visible_in_snapshot</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>bigint, txid_snapshot</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>boolean</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>给定的事务ID是否对snapshot可见，即：给定的事务ID是否在生成snapshot之前完成。本函数对subtransaction ID不能给出正确的结果。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select txid_visible_in_snapshot(722,&#39;10:20:10,14,15&#39;);
txid_visible_in_snapshot
--------------------------
f
(1 row)
 postgres=# select txid_visible_in_snapshot(12,&#39;10:20:10,14,15&#39;);
 txid_visible_in_snapshot
 --------------------------
 t
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.111. txid_status {#txid_status}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>txid_status</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>bigint</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回近期事务的提交状态。本函数的执行结果是下面三个中的一个:in progress、commited、aborted。当事务足够老而没有在PostgreSQL中保存下来时，commit status会被丢弃，此时本函数返回结果为NULL。请注意，针对prepared transactions，本函数的返回结果为in progress,应用程序必须检查pg_prepared_xacts以确定一个transaction ID是否属于prepared transaction.</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select txid_status(txid_current());
txid_status
-------------
in progress
(1 row)
 postgres=# select txid_current();
 txid_current
 --------------
 742
 (1 row)
 postgres=# select txid_status(722);
 txid_status
 -------------
 committed
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.112. pg_xact_commit_timestamp {#pg_xact_commit_timestamp}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_xact_commit_timestamp</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>xid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>timestamp with time zone</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回一个事务的提交时间。本函数能正常使用的前提就是配置参数track_commit_timestamp设置为on，否会有如下提示：</p>
<pre class="sql"><code>postgres=# select pg_xact_commit_timestamp(722::text::xid);
ERROR: could not get commit timestamp data
HINT: Make sure the configuration parameter &quot;track_commit_timestamp&quot; is set.
postgres=#</code></pre></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select txid_current();
txid_current
--------------
743
(1 row)
 postgres=# select pg_xact_commit_timestamp(743::text::xid);
 pg_xact_commit_timestamp
 ------------------------------
 2021-04-29 16:52:37.19133+08
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.113. pg_last_committed_xact {#pg_last_committed_xact}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_last_committed_xact</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入数据类型</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>record ( xid xid, timestamp timestamp with time zone )</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回最后一个提交事务的transaction id和commit timestamp</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_last_committed_xact();
pg_last_committed_xact
--------------------------------------
(743,&quot;2021-04-29 16:52:37.19133+08&quot;)
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.114. pg_control_checkpoint {#pg_control_checkpoint}

|  |  |
|----|----|
| 函数名称 | pg_control_checkpoint |
| 参数数据类型 | 无输入数据类型 |
| 函数返回值数据类型 | record |
| 函数含义 | 本函数是从PostgreSQL控制文件中获取数据。本函数返回当前checkpoint状态的相关信息 |
| 使用举例 |  |

### 1.115. pg_control_system {#pg_control_system}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_control_system</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入数据类型</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>record</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>本函数是从PostgreSQL控制文件中获取数据。本函数返回当前控制文件状态的相关信息。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_control_system();
pg_control_system
---------------------------------------------------------------
(1300,202007201,6908228805274066467,&quot;2021-04-29 16:57:56+08&quot;)
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.116. pg_control_init {#pg_control_init}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_control_init</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入数据类型</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>record</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>本函数是从PostgreSQL控制文件中获取数据。本函数返回cluster初始化时的相关信息</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_control_init();
pg_control_init
---------------------------------------------------
(8,8192,131072,8192,16777216,64,32,1996,2048,t,0)
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.117. pg_control_recovery {#pg_control_recovery}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pg_control_recovery</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入数据类型</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>record</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>本函数是从PostgreSQL控制文件中获取数据。本函数返回恢复状态的信息。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pg_control_recovery();
pg_control_recovery
---------------------
(0/0,0,0/0,0/0,f)
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.118. gen_random_uuid {#gen_random_uuid}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>gen_random_uuid</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>uuid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>本函数返回version 4版本的uuid</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select gen_random_uuid();
gen_random_uuid
--------------------------------------
39158a63-f6d0-4883-8765-8b8e9c9cae62
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.119. array_to_tsvector {#array_to_tsvector}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>array_to_tsvector</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text[]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将array of lexemes转换为tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select array_to_tsvector(&#39;{fat,cat,rat}&#39;::text[]);
array_to_tsvector
-------------------
&#39;cat&#39; &#39;fat&#39; &#39;rat&#39;
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.120. get_current_ts_config {#get_current_ts_config}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>get_current_ts_config</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>无输入参数</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regconfig</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回当前默认的text search配置的oid（参见配置参数default_text_search_config）</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select get_current_ts_config();
get_current_ts_config
-----------------------
english
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.121. length {#length}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>length</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回lexemes的数量</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select length(&#39;fat:2,4 cat:3 rat:5A&#39;::tsvector);
length
--------
3
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.122. numnode {#numnode}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>numnode</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsquery</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回lexemes加operator的数量</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select numnode(&#39;(fat &amp; rat) | cat&#39;::tsquery) ;
numnode
---------
5
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.123. plainto_tsquery {#plainto_tsquery}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>plainto_tsquery</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>[config regconfig,] query text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsquery</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将text转换为tsquery。其中，字符串中的任何标点都将被忽略</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select plainto_tsquery(&#39;english&#39;, &#39;The Fat Rats&#39;);
plainto_tsquery
-----------------
&#39;fat&#39; &amp; &#39;rat&#39;
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.124. phraseto_tsquery {#phraseto_tsquery}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>phraseto_tsquery</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>[config regconfig,] query text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsquery</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将text转换为tsquery。其中，字符串中的任何标点都将被忽略</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select phraseto_tsquery(&#39;english&#39;, &#39;The Fat Rats&#39;) ;
phraseto_tsquery
------------------
&#39;fat&#39; &lt;-&gt; &#39;rat&#39;
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.125. websearch_to_tsquery {#websearch_to_tsquery}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>websearch_to_tsquery</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>[ <em>config</em> regconfig, ] <em>query</em> text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsquery</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将text转换为tsquery。引用的单词序列被转换成短语测试。"or"一词被理解为产生or运算符，破折号产生NOT运算符，忽略其他标点符号</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select websearch_to_tsquery(&#39;english&#39;, &#39;&quot;fat rat&quot; or cat dog&#39;);
websearch_to_tsquery
---------------------------------
&#39;fat&#39; &lt;-&gt; &#39;rat&#39; | &#39;cat&#39; &amp; &#39;dog&#39;
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.126. querytree {#querytree}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>querytree</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsquery</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回一个tsquery中的可索引部分。当返回结果为空或者T时，表示这是一个不可索引的query。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select querytree(&#39;foo &amp; ! bar&#39;::tsquery);
querytree
-----------
&#39;foo&#39;
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.127. setweight {#setweight}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>setweight</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>vector tsvector, weight "char"或者vector tsvector, weight "char", lexemes text[]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>为vector中的每个元素指定权重或者为在lexemes之内的vector中的每个元素指定权重</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select setweight(&#39;fat:2,4 cat:3 rat:5B&#39;::tsvector, &#39;A&#39;);
setweight
-------------------------------
&#39;cat&#39;:3A &#39;fat&#39;:2A,4A &#39;rat&#39;:5A
(1 row)
 postgres=#
 postgres=# select setweight(&#39;fat:2,4 cat:3 rat:5,6B&#39;::tsvector, &#39;A&#39;, &#39;{cat,rat}&#39;);
 setweight
 --------------------------------
 &#39;cat&#39;:3A &#39;fat&#39;:2,4 &#39;rat&#39;:5A,6A
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.128. strip {#strip}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>strip</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>从tsvector中抹掉position和weight</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select strip(&#39;fat:2,4 cat:3 rat:5A&#39;::tsvector);
strip
-------------------
&#39;cat&#39; &#39;fat&#39; &#39;rat&#39;
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.129. to_tsquery {#to_tsquery}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>to_tsquery</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regconfig, text 或者text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsquery</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将text转换为tsquery，本函数的返回结果必须由有效的tsquery operator进行连接。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select to_tsquery(&#39;english&#39;, &#39;The &amp; Fat &amp; Rats&#39;);
to_tsquery
---------------
&#39;fat&#39; &amp; &#39;rat&#39;
(1 row)
 postgres=# select to_tsquery( &#39;The &amp; Fat &amp; Rats&#39;);
 to_tsquery
 ---------------
 &#39;fat&#39; &amp; &#39;rat&#39;
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.130. to_tsvector {#to_tsvector}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>to_tsvector</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regconfig,text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将text转换为tsvector ，结果中包括位置信息</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select to_tsvector(&#39;english&#39;, &#39;The Fat Rats&#39;);
to_tsvector
-----------------
&#39;fat&#39;:2 &#39;rat&#39;:3
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.131. to_tsvector {#to_tsvector-2}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>to_tsvector</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>regconfig,json或者regconfig,jsonb</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将json文档中的每个字符串值转换为tsvector，结果值是按照文档顺序进行连接后输出的，当输入参数数据类型为jsonb时，json对象的字段的文档顺序是与实现相关的</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select to_tsvector(&#39;english&#39;, &#39;{&quot;aa&quot;: &quot;The Fat Rats&quot;, &quot;b&quot;: &quot;dog&quot;}&#39;::json);
to_tsvector -------------------------
&#39;dog&#39;:5 &#39;fat&#39;:2 &#39;rat&#39;:3
(1 row)
 postgres=# postgres=# select to_tsvector(&#39;english&#39;, &#39;{&quot;aa&quot;: &quot;The Fat Rats&quot;, &quot;b&quot;: &quot;dog&quot;}&#39;::jsonb);
 to_tsvector
 -------------------------
 &#39;dog&#39;:1 &#39;fat&#39;:4 &#39;rat&#39;:5
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.132. json_to_tsvector {#json_to_tsvector}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>json_to_tsvector</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>[config regconfig,] json, jsonb</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将json文档中满足filter条件的每个item转换为一个tsvector。结果值是按照文档顺序进行连接后输出的，当输入参数数据类型为jsonb时，json对象的字段的文档顺序是与实现相关的。Filter条件必须是一个包括另个或者多个关键字的json 数组：string代表包括所有字符串值numeric代表包括所有数字值boolean代表包括所有boolean值key代表包括所有keyall代表包括上述所有。作为一个简单的例子，filter条件不可以是一个简单的并且是上述关键字之一的json值。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select json_to_tsvector(&#39;english&#39;, &#39;{&quot;a&quot;: &quot;The Fat Rats&quot;, &quot;b&quot;: 123}&#39;::json, &#39;[&quot;string&quot;, &quot;numeric&quot;]&#39;);
json_to_tsvector
-------------------------
&#39;123&#39;:5 &#39;fat&#39;:2 &#39;rat&#39;:3
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.133. jsonb_to_tsvector {#jsonb_to_tsvector}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>jsonb_to_tsvector</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>[config regconfig,] jsonb,jsonb</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将json文档中满足filter条件的每个item转换为一个tsvector。结果值是按照文档顺序进行连接后输出的，当输入参数数据类型为jsonb时，json对象的字段的文档顺序是与实现相关的。Filter条件必须是一个包括另个或者多个关键字的json 数组：string代表包括所有字符串值numeric代表包括所有数字值boolean代表包括所有boolean值key代表包括所有keyall代表包括上述所有。作为一个简单的例子，filter条件不可以是一个简单的并且是上述关键字之一的json值。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select jsonb_to_tsvector(&#39;english&#39;, &#39;{&quot;a&quot;: &quot;The Fat Rats&quot;, &quot;b&quot;: 123}&#39;::jsonb, &#39;[&quot;string&quot;, &quot;numeric&quot;]&#39;);
jsonb_to_tsvector
-------------------------
&#39;123&#39;:5 &#39;fat&#39;:2 &#39;rat&#39;:3
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.134. ts_delete {#ts_delete}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>ts_delete</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector,text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>从vector中删除掉指定的lexeme<br />
</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select ts_delete(&#39;fat:2,4 cat:3 rat:5A&#39;::tsvector, &#39;fat&#39;);
ts_delete
------------------
&#39;cat&#39;:3 &#39;rat&#39;:5A
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.135. ts_delete {#ts_delete-2}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>ts_delete</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector,text[]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>从vector中删除掉指定的lexeme</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select ts_delete(&#39;fat:2,4 cat:3 rat:5A&#39;::tsvector, ARRAY[&#39;fat&#39;,&#39;rat&#39;]);
ts_delete -----------
&#39;cat&#39;:3
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.136. ts_filter {#ts_filter}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>ts_filter</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector, "char"[]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>从vector中筛选出带有指定weights的元素</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select ts_filter(&#39;fat:2,4 cat:3b,7c rat:5A&#39;::tsvector, &#39;{a,b}&#39;);
ts_filter
-------------------
&#39;cat&#39;:3B &#39;rat&#39;:5A
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.137. ts_headline {#ts_headline}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>ts_headline</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>[config regconfig,] document text, query tsquery [, options text]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>以简写的形式显示在document匹配到的query</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select ts_headline(&#39;The fat cat ate the rat.&#39;, &#39;cat&#39;);
ts_headline
---------------------------------
The fat &lt;b&gt;cat&lt;/b&gt; ate the rat.
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.138. ts_headline {#ts_headline-2}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>ts_headline</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>[config regconfig,] document json, query tsquery [, options text]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>json</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>以缩写的形式显示在json document匹配到的query</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select ts_headline(&#39;{&quot;cat&quot;:&quot;raining cats and dogs&quot;}&#39;::json, &#39;cat&#39;);
ts_headline
----------------------------------------
{&quot;cat&quot;:&quot;raining &lt;b&gt;cats&lt;/b&gt; and dogs&quot;}
(1 row)</code></pre></td>
</tr>
</tbody>
</table>

### 1.139. ts_headline {#ts_headline-3}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>ts_headline</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>[config regconfig,] document jsonb, query tsquery [, options text]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>jsonb</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>以缩写的形式显示在json document匹配到的query</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select ts_headline(&#39;{&quot;cat&quot;:&quot;raining cats and dogs&quot;}&#39;::jsonb, &#39;cat&#39;);
ts_headline
-----------------------------------------
{&quot;cat&quot;: &quot;raining &lt;b&gt;cats&lt;/b&gt; and dogs&quot;}
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.140. ts_rank {#ts_rank}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>ts_rank</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>[weights real[], ] vector tsvector, query tsquery [, normalization integer]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>real</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>计算query与vector的匹配程度</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# SELECT ts_rank(to_tsvector(&#39;The quick brown fox jumps over the lazy dog.&#39;),to_tsquery(&#39;fox &amp; dog&#39;)); ts_rank
------------
0.09148999
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.141. ts_rank_cd {#ts_rank_cd}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>ts_rank_cd</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>[weights real[], ] vector tsvector, query tsquery [, normalization integer]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>real</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>使用覆盖密度算法来计算query与vector的匹配程度</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# SELECT ts_rank_cd(&#39;{0.1, 0.2, 0.4, 1.0}&#39;, to_tsvector(&#39;PostgreSQL full text search is a wonderful method&#39;),to_tsquery(&#39;wonderful&#39;));
ts_rank_cd
------------
0.1
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.142. ts_rewrite {#ts_rewrite}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>ts_rewrite</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>query tsquery, target tsquery, substitute tsquery</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsquery</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>用substitute替换掉query中的target</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# SELECT ts_rewrite(&#39;c &amp; b&#39;::tsquery, &#39;b&#39;::tsquery, &#39;bad|bat&#39;::tsquery);
ts_rewrite
-------------------------
( &#39;bad&#39; | &#39;bat&#39; ) &amp; &#39;c&#39;
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.143. ts_rewrite {#ts_rewrite-2}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>ts_rewrite</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>query tsquery, select text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsquery</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# CREATE TABLE test (col1 tsquery PRIMARY KEY, COL2 tsquery);
CREATE TABLE
postgres=# INSERT INTO test values (&#39;p&#39;,&#39;q&#39;);
INSERT 0 1
postgres=# SELECT ts_rewrite(&#39;r &amp; q&#39;::tsquery, &#39;SELECT col1,col2 FROM test&#39;);
ts_rewrite
------------
&#39;r&#39; &amp; &#39;q&#39;
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.144. tsquery_phrase {#tsquery_phrase}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>tsquery_phrase</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>query1 tsquery, query2 tsquery</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsquery</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>构造一个phrase query用于在连续的词位匹配query1和query2(同&lt;→操作符)</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select tsquery_phrase(to_tsquery(&#39;fat&#39;), to_tsquery(&#39;cat&#39;));
tsquery_phrase
-----------------
&#39;fat&#39; &lt;-&gt; &#39;cat&#39;
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.145. tsquery_phrase {#tsquery_phrase-2}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>tsquery_phrase</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>query1 tsquery, query2 tsquery, distance integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsquery</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>构造一个词组查询，该词组搜索匹配query1且query2完全distance分开词素的匹配项</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select tsquery_phrase(to_tsquery(&#39;fat&#39;), to_tsquery(&#39;cat&#39;), 10);
tsquery_phrase
------------------
&#39;fat&#39; &lt;10&gt; &#39;cat&#39;
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.146. tsvector_to_array {#tsvector_to_array}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>tsvector_to_array</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text[]</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将tsvector转换为词素数组</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select tsvector_to_array(&#39;fat:2,4 cat:3 rat:5A&#39;::tsvector) ;
tsvector_to_array
-------------------
{cat,fat,rat}
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.147. unnest {#unnest}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>unnest</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>tsvector</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>setof record ( lexeme text, positions smallint[], weights text )</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将tsvector扩展为一行一个词素</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select * from unnest(&#39;cat:3 fat:2,4 rat:5A&#39;::tsvector);
 lexeme | positions | weights
--------+-----------+---------
 cat    | {3}       | {D}
 fat    | {2,4}     | {D,D}
 rat    | {5}       | {A}
(3 rows)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.148. abbrev {#abbrev}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>abbrev</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将inet转换为text的缩写显示格式</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select abbrev(inet &#39;10.1.1.3&#39;);
abbrev
----------
10.1.1.3
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.149. abbrev {#abbrev-2}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>abbrev</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>cidr</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将cidr转换为text的缩写显示格式，返回结果中去掉了netmask中右边的零</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select abbrev(cidr &#39;10.1.0.0/16&#39;);
abbrev
---------
10.1/16
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.150. broadcast {#broadcast}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>broadcast</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>计算一个ip地址的广播地址</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select broadcast(inet &#39;192.168.1.5/24&#39;);
broadcast
------------------
192.168.1.255/24
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.151. family {#family}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>family</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回一个地址是IPV4（返回4）还是IPV6（返回6）</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select family(&#39;fe80::5054:ff:fe99:540c&#39;) ;
family
--------
6
(1 row)
 postgres=# select family(inet &#39;172.1.0.23&#39;) ;
 family
 --------
 4
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.152. host {#host}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>host</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回IP地址的text形式，且忽略掉netmask</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select host(inet &#39;192.168.1.0/24&#39;);
host
-------------
192.168.1.0
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.153. hostmask {#hostmask}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>hostmask</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>Inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回ip地址的host mask</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select hostmask(inet &#39;192.168.23.20/30&#39;) ;
hostmask
----------
0.0.0.3
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.154. inet_merge {#inet_merge}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>inet_merge</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet, inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>cidr</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回包含两个给定网络的最小网络</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select inet_merge(inet &#39;192.168.1.5/24&#39;, inet &#39;192.168.2.5/24&#39;);
inet_merge
----------------
192.168.0.0/22
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.155. inet_same_family {#inet_same_family}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>inet_same_family</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet，inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>bool</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回两个ip地址是否属于同一个family</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select inet_same_family(inet &#39;192.168.1.5/24&#39;, inet &#39;::1&#39;);
inet_same_family
------------------
f
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.156. masklen {#masklen}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>masklen</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回以位为单位的网络掩码长度</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select masklen(inet &#39;192.168.1.5/24&#39;);
masklen
---------
24
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.157. netmask {#netmask}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>netmask</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回网络地址的网络掩码</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select netmask(inet &#39;192.168.1.5/24&#39;);
netmask
---------------
255.255.255.0
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.158. network {#network}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>network</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回地址的网络部分，将网络掩码右边的内容清零</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select network(inet &#39;192.168.1.5/24&#39;) ;
network
----------------
192.168.1.0/24
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.159. set_masklen {#set_masklen}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>set_masklen</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet, integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>为inet设置netmask长度，网络地址部分保持不变</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select set_masklen(inet &#39;192.168.1.5/24&#39;, 16);
set_masklen
----------------
192.168.1.5/16
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.160. set_masklen {#set_masklen-2}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>set_masklen</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>cidr, integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>cidr</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>为cidr设置netmask长度，网络地址右边的设置为零</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select set_masklen(cidr &#39;192.168.1.0/24&#39;, 16);
set_masklen
----------------
192.168.0.0/16
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.161. text {#text}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>text</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>inet</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>text</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回ip地址及其掩码的text形式</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select text(inet &#39;192.168.1.5&#39;);
text
----------------
192.168.1.5/32
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.162. trunc {#trunc}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>trunc</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>macaddr</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>macaddr</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将mac地址的最后三个字节清零，前缀可以与特定的网卡制造商关联</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select trunc(macaddr &#39;12:34:56:78:90:ab&#39;) ;
trunc
-------------------
12:34:56:00:00:00
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.163. trunc {#trunc-2}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>trunc</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>macaddr8</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>macaddr8</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将mac地址的最后五个字节清零，前缀可以与特定的网卡制造商关联</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select trunc(macaddr8 &#39;12:34:56:78:90:ab:cd:ef&#39;) ;
trunc
-------------------------
12:34:56:00:00:00:00:00
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.164. macaddr8_set7bit {#macaddr8_set7bit}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>macaddr8_set7bit</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>macaddr8</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>macaddr8</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将地址的第7位设置为1，从而创建被称为修改后的EUI-64，以包含在IPv6地址中。</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select macaddr8_set7bit(macaddr8 &#39;00:34:56:ab:cd:ef&#39;);
macaddr8_set7bit
-------------------------
02:34:56:ff:fe:ab:cd:ef
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.165. area {#area}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>area</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>geometric_type</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>double precision</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>计算面积，针对box, path, circle适用，path必须是能closed，否则会返回NULL</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select area(box &#39;(2,2),(0,0)&#39;);
area
------
4
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.166. center {#center}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>center</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>geometric_type</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>point</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>计算中点，针对box, circle适用</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select center(box &#39;(1,2),(0,0)&#39;) ;
 center
 ---------
 (0.5,1)
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.167. diagonal {#diagonal}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>diagonal</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>box</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>lseg</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>获取box的对角线作为一个line segment，作用与lseg(box)一样</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select diagonal(box &#39;(1,2),(0,0)&#39;);
diagonal
---------------
[(1,2),(0,0)]
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.168. diameter {#diameter}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>diameter</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>circle</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>double precision</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>计算circle的直径</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select diameter(circle &#39;&lt;(0,0),2&gt;&#39;) ;
diameter
 ----------
  4
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.169. height {#height}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>height</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>box</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>double precision</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>计算box的垂直大小</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select height(box &#39;(1,2),(0,0)&#39;);
 height
 --------
 2
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.170. isclosed {#isclosed}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>isclosed</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>path</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>bool</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>path是否是closed的</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select isclosed(path &#39;((0,0),(1,1),(2,0))&#39;);
 isclosed
 ----------
  t
   (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.171. isopen {#isopen}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>isopen</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>path</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>bool</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>Path是否是open的</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select isopen(path &#39;[(0,0),(1,1),(2,0)]&#39;);
isopen
 --------
  t
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.172. length {#length-2}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>length</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>geometric_type</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>double precision</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>计算总长度，对lseg以及path适用</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select length(path &#39;((-1,0),(1,0))&#39;) ;
 length
 --------
  4
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.173. npoints {#npoints}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>npoints</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>geometric_type</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>integer</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>返回point的数量，对path以及polygon适用</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select npoints(path &#39;[(0,0),(1,1),(2,0)]&#39;);
npoints
---------
 3
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.174. pclose {#pclose}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>pclose</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>path</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>path</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将patch转换为closed的形式</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select pclose(path &#39;[(0,0),(1,1),(2,0)]&#39;);
pclose
---------------------
((0,0),(1,1),(2,0))
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.175. popen {#popen}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>popen</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>path</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>path</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>将patch转换为open的形式</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select popen(path &#39;((0,0),(1,1),(2,0))&#39;);
popen
---------------------
[(0,0),(1,1),(2,0)]
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.176. radius {#radius}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>radius</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>circle</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>double precision</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>求一个圆形的半径</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select radius(circle &#39;&lt;(0,0),2&gt;&#39;);
 radius
 --------
 2
 (1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.177. slope {#slope}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>slope</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>point,point</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>double precision</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>计算通过两个点的直线的斜率</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select slope(point &#39;(0,0)&#39;, point &#39;(2,1)&#39;);
 slope
 -------
  0.5
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.178. width {#width}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>width</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>double precision</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>box</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>计算box的horizontal size</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select width(box &#39;(1,2),(0,0)&#39;) ;
width
-------
1
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>

### 1.179. box {#box}

<table class="tableblock frame-all grid-all stretch">
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<th class="tableblock halign-left valign-top"><p>函数名称</p></th>
<th class="tableblock halign-left valign-top"><p>box</p></th>
</tr>
&#10;<tr>
<td class="tableblock halign-left valign-top"><p>参数数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>circle</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数返回值数据类型</p></td>
<td class="tableblock halign-left valign-top"><p>box</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>函数含义</p></td>
<td class="tableblock halign-left valign-top"><p>计算圆内切的box</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>使用举例</p></td>
<td class="tableblock halign-left valign-top"><pre class="sql"><code>postgres=# select box(circle &#39;&lt;(0,0),2&gt;&#39;);
box
-------------------------------------------------------------------------------
(1.414213562373095,1.414213562373095),(-1.414213562373095,-1.414213562373095)
(1 row)
postgres=#</code></pre></td>
</tr>
</tbody>
</table>
