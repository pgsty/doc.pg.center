---
title: yezzey
description: yezzey 将 AO 表（行存和列存）的数据转存到兼容 S3 的对象存储。
weight: 290
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/yezzey.md
---

`yezzey` 模块将 AO 表（行存和列存）的数据转存（offload）到兼容 S3 的对象存储。转存后的表保留其定义，仍存在于数据库中。可以继续使用相同的 SQL 语句查询和修改它，Apache Cloudberry 会在对象存储中读写其数据文件，而非在 Segment 的本地磁盘上读写。

使用 `yezzey` 可以将冷数据移至成本更低的存储，减少集群所需的磁盘空间。

> [!NOTE]
> `yezzey` 在 [open-gpdb/yezzey](https://github.com/open-gpdb/yezzey) 项目中开发。Apache Cloudberry 源码树通过 `gpcontrib/yezzey` 中的 Git 子模块引用它。Apache Cloudberry 2.2 固定使用 `yezzey` 2.0。

## 工作原理 {#how-it-works}

`yezzey` 由以下部分组成：

- AO 表的存储管理器。加载 `yezzey` 库时，它以钩子形式安装，将已转存表的文件操作重定向到对象存储。
- `yezzey` 扩展，提供管理转存的函数和元数据表。
- [YProxy](https://github.com/open-gpdb/yproxy)，运行在集群主机上的独立服务。Segment 不直接连接对象存储，而是通过 Unix 域套接字将所有请求发送给 YProxy；YProxy 维护到对象存储的连接池并调度请求。

转存表时：

1. `yezzey` 获取该表的排他锁。
2. 将所有 Segment 上该表的数据文件上传到对象存储。
3. 将表的表空间改为 `yezzey` 虚拟表空间（OID 为 `8555`）。
4. 提交事务。

转存后，新插入表的数据写入对象存储。对象存储中的文件从不原地修改：每次写入都会创建新文件，`yezzey` 将这些文件记录在遵循数据库 MVCC 规则的元数据表——虚拟索引中。不再被引用的文件成为垃圾，可使用[移除过时文件](#remove-obsolete-files)中介绍的清理函数移除。

## 构建与安装 {#build-and-install}

`yezzey` 默认不构建。

1. 在 Apache Cloudberry 源码树中获取子模块：

    ```shell
    git submodule update --init gpcontrib/yezzey
    ```

2. 使用 `--with-yezzey` 选项配置 Apache Cloudberry，然后构建并安装。`--with-yezzey` 要求 OpenSSL 支持（`--with-ssl=openssl`）和 C++11 编译器：

    ```shell
    ./configure --with-yezzey --with-ssl=openssl [other options...]
    make
    make install
    ```

    要在已有构建树上只构建此模块：

    ```shell
    make -C gpcontrib/yezzey
    make -C gpcontrib/yezzey install
    ```

3. 在集群的每台主机上构建并安装 YProxy。操作说明见 [YProxy](https://github.com/open-gpdb/yproxy) 项目。

## 设置 {#set-up}

### 配置并启动 YProxy {#configure-and-start-yproxy}

YProxy 读取定义套接字和对象存储的 YAML 配置文件。以下示例基于 `yezzey` 测试所用的配置：

```yaml
socket_path: "/tmp/yproxy.sock"
interconnect_socket_path: "/tmp/ic.sock"
log_level: info

storage:
  access_key_id: "<access key ID>"
  secret_access_key: "<secret access key>"
  storage_endpoint: "<endpoint URL>"
  storage_prefix: ""
  storage_bucket: "<bucket>"
  storage_region: "<region>"
  storage_type: "s3"
  tablespace_map:
    "pg_default": "<bucket>"

backup_storage:
  access_key_id: "<access key ID>"
  secret_access_key: "<secret access key>"
  storage_endpoint: "<endpoint URL>"
  storage_prefix: ""
  storage_bucket: "<bucket>"
  storage_region: "<region>"
  storage_type: "s3"
```

`tablespace_map` 将表转存前所在的表空间映射到接收其数据的存储桶。对于每个包含待转存表的表空间，都要添加一个条目。

在每台主机上启动 YProxy，并确保运行 Apache Cloudberry 的操作系统用户可以访问该套接字：

```shell
yproxy -c /path/to/yproxy.yaml
```

完整的 YProxy 设置列表见 YProxy 文档。

### 启用模块 {#enable-the-module}

1. 将 `yezzey` 加入 `shared_preload_libraries` 并重启集群。此库拒绝以其他方式加载：

    ```shell
    gpconfig -c shared_preload_libraries -v yezzey
    gpstop -ar
    ```

    如果 `shared_preload_libraries` 已列出其他库，请在其值中保留它们。

2. 设置环境所需的配置参数，并重新加载配置。至少检查 `yezzey.yproxy_socket` 和 `yezzey.use_gpg_crypto`：

    ```shell
    gpconfig -c yezzey.yproxy_socket -v "/tmp/yproxy.sock"
    gpstop -u
    ```

    `yezzey.use_gpg_crypto` 默认为 `on`，要求在 YProxy 配置的 `crypto` 部分设置 GPG 密钥（`gpg_key_id` 和 `gpg_key_path`）。没有密钥时，`yezzey.offload_relation()` 会报错 `failed to offload relation`。如果不加密数据，请关闭此参数：

    ```shell
    gpconfig -c yezzey.use_gpg_crypto -v false
    gpstop -u
    ```

3. 在每个需要转存表的数据库中创建扩展：

    ```sql
    CREATE EXTENSION yezzey;
    ```

    扩展创建 `yezzey` 模式，并将其 `USAGE` 权限授予 `PUBLIC`。此扩展标为可信，因此拥有数据库 `CREATE` 权限的非超级用户也可以创建。

    > [!NOTE]
    > `PUBLIC` 可以执行扩展的函数，且 `yezzey.offload_relation()` 和 `yezzey.load_relation()` 不检查表的所有权。如果只允许管理员转存、回载或清理表，请从 `PUBLIC` 撤销这些函数的 `EXECUTE` 权限。

## 配置参数 {#configuration-parameters}

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `yezzey.yproxy_socket` | 字符串 | `/tmp/yproxy.sock` | YProxy 的 Unix 域套接字路径。 |
| `yezzey.use_gpg_crypto` | 布尔值 | `on` | 要求 YProxy 在将数据写入对象存储时通过 GPG 加密。密钥在 YProxy 配置的 `crypto` 部分设置。 |
| `yezzey.storage_class` | 字符串 | `STANDARD` | `yezzey` 写入对象的默认存储类别。 |
| `yezzey.multipart_chunksize` | 整数 | `16777216` | 分段上传的默认块大小，单位为字节。 |
| `yezzey.multipart_threshold` | 整数 | `67108864` | 分段上传的默认大小阈值，单位为字节。 |
| `yezzey.use_otm_feature` | 布尔值 | `off` | 启用转存表空间映射。为 `off` 时，只能转存默认表空间中的表；为 `on` 时，也可以转存其他表空间中的表，`yezzey` 会在 `yezzey.offload_tablespace_map` 中记录各表原来的表空间。此参数只能在连接启动时或服务器配置中设置。 |
| `yezzey.log_level` | 枚举 | `debug1` | `yezzey` 函数消息的日志级别。 |
| `yezzey.ao_log_level` | 枚举 | `debug1` | 已转存文件读写操作消息的日志级别。 |
| `yezzey.autooffload` | 布尔值 | `off` | 保留参数。已定义，但此版本未使用。 |

除 `yezzey.use_otm_feature` 和 `yezzey.autooffload` 外，其他参数只有超级用户可以更改。

## 转存表 {#offload-a-table}

`yezzey` 只支持 AO 表，包括行存和列存。

要转存已有表，调用 `yezzey.offload_relation()`：

```sql
CREATE TABLE sales_archive (id int, amount numeric)
    WITH (appendonly=true) DISTRIBUTED BY (id);
INSERT INTO sales_archive SELECT i, i FROM generate_series(1, 100000) i;

SELECT yezzey.offload_relation('sales_archive');
```

函数通过每个 Segment 发出的 `NOTICE` 消息报告进度。所需时间取决于表大小。如果表已转存，函数会返回并给出警告 `The relation has already been offloaded`。

也可以直接在 `yezzey` 虚拟表空间中创建从一开始就转存到对象存储的表：

```sql
CREATE TABLE regao_tt_alr_off (i int)
    WITH (appendonly=true)
    TABLESPACE yezzey
    DISTRIBUTED BY (i);

INSERT INTO regao_tt_alr_off SELECT generate_series(1,10010);

SELECT segindex, local_bytes, external_bytes
FROM yezzey.offload_relation_status('regao_tt_alr_off');
```

```text
 segindex | local_bytes | external_bytes
----------+-------------+----------------
        0 |           0 |          33816
        1 |           0 |          33928
        2 |           0 |          32560
(3 rows)
```

表转存后，仍可对它执行 `SELECT`、`INSERT`、`UPDATE`、`DELETE`、`VACUUM` 和 `ALTER TABLE ... ADD COLUMN`。

要转存分区表，需分别转存各个叶子分区。对分区表本身调用 `yezzey.offload_relation()` 会失败。

## 将表回载到本地存储 {#load-a-table-back-to-local-storage}

要将已转存表的数据移回 Segment 的本地磁盘，调用 `yezzey.load_relation()`：

```sql
SELECT yezzey.load_relation('sales_archive');
```

下载耗时取决于表大小和段文件数量。此前上传的文件仍留在对象存储中，因此 `yezzey.offload_relation_status()` 中的 `external_bytes` 不会重置为 `0`。

## 检查表状态 {#check-the-status-of-a-table}

`yezzey.offload_relation_status()` 为每个 Segment 返回一行：

```sql
SELECT * FROM yezzey.offload_relation_status('sales_archive');
```

| 列 | 说明 |
|---|---|
| `reloid` | 表的 OID。 |
| `segindex` | Segment 内容 ID。 |
| `local_bytes` | 本地磁盘上存储的数据大小。`0` 表示表已完全转存。 |
| `local_commited_bytes` | 本地磁盘上已提交的数据大小。 |
| `external_bytes` | 对象存储中的数据大小。所有 Segment 均为 `0` 表示表从未转存过。 |
| `external_bloat_bytes` | 对象存储中不再使用但尚未删除的数据大小。 |

要查看更多细节，使用 `yezzey.offload_relation_status_per_filesegment()`，它为每个段文件返回一行；或使用 `yezzey.relation_describe_external_storage_structure()`，它为对象存储中的每个文件返回一行，包括其路径。

`yezzey.offload_metadata` 表列出通过 `yezzey.offload_relation()` 转存的表，不包括直接在 `yezzey` 表空间中创建的表。该表的 `SELECT` 权限授予 `PUBLIC`。

## 移除过时文件 {#remove-obsolete-files}

删除行或删除表时，不会删除对象存储中的数据，因为回滚事务或恢复备份时可能仍需这些文件。以下函数向 YProxy 发送删除过时文件的请求，在所有 Segment 上运行。

| 函数 | 范围 |
|---|---|
| `yezzey.vacuum(confirm boolean DEFAULT false, crazyDrop boolean DEFAULT false)` | 所有表空间。 |
| `yezzey.vacuum_tablespace(tablespace oid, confirm boolean DEFAULT false, crazyDrop boolean DEFAULT false)` | 一个表空间。 |
| `yezzey.vacuum_relation(relation regclass, confirm boolean DEFAULT false, crazyDrop boolean DEFAULT false)` | 一张已转存的表。 |

- `confirm` 控制 YProxy 是否实际删除对象。默认值 `false` 表示试运行，设为 `true` 才确认删除。
- `crazyDrop` 启用更激进的清理模式，只有超级用户可以将其设为 `true`。

典型的清理过程如下：

1. 对 AO 表运行 `VACUUM`，使其过时文件成为垃圾。
2. 通过 `yezzey.relation_describe_external_storage_structure('<table>')` 检查表的存储情况。
3. 根据需要清理的范围，调用 `yezzey.vacuum_relation()`、`yezzey.vacuum_tablespace()` 或 `yezzey.vacuum()`。
4. 再次检查表的存储情况，确认过时文件已移除。

默认情况下，YProxy 会保留备份可能仍需要的文件。控制此行为的设置见 YProxy 配置的 `vacuum` 部分。

## 函数参考 {#function-reference}

所有函数均位于 `yezzey` 模式中。

| 函数 | 返回值 | 说明 |
|---|---|---|
| `offload_relation(relation regclass)` | `void` | 将 AO 表转存到对象存储。 |
| `load_relation(relation regclass)` | `void` | 将已转存的表回载到本地存储。 |
| `offload_relation_status(relation regclass)` | 行集合 | 按 Segment 返回表的本地和外部大小。 |
| `offload_relation_status_per_filesegment(relation regclass)` | 行集合 | 按段文件返回表的本地和外部大小。 |
| `relation_describe_external_storage_structure(relation regclass)` | 行集合 | 对象存储中该表的文件，以及各文件的路径和大小。 |
| `vacuum(confirm boolean, crazyDrop boolean)` | `boolean` 集合 | 移除所有表空间中的过时文件。 |
| `vacuum_tablespace(tablespace oid, confirm boolean, crazyDrop boolean)` | `boolean` 集合 | 移除一个表空间中的过时文件。 |
| `vacuum_relation(relation regclass, confirm boolean, crazyDrop boolean)` | `boolean` 集合 | 移除一张已转存表的过时文件。 |

扩展还创建内部函数和元数据表，例如 `yezzey.yezzey_virtual_index`、`yezzey.yezzey_expire_index` 和 `yezzey.offload_tablespace_map`。不要直接调用内部函数或修改元数据表。

## 使用说明 {#usage-notes}

- 只能转存 AO 表。
- 要转存不在默认表空间中的表，需开启 `yezzey.use_otm_feature`，否则会拒绝转存。
- 不能通过 `ALTER TABLE ... SET TABLESPACE` 将已转存表移到另一个表空间，此语句会失败。请使用 `yezzey.load_relation()` 将数据回载到本地存储。
- 访问已转存表之前，YProxy 必须在每台主机上运行。如果 YProxy 或对象存储不可用，`yezzey` 最多重试读取请求 100 次。
- 转存期间会持有表的排他锁，直到上传结束。
- 从备份恢复集群时，对象存储中必须保留备份引用的文件。因此，只有不再有备份需要过时文件时，才能删除它们。
- 对于从主集群接收 WAL 的备集群，备集群也必须能够访问对象存储。
