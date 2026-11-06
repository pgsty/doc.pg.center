---
title: "透明数据加密"
description: "为满足保护用户数据安全的要求，Apache Cloudberry 支持透明数据加密（TDE）。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/security/transparent-data-encryption.md"
---

TDE 是一种用于加密数据库数据文件的技术：

- “数据”指数据库中的数据。
- 文件在硬盘上以密文存储，在内存中以明文处理。TDE 用于保护静态数据，因此也称为静态数据加密。
- “透明”意味着用户不需要改变操作习惯。TDE 自动管理加密/解密过程，无需用户或应用程序干预。

## 加密算法简介 {#introduction-to-encryption-algorithms}

### 基本概念 {#basic-concepts}

- DEK（数据加密密钥）：用于加密数据的密钥，由数据库生成并存储在内存中。
- DEK 明文：与 DEK 含义相同，但只能存储在内存中。
- 主密钥：用于加密 DEK 的密钥。
- DEK 密文：使用主密钥加密后的 DEK，持久化存储。

### 密钥管理模块 {#key-management-module}

密钥管理模块是 TDE 的核心组件，实现了主密钥和 DEK 两级密钥结构。主密钥用于加密 DEK，存储在数据库外部；DEK 用于加密数据库数据，以密文形式存储在数据库中。

### 算法分类 {#algorithm-classification}

加密算法分为以下类型：

- 对称加密：加密和解密使用相同的密钥。
- 非对称加密：使用公钥加密、私钥解密，适用于一对多和多对一的加密需求。

对称加密中的分组加密算法是主流选择，其性能优于流加密和非对称加密。Apache Cloudberry 支持 AES 和 SM4 两种分组加密算法。

#### AES 加密算法 {#aes-encryption-algorithm}

AES 是一种国际标准化的分组加密算法，支持 128、192 和 256 位密钥。常见的加密模式包括：

- ECB：电子密码本模式
- CBC：密码分组链接模式
- CFB：密码反馈模式
- OFB：输出反馈模式
- CTR：计数器模式

#### 更多 ISO/IEC 加密算法 {#more-isoiec-encryption-algorithms}

其他 ISO/IEC 加密算法包括：

- ISO/IEC 14888-3/AMD1（即 SM2）：非对称加密，基于 ECC，性能优于 RSA。
- ISO/IEC 10118-3:2018（即 SM3）：消息摘要算法，类似 MD5，输出长度为 256 位。
- ISO/IEC 18033-3:2010/AMD1:2021（即 SM4）：用于无线局域网标准的对称加密算法，支持 128 位的密钥和分组长度。

## 使用说明 {#user-instructions}

使用 TDE 功能前，请确保满足以下条件：

- 安装 OpenSSL：Apache Cloudberry 节点上应已安装 OpenSSL。通常，Linux 发行版会预装 OpenSSL。
- Apache Cloudberry 版本：确保 Apache Cloudberry 版本不低于 v1.6.0，TDE 支持从该版本引入。

部署 Apache Cloudberry 时，可以通过设置启用 TDE 功能，使后续所有数据加密操作对用户完全透明。要在数据库初始化时启用 TDE，请在 `gpinitsystem` 命令中使用 `-T` 参数。Apache Cloudberry 支持 AES 和 SM4 两种加密算法。以下是启用 TDE 的示例：

- 使用 AES256 加密算法：

    ```shell
    gpinitsystem -c gpinitsystem_config -T AES256
    ```

- 使用 SM4 加密算法：

    ```shell
    gpinitsystem -c gpinitsystem_config -T SM4
    ```

## 验证 TDE 是否生效 {#verify-tde-effectiveness}

透明数据加密功能对用户不可见，也就是说，启用或禁用此功能不会影响用户执行读写操作时的体验。不过，要验证加密是否生效，可以按照以下步骤模拟密钥文件丢失的场景，确认数据库在缺少密钥文件时无法启动。

密钥文件位于 Coordinator 节点上。要找到密钥文件，请先查找 Coordinator 节点的数据目录。例如：

```shell
COORDINATOR_DATA_DIRECTORY=/home/gpadmin/work/data0/master/gpseg-1
```

然后，查找密钥文件：

```shell
$ pwd
/home/gpadmin/work/data0/master/gpseg-1

$ ls -l pg_cryptokeys/live/
total 8
-rw------- 1 gpadmin gpadmin 48 Apr 12 10:26 relation.wkey
-rw------- 1 gpadmin gpadmin 48 Apr 12 10:26 wal.wkey
```

`relation.wkey` 文件中的密钥用于加密数据文件，而 `wal.wkey` 文件用于加密 WAL 日志。目前只有 `relation.wkey` 生效，WAL 日志尚未加密。

### 验证过程 {#verification-process}

1. 创建表并插入数据。

    - 创建仅追加（AO）表并插入数据：

        ```sql
        postgres=# create table ao2 (id int) with(appendonly=true);
        postgres=# insert into ao2 select generate_series(1,10);
        ```

    - 确保数据已成功插入。

2. 停止数据库。

    ```shell
    gpstop -a
    ```

3. 模拟密钥文件丢失。

    - 切换到存储密钥文件的目录：

        ```shell
        cd /home/gpadmin/work/data0/master/gpseg-1/pg_cryptokeys/
        ```

    - 将密钥文件移至其他目录（模拟密钥文件丢失）：

        ```shell
        mv live backup
        ```

4. 尝试启动数据库。

    - 使用 `gpstart` 命令启动数据库：

        ```shell
        gpstart -a
        ```

        由于缺少密钥文件，数据库将无法启动。在 Coordinator 节点的数据库日志中，会看到类似以下内容的错误：

        ```shell
        FATAL: cluster has no data encryption keys
        ```

        这证实了数据库在缺少密钥文件时无法启动，从而保障数据安全。

5. 将先前备份的密钥文件移回原目录，以恢复密钥文件：

    ```shell
    mv backup live
    ```

6. 重新启动数据库并验证数据。

    1. 再次使用 `gpstart` 命令启动数据库：

        ```shell
        gpstart -a
        ```

    2. 数据库成功启动后，查询 `ao2` 表以验证数据：

        ```sql
        postgres=# select * from ao2 order by id;
        id
        ----
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        (10 rows)
        ```

通过以上步骤，可以验证透明数据加密功能是否生效，确认数据库在缺少密钥文件时无法启动，从而保障静态数据的安全。
