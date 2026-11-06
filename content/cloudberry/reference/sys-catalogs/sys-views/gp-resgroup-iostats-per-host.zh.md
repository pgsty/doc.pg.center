---
title: "gp_resgroup_iostats_per_host"
description: "`gp_toolkit.gp_resgroup_iostats_per_host` 视图允许管理员按主机查看各资源组当前的磁盘 I/O 使用情况。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/gp-resgroup-iostats-per-host.md"
---

内存量以 MB 为单位。

> [!NOTE]
> 只有启用基于资源组的资源管理时，`gp_resgroup_iostats_per_host` 视图才有效。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`rsgname`|name| pg_resgroup.rsgname|资源组的名称|
|`hostname`|text|gp_segment_configuration.hostname|Segment 主机的主机名|
|`tablespace`|text|pg_tablespace.spcname|表空间的名称|
|`rbps`|bigint| |资源组在某台主机上的实时顺序磁盘读 I/O 吞吐量，以 Bytes/s 为单位|
|`wbps`|bigint| |资源组在某台主机上的实时顺序磁盘写 I/O 吞吐量，以 Bytes/s 为单位|
|`riops`|bigint| |资源组在某台主机上实时每秒执行的读 I/O 操作数|
|`wiops`|bigint| |资源组在某台主机上实时每秒执行的写 I/O 操作数|

`gp_resgroup_iostats_per_host` 视图的示例输出：

```sql
SELECT * from gp_toolkit.gp_resgroup_iostats_per_host;

rsgname        | hostname | tablespace       | rbps | wbps | riops | wiops  
----------------+----------+------------------+------------------+------------------+-------------+-------------
rg_test_group1 | mtspc    | pg_default       | 21356347                | 29369067                | 162           | 36           
rg_test_group2 | mtspc    | pg_default       | 0                | 0                | 0           | 0           
rg_test_group3 | mtspc    | pg_default       | 0                | 0                | 0           | 0           
rg_test_group4 | mtspc    | *                | 0                | 0                | 0           | 0           
rg_test_group5 | mtspc    | rg_io_limit_ts_1 | 0                | 0                | 0           | 0           
(5 rows)
```
