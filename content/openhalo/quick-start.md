---
type: docs
upstream_source: openhalo
upstream_link: https://github.com/HaloTech-Co-Ltd/openHalo/blob/90fc8d777c3f111d4c8d236625bb15b5d4b19d7c/README.md
title: Build and configure OpenHalo
description: Build from source, enable MySQL compatibility, and connect with the mysql client.
weight: 10
---

This page preserves the source-build workflow from the openHalo README. For Halo Database 1.0.16's recommended MySQL endpoint configuration and connection rules, see [Configure MySQL compatibility](/openhalo/mysql-configuration/).

## Installation from source {#installation}
- uuid is mandatory.

```sh
./configure --prefix=/home/halo/openhalo/1.0 --enable-debug --with-uuid=ossp --with-icu CFLAGS=-O2
make && make install
cd contrib
make && make install
```

## Server setup {#server-setup}
- Create User & User Group
```sh
groupadd -g 1000 halo
useradd -u 1000 -g halo halo
```

- Setup Environment Variables
```sh
sudo mkdir /var/run/openhalo
sudo chown halo:halo /var/run/openhalo

export HALO_HOME=/home/halo/openhalo/1.0
export PGDATA=/home/halo/ohdata
export PATH=$HALO_HOME/bin:$PATH
export LD_LIBRARY_PATH=$HALO_HOME/lib
export PGHOST=/var/run/openhalo
```

- Initialize Database
```sh
pg_ctl init -D $PGDATA
```

- Server Configuration
```
...
database_compat_mode = 'mysql'                 # database compat mode, values can be:
                                               # mysql (mysql mode)
                                               # postgresql (default)

mysql.listener_on = true                       # (enable MySQL listener; change requires restart)
mysql.port = 3306                              # (port for MySQL; change requires restart)
...
```

- Start & Initialize MySQL Environment
```sql
psql -p 5432

# CREATE EXTENSION aux_mysql CASCADE;
```

- Query Database using mysql CLI
```sh
mysql -P 3306 -h 127.0.0.1 
```
![Query OpenHalo with the MySQL client](/openhalo/assets/mysql-query.png)

The source README uses `0/0` as a remote-login demonstration. Replace it with the smallest deployment CIDR and the authentication policy required by the exact build.

- Enable remote login with mysql CLI

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

Halo, HaloBase are trademarks of Halo Tech Co.,Ltd. <br/>
openHalo is a trademark of Halo Tech Co.,Ltd. <br/>
openHalo official website: https://www.openhalo.org
