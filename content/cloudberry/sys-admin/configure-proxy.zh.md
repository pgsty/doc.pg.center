---
title: "为 Interconnect 配置代理"
description: "可以配置 Cloudberry 系统使用互联代理进行互联通信，减少查询处理期间的连接和端口使用量。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/configure-proxy.md"
---

Cloudberry *Interconnect*（网络层）指 Segment 之间的进程间通信，以及这种通信所依赖的网络基础设施。有关 Cloudberry 架构和 Interconnect 的信息，参见 [Cloudberry 架构简介](/cloudberry/introduction/cbdb-architecture/)。

通常，运行查询时，Cloudberry Coordinator 上的 QD（查询分发器）会连接一个或多个 Segment 上的 QE（查询执行器）进程，QE 还可以连接其他 QE。有关 Cloudberry 查询处理和并行查询处理的说明，参见 [Cloudberry 查询处理简介](/cloudberry/performance/optimize-queries/parallel-query-execution/)。

默认情况下，Coordinator 上的 QD 与 Segment 实例上的 QE 之间，以及不同 Segment 实例上的 QE 之间的连接，都需要独立的网络端口。可以配置 Cloudberry 系统，在 QD 与 QE 之间以及不同 Segment 实例上的 QE 之间通信时使用代理。Interconnect 代理在两个 Segment 实例之间的 Cloudberry 内部通信中只需一个网络连接，因此比 `TCP` 模式占用更少的连接和端口，并且在高延迟网络中的性能优于 `UDPIFC` 模式。

要为 Cloudberry 系统启用 Interconnect 代理，请设置以下系统配置参数。

- 使用参数 `gp_interconnect_proxy_addresses` 列出代理端口。必须为 Coordinator、Standby Coordinator 以及所有 Segment 实例指定代理端口。
- 将参数 `gp_interconnect_type` 设置为 `proxy`。

> [!NOTE]
> 扩容 Apache Cloudberry 系统时，必须先停用 Interconnect 代理，再向系统添加新主机和 Segment 实例；重新启用 Interconnect 代理前，还必须使用新增 Segment 实例更新 `gp_interconnect_proxy_addresses` 参数。

## 示例 {#example}

本示例配置 Cloudberry 系统，使查询运行时的 Cloudberry Interconnect 使用代理。示例先设置 `gp_interconnect_proxy_addresses` 参数并测试代理，再为 Cloudberry 系统设置 `gp_interconnect_type` 参数。

- [设置 Interconnect 代理地址](#set-the-interconnect-proxy-addresses)
- [测试 Interconnect 代理](#test-the-interconnect-proxies)
- [为系统设置 Interconnect 代理](#set-interconnect-proxies-for-the-system)

### 设置 Interconnect 代理地址 {#set-the-interconnect-proxy-addresses}

设置 `gp_interconnect_proxy_addresses` 参数，为 Coordinator 和 Segment 实例指定代理端口。该值的语法格式如下，参数值必须是单引号字符串。

```
<db_id>:<cont_id>:<seg_address>:<port>[, ... ]
```

对于 Coordinator、Standby Coordinator 和 Segment 实例，前三个字段 db_id、cont_id 和 seg_address 可在 [`gp_segment_configuration`](/cloudberry/reference/sys-catalogs/sys-tables/gp-segment-configuration/) 目录表中找到。第四个字段 port 是为 Cloudberry Coordinator 或 Segment 实例指定的代理端口。

- db_id 是目录表中的 `dbid` 列。
- cont_id 是目录表中的 `content` 列。
- seg_address 是与目录表中 `address` 列对应的 IP 地址或主机名。
- port 是所指定 Segment 实例代理的 TCP/IP 端口。

> [!NOTE]
> 如果 Segment 实例主机名在运行时绑定到不同的 IP 地址，必须运行 `gpstop -u`，重新加载 `gp_interconnect_proxy_addresses` 的值。

以下 PL/Python 函数示例用于显示或设置 `gp_interconnect_proxy_addresses` 参数的 Segment 实例代理端口值。要创建并运行此函数，必须先在数据库中使用 `CREATE EXTENSION plpython3u` 命令启用 PL/Python。

```sql
--
-- A PL/Python function to setup the interconnect proxy addresses.
-- Requires the Python modules os and socket.
--
-- Usage:
--   select my_setup_ic_proxy(-1000, '');              -- display IC proxy values for segments
--   select my_setup_ic_proxy(-1000, 'update proxy');  -- update the gp_interconnect_proxy_addresses parameter
--
-- The first argument, "delta", is used to calculate the proxy port with this formula:
--
--   proxy_port = postmaster_port + delta
--
-- The second argument, "action", is used to update the gp_interconnect_proxy_addresses parameter.
-- The parameter is not updated unless "action" is 'update proxy'.
-- Note that running  "gpstop -u" is required for the update to take effect. 
-- A Cloudberry system restart will also work.
--
create or replace function my_setup_ic_proxy(delta int, action text)
returns table(dbid smallint, content smallint, address text, port int) as $$
    import os
    import socket

    results = []
    value = ''

    segs = plpy.execute('''SELECT dbid, content, port, address
                              FROM gp_segment_configuration
                            ORDER BY 1''')
    for seg in segs:
        dbid = seg['dbid']
        content = seg['content']
        port = seg['port']
        address = seg['address']

        # decide the proxy port
        port = port + delta

        # append to the result list
        results.append((dbid, content, address, port))

        # build the value for the GUC
        if value:
            value += ','
        value += '{}:{}:{}:{}'.format(dbid, content, address, port)

    if action.lower() == 'update proxy':
        os.system('''gpconfig --skipvalidation -c gp_interconnect_proxy_addresses -v "'{}'"'''.format(value))
        plpy.notice('''the settings are applied, please reload with 'gpstop -u' to take effect.''')
    else:
        plpy.notice('''if the settings are correct, re-run with 'update proxy' to apply.''')
    return results
$$ language plpython3u execute on coordinator;
```

> [!NOTE]
> 运行该函数时，应使用 Cloudberry Interconnect 类型 `UDPIFC` 或 `TCP` 连接数据库。本示例使用 `psql` 以 `UDPIFC` Interconnect 类型连接数据库 `mytest`。

```shell
PGOPTIONS="-c gp_interconnect_type=udpifc" psql -d mytest
```

运行此命令会列出 `gp_interconnect_proxy_addresses` 参数的 Segment 实例值。

```sql
select my_setup_ic_proxy(-1000, '');
```

此命令运行该函数来设置参数。

```sql
select my_setup_ic_proxy(-1000, 'update proxy');
```

也可以运行 [`gpconfig`](/cloudberry/reference/sys-utilities/gpconfig/) 工具设置 `gp_interconnect_proxy_addresses` 参数。要将值设置为字符串，需将单引号字符串放在双引号中。本示例的 Cloudberry 系统包含一个 Coordinator 和一个 Segment 实例。

```shell
gpconfig --skipvalidation -c gp_interconnect_proxy_addresses -v "'1:-1:192.168.180.50:35432,2:0:192.168.180.54:35000'"
```

设置 `gp_interconnect_proxy_addresses` 参数后，使用 `gpstop -u` 命令重新加载 `postgresql.conf` 文件。该命令不会停止并重启 Cloudberry 系统。

### 测试 Interconnect 代理 {#test-the-interconnect-proxies}

要测试系统配置的代理端口，可以在命令 shell 中启动 `psql` 会话时设置 `PGOPTIONS` 环境变量。此命令设置该环境变量以启用 Interconnect 代理，启动 `psql` 并登录数据库 `mytest`。

```shell
PGOPTIONS="-c gp_interconnect_type=proxy" psql -d mytest
```

可以在 shell 中运行查询测试系统。例如，可以运行访问所有主 Segment 实例的查询。该查询显示 `sales` 表中每个 Segment 实例的 Segment ID 和行数。

```sql
# Select gp_segment_id, COUNT(*) FROM sales GROUP BY gp_segment_id ;
```

### 为系统设置 Interconnect 代理 {#set-interconnect-proxies-for-the-system}

测试系统的 Interconnect 代理后，使用 `gpconfig` 工具设置系统的服务器配置参数。

```shell
gpconfig -c  gp_interconnect_type -v proxy
```

使用 `gpstop -u` 命令重新加载 `postgresql.conf` 文件。该命令不会停止并重启 Cloudberry 系统。
