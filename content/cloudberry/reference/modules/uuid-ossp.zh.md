---
title: uuid-ossp
description: uuid-ossp 提供使用多种标准算法生成通用唯一标识符（UUID）的函数。
weight: 280
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/uuid-ossp.md
---

`uuid-ossp` 模块提供使用多种标准算法生成通用唯一标识符（UUID）的函数，还包含生成某些特殊 UUID 常量的函数。

Apache Cloudberry 的 `uuid-ossp` 模块与 PostgreSQL 的 `uuid-ossp` 模块等价，没有 MPP 特有的注意事项。

## 安装并注册模块 {#install-and-register-the-module}

只有在配置 Apache Cloudberry 时通过 `configure` 的 `--with-uuid=LIB` 选项指定 UUID 库，才会构建 `uuid-ossp`（`LIB` 为 `e2fs`、`bsd` 或 `ossp`）。它也不属于默认构建目标（`make` 和 `make install`）。如果 `CREATE EXTENSION` 报告该扩展不可用，请使用配置当前安装版本时所用的 Apache Cloudberry 源码树，构建并安装此模块：

```shell
make -C contrib/uuid-ossp install
```

集群的每台主机（Coordinator、Standby Coordinator 及所有 Segment 主机）上都必须有模块文件。`make install-world` 也会安装此模块。

然后在每个需要使用它的数据库中注册扩展。扩展名包含连字符，必须加引号：

```sql
CREATE EXTENSION "uuid-ossp";
```

## 函数 {#functions}

| 函数 | 说明 |
|----------|-------------|
| `uuid_generate_v1()` | 根据主机的 MAC 地址和时间戳生成版本 1 的 UUID。 |
| `uuid_generate_v1mc()` | 使用随机多播 MAC 地址生成版本 1 的 UUID。 |
| `uuid_generate_v3(namespace uuid, name text)` | 在指定命名空间中生成版本 3 的 UUID（MD5 哈希）。 |
| `uuid_generate_v4()` | 根据随机数生成版本 4 的 UUID。 |
| `uuid_generate_v5(namespace uuid, name text)` | 在指定命名空间中生成版本 5 的 UUID（SHA-1 哈希）。 |
| `uuid_nil()` | 返回 nil UUID 常量。 |
| `uuid_ns_dns()`, `uuid_ns_url()`, `uuid_ns_oid()`, `uuid_ns_x500()` | 返回表示 DNS、URL、ISO 对象标识符和 X.500 可分辨名称命名空间的常量。 |

> [!NOTE]
> 如果只需要随机生成的 UUID（版本 4），可以改用 [pgcrypto](/cloudberry/reference/modules/pgcrypto/) 模块的 `gen_random_uuid()` 函数。

## 模块文档 {#module-documentation}

此模块的详细信息，参见 PostgreSQL 文档中的 [uuid-ossp](https://www.postgresql.org/docs/14/uuid-ossp.html)。
