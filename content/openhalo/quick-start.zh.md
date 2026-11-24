---
type: docs
upstream_source: openhalo
upstream_link: https://github.com/HaloTech-Co-Ltd/openHalo/blob/90fc8d777c3f111d4c8d236625bb15b5d4b19d7c/README.md
title: 编译与配置 OpenHalo（PG14 历史）
description: 历史上游 PG14 README 中的源码编译、database_compat_mode 配置与 mysql 客户端连接流程。
weight: 10
linkTitle: "PG14 构建（历史）"
---


> [!WARNING]
> **历史 PG14 指南 —— 不适用于 OpenHalo 18。** 本页保留上游 PostgreSQL 14 openHalo 在 `90fc8d7` 时的 README。文中的 `--with-uuid=ossp`、`database_compat_mode = 'mysql'` 与 `set password_encryption=mysql_native_password` 在 PGSTY OpenHalo 18 分支中均不存在，照搬执行会报错。OpenHalo 18 请使用[构建与配置](/openhalo/18/configuration/)。

本页保留 openHalo README 中的源码编译流程。Halo Database 1.0.16 推荐的 MySQL 端点配置和连接规则见[配置 MySQL 兼容](/openhalo/mysql-configuration/)。

## 从源码安装 {#installation}
- 必须安装 uuid。

```sh
./configure --prefix=/home/halo/openhalo/1.0 --enable-debug --with-uuid=ossp --with-icu CFLAGS=-O2
make && make install
cd contrib
make && make install
```

## 配置服务器 {#server-setup}
- 创建用户与用户组
```sh
groupadd -g 1000 halo
useradd -u 1000 -g halo halo
```

- 设置环境变量
```sh
sudo mkdir /var/run/openhalo
sudo chown halo:halo /var/run/openhalo

export HALO_HOME=/home/halo/openhalo/1.0
export PGDATA=/home/halo/ohdata
export PATH=$HALO_HOME/bin:$PATH
export LD_LIBRARY_PATH=$HALO_HOME/lib
export PGHOST=/var/run/openhalo
```

- 初始化数据库
```sh
pg_ctl init -D $PGDATA
```

- 配置服务器
```
...
database_compat_mode = 'mysql'                 # database compat mode, values can be:
                                               # mysql (mysql mode)
                                               # postgresql (default)

mysql.listener_on = true                       # (enable MySQL listener; change requires restart)
mysql.port = 3306                              # (port for MySQL; change requires restart)
...
```

- 启动并初始化 MySQL 环境
```sql
psql -p 5432

# CREATE EXTENSION aux_mysql CASCADE;
```

- 使用 mysql 命令行客户端查询数据库
```sh
mysql -P 3306 -h 127.0.0.1 
```
![使用 MySQL 客户端查询 OpenHalo](/openhalo/assets/mysql-query.png)

源码 README 使用 `0/0` 演示远程登录。实际部署时应改为最小的客户端网段，并根据当前构建使用所需的认证策略。

- 允许通过 mysql 命令行客户端远程登录

postgresql.conf
```
...
listen_addresses = '*'              # what IP address(es) to listen on;
                                    # comma-separated list of addresses;
                                    # defaults to 'localhost'; use '*' for all
                                    # (change requires restart)
...
```

```sh
pg_ctl restart 
```

pg_hba.conf
```
...
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
host    all             all             0/0                     md5
...
```

```sh
pg_ctl reload 
```

```sql
psql -p 5432

set password_encryption=mysql_native_password;

create user test password 'test';

select * from pg_shadow where usename='test';

```

```sh
mysql -P 3306 -h <Server IP> -utest -p
```

Halo、HaloBase 是 Halo Tech Co.,Ltd. 的商标。 <br/>
openHalo 是 Halo Tech Co.,Ltd. 的商标。 <br/>
openHalo 官方网站： https://www.openhalo.org
