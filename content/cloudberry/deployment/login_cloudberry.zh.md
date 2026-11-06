---
title: "登录 Apache Cloudberry"
description: "至此，您已成功部署 Apache Cloudberry。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/login_cloudberry.md"
---

可参考以下命令登录数据库：

```bash
psql -h <hostname> -p <port> -U <username> -d <database>
```

在上述命令中：

- `<hostname>` 是 Apache Cloudberry 服务器的 Coordinator 节点 IP 地址。
- `<port>` 是 Apache Cloudberry 的端口号，默认为 `5432`。
- `<username>` 是数据库用户名。
- `<database>` 是要连接的数据库名称。

运行 `psql` 命令后，系统会提示输入数据库密码。输入正确密码后，即可成功登录 Apache Cloudberry，并执行 SQL 查询和操作。请确保具有访问目标数据库所需的权限。

```sql
[gpadmin@cdw ~]$ psql warehouse
psql (14.4, server 14.4)
Type "help" for help.

warehouse=# SELECT * FROM gp_segment_configuration;
 dbid | content | role | preferred_role | mode | status | port | hostname | address |          datadir          | warehouseid
------+---------+------+----------------+------+--------+------+----------+---------+---------------------------+-------------
    1 |      -1 | p    | p              | n    | u      | 5432 | cdw      | cdw     | /data/coordinator/gpseg-1 |           0
    2 |       0 | p    | p              | s    | u      | 6000 | sdw1     | sdw1    | /data/primary/gpseg0      |           0
    8 |       0 | m    | m              | s    | u      | 7000 | sdw2     | sdw2    | /data/mirror/gpseg0       |           0
    3 |       1 | p    | p              | s    | u      | 6001 | sdw1     | sdw1    | /data/primary/gpseg1      |           0
    9 |       1 | m    | m              | s    | u      | 7001 | sdw3     | sdw3    | /data/mirror/gpseg1       |           0
    4 |       2 | p    | p              | s    | u      | 6000 | sdw2     | sdw2    | /data/primary/gpseg2      |           0
   10 |       2 | m    | m              | s    | u      | 7000 | sdw3     | sdw3    | /data/mirror/gpseg2       |           0
    5 |       3 | p    | p              | s    | u      | 6001 | sdw2     | sdw2    | /data/primary/gpseg3      |           0
   11 |       3 | m    | m              | s    | u      | 7001 | sdw1     | sdw1    | /data/mirror/gpseg3       |           0
    6 |       4 | p    | p              | s    | u      | 6000 | sdw3     | sdw3    | /data/primary/gpseg4      |           0
   12 |       4 | m    | m              | s    | u      | 7000 | sdw1     | sdw1    | /data/mirror/gpseg4       |           0
    7 |       5 | p    | p              | s    | u      | 6001 | sdw3     | sdw3    | /data/primary/gpseg5      |           0
   13 |       5 | m    | m              | s    | u      | 7001 | sdw2     | sdw2    | /data/mirror/gpseg5       |           0
(13 rows)
```
