---
title: "配置 MinIO、AWS S3 和 Dell ECS 对象存储连接器（可选）"
description: "配置连接 MinIO 和 S3 对象存储的 PXF 连接器。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/configuring/s3_objstore_cfg.md"
---

你可以使用 PXF 访问兼容 S3 的对象存储。本主题介绍如何为这些外部数据源配置 PXF 连接器。

*如果不打算使用这些 PXF 对象存储连接器，则无需执行此步骤。*

## 关于对象存储配置 {#about-object-store-configuration}

要访问对象存储中的数据，必须提供服务器位置和客户端凭据。配置 PXF 对象存储连接器时，需要按照[配置 PXF 服务器](/cloudberry/pxf/administering/configuring/cfg_server/)中的说明，为该连接器添加至少一个具名 PXF 服务器配置。

PXF 为大多数对象存储连接器提供了配置文件模板。这些模板文件位于 `<PXF_INSTALL_DIR>/templates/` 目录中。


## MinIO 服务器配置 {#minio-server-configuration}

MinIO 的模板配置文件是 `<PXF_INSTALL_DIR>/templates/minio-site.xml`。配置 MinIO 服务器时，必须提供以下服务器配置属性，并将模板值替换为你的凭据：

| 属性 | 说明 | 值 |
|----------------|--------------------------------------------|------ |
| fs.s3a.endpoint | 要连接的 MinIO S3 端点。 | 你的端点。 |
| fs.s3a.access.key | MinIO 账户访问密钥。 | 你的 MinIO 用户名。 |
| fs.s3a.secret.key | 与访问密钥关联的 MinIO 秘密密钥。 | 你的 MinIO 密码。 |
| fs.s3a.fast.upload | 控制快速上传的属性；默认值为 `false`。 | 设置为 `true` 以启用快速上传。 |
| fs.s3a.path.style.access | 控制通过路径指定文件的属性；默认值为 `false`。 | 设置为 `true` 以启用路径样式访问。 |

## S3 服务器配置 {#s3-server-configuration}

S3 的模板配置文件是 `<PXF_INSTALL_DIR>/templates/s3-site.xml`。配置 S3 服务器时，必须提供以下服务器配置属性，并将模板值替换为你的凭据：

| 属性 | 说明 | 值 |
|----------------|--------------------------------------------|-------|
| fs.s3a.access.key | AWS 账户访问密钥 ID。 | 你的访问密钥。 |
| fs.s3a.secret.key | 与 AWS 访问密钥 ID 关联的秘密密钥。 | 你的秘密密钥。 |

如有需要，可以通过在 `s3-site.xml` 服务器配置文件中指定 Hadoop-AWS 模块文档 [S3A](https://hadoop.apache.org/docs/current/hadoop-aws/tools/hadoop-aws/index.html#S3A) 一节中列出的属性，对 PXF 的 S3 连接进行微调。

你可以通过在 `CREATE EXTERNAL TABLE` 命令的 `LOCATION` 子句中使用自定义选项直接指定 S3 访问 ID 和秘密密钥，覆盖 S3 服务器配置的凭据。有关更多信息，请参阅[为外部表覆盖 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-external-tables)。


### 配置 S3 服务端加密 {#configuring-s3-server-side-encryption}

对于通过指定 `pxf` 协议和 `s3:*` Profile 的可读和可写 Apache Cloudberry 外部表访问的 S3 文件，PXF 支持 Amazon Web Service S3 服务端加密（SSE）。AWS S3 服务端加密保护静态数据；它在将对象数据写入磁盘时进行加密，并在你访问数据时为你透明地解密。

PXF 支持以下 AWS SSE 加密密钥管理方案：

- 使用 S3 托管密钥的 SSE（SSE-S3）- 由 Amazon 管理数据密钥和主加密密钥。
- 使用密钥管理服务托管密钥的 SSE（SSE-KMS）- 由 Amazon 管理数据密钥，你在 AWS KMS 中管理加密密钥。
- 使用客户提供密钥的 SSE（SSE-C）- 由你设置并管理加密密钥。

无论数据是否加密，你的 S3 访问密钥和秘密密钥都控制你对所有 S3 存储桶对象的访问。

对于通过指定 `pxf` 协议和 `s3:*` Profile 创建的可读外部表访问的加密文件，S3 在读取操作期间会透明地解密数据。无需额外配置。

要加密通过此类外部表写入 S3 的数据，有两种选择：

- 通过 AWS 控制台或命令行工具，按 S3 存储桶配置默认的 SSE 加密密钥管理方案（推荐）。
- 在 PXF S3 服务器的 `s3-site.xml` 配置文件中配置 SSE 加密选项。

#### 通过 S3 存储桶策略配置 SSE（推荐） {#configuring-sse-via-an-s3-bucket-policy-recommended}

你可以创建 S3 <i>存储桶策略（Bucket Policy）</i>，指定要加密的对象、加密密钥管理方案以及对这些对象允许的写操作。有关 SSE 加密密钥管理方案的更多信息，请参阅 AWS S3 文档中的 [Protecting Data Using Server-Side Encryption](http://docs.aws.amazon.com/AmazonS3/latest/dev/serv-side-encryption.html)。[How Do I Enable Default Encryption for an S3 Bucket?](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/default-bucket-encryption.html) 介绍了如何设置默认加密存储桶策略。


#### 在 PXF S3 服务器配置中指定 SSE 选项 {#specifying-sse-options-in-a-pxf-s3-server-configuration}

要在 PXF S3 服务器配置中配置服务端加密，必须在 `s3-site.xml` 中包含某些属性。你添加到文件中的属性和值取决于 SSE 加密密钥管理方案。

**SSE-S3**

要对写入任何 S3 存储桶的任何文件启用 SSE-S3，请在 `s3-site.xml` 文件中设置以下加密算法属性和值：

```xml
<property>
  <name>fs.s3a.server-side-encryption-algorithm</name>
  <value>AES256</value>
</property>
```

要对特定 S3 存储桶启用 SSE-S3，请使用包含存储桶名称的属性名变体。例如：

```xml
<property>
  <name>fs.s3a.bucket.YOUR_BUCKET1_NAME.server-side-encryption-algorithm</name>
  <value>AES256</value>
</property>
```

将 `YOUR_BUCKET1_NAME` 替换为 S3 存储桶的名称。

**SSE-KMS**

要对写入任何 S3 存储桶的任何文件启用 SSE-KMS，请同时设置加密算法和加密密钥 ID。在 `s3-site.xml` 文件中设置这些属性：

```xml
<property>
  <name>fs.s3a.server-side-encryption-algorithm</name>
  <value>SSE-KMS</value>
</property>
<property>
  <name>fs.s3a.server-side-encryption.key</name>
  <value>YOUR_AWS_SSE_KMS_KEY_ARN</value>
</property>
```

将 `YOUR_AWS_SSE_KMS_KEY_ARN` 替换为你的密钥资源名称。如果不指定加密密钥，则使用 Amazon KMS 中定义的默认密钥。KMS 密钥示例：`arn:aws:kms:us-west-2:123456789012:key/1a23b456-7890-12cc-d345-6ef7890g12f3`。

**注意**：请务必在同一个 Amazon 可用区中创建存储桶和密钥。

要对特定 S3 存储桶启用 SSE-KMS，请使用包含存储桶名称的属性名变体。例如：

```xml
<property>
  <name>fs.s3a.bucket.YOUR_BUCKET2_NAME.server-side-encryption-algorithm</name>
  <value>SSE-KMS</value>
</property>
<property>
  <name>fs.s3a.bucket.YOUR_BUCKET2_NAME.server-side-encryption.key</name>
  <value>YOUR_AWS_SSE_KMS_KEY_ARN</value>
</property>
```

将 `YOUR_BUCKET2_NAME` 替换为 S3 存储桶的名称。

**SSE-C**

要对写入任何 S3 存储桶的任何文件启用 SSE-C，请同时设置加密算法和加密密钥（base-64 编码）。所有客户端必须共用同一个密钥。

在 `s3-site.xml` 文件中设置这些属性：

```xml
<property>
  <name>fs.s3a.server-side-encryption-algorithm</name>
  <value>SSE-C</value>
</property>
<property>
  <name>fs.s3a.server-side-encryption.key</name>
  <value>YOUR_BASE64-ENCODED_ENCRYPTION_KEY</value>
</property>
```

要对特定 S3 存储桶启用 SSE-C，请使用包含存储桶名称的属性名变体，具体方法如 SSE-KMS 示例所述。


## 服务器配置示例步骤 {#example-server-configuration-procedure}

在本步骤中，你将为 S3 Cloud Storage 连接器命名并在 Apache Cloudberry Coordinator 主机的 `$PXF_BASE/servers` 目录中添加一个 PXF 服务器配置。然后使用 `pxf cluster sync` 命令将服务器配置同步到 Apache Cloudberry 集群。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 为服务器选择一个名称。你需要把该名称提供给需要引用对象存储中文件的最终用户。

3. 创建 `$PXF_BASE/servers/<server_name>` 目录。例如，使用以下命令为名为 `s3srvcfg` 的 S3 服务器创建服务器配置：

    ```shell
    gpadmin@coordinator$ mkdir $PXF_BASE/servers/s3srvcfg
    ````

3. 将 S3 的 PXF 模板文件复制到服务器配置目录。例如：

    ```shell
    gpadmin@coordinator$ cp <PXF_INSTALL_DIR>/templates/s3-site.xml $PXF_BASE/servers/s3srvcfg/
    ```
        
4. 在你选择的编辑器中打开模板服务器配置文件，并根据你的环境提供适当的属性值。例如：

    ```text
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
        <property>
            <name>fs.s3a.access.key</name>
            <value>access_key_for_user1</value>
        </property>
        <property>
            <name>fs.s3a.secret.key</name>
            <value>secret_key_for_user1</value>
        </property>
        <property>
            <name>fs.s3a.fast.upload</name>
            <value>true</value>
        </property>
    </configuration>
    ```
5. 保存更改并退出编辑器。

4. 使用 `pxf cluster sync` 命令，将新的服务器配置复制到 Apache Cloudberry 集群：
    
    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

## Dell ECS 服务器配置 {#dell-ecs-server-configuration}

Dell ECS 没有模板服务器配置文件。你可以使用 MinIO 服务器配置模板 `<PXF_INSTALL_DIR>/templates/minio-site.xml`。

配置 Dell ECS 服务器时，必须提供以下服务器配置属性，并将模板值替换为你的凭据：

| 属性 | 说明 | 值 |
|----------------|--------------------------------------------|------ |
| fs.s3a.endpoint | 要连接的 Dell ECS S3 端点。 | 你的 ECS 端点。 |
| fs.s3a.access.key | Dell ECS 账户访问密钥。 | 你的 ECS 用户名。 |
| fs.s3a.secret.key | 与访问密钥关联的 Dell ECS 秘密密钥。 | 你的 ECS 秘密密钥1。 |
| fs.s3a.fast.upload | 控制快速上传的属性；默认值为 `false`。 | 设置为 `true` 以启用快速上传。 |
| fs.s3a.path.style.access | 控制通过路径指定文件的属性；默认值为 `false`。 | 设置为 `true` 以启用路径样式访问。 |
