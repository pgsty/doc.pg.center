---
title: "配置 Azure 和 Google Cloud Storage 对象存储连接器（可选）"
description: "配置连接 Azure 和 Google Cloud Storage 的 PXF 连接器。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/configuring/objstore_cfg.md"
---

你可以使用 PXF 访问 Azure Data Lake Storage Gen2、Azure Blob Storage 和 Google Cloud Storage 对象存储。本主题介绍如何为这些外部数据源配置 PXF 连接器。

*如果不打算使用这些 PXF 对象存储连接器，则无需执行此步骤。*

## 关于对象存储配置 {#about-object-store-configuration}

要访问对象存储中的数据，必须提供服务器位置和客户端凭据。配置 PXF 对象存储连接器时，需要按照[配置 PXF 服务器](/cloudberry/pxf/administering/configuring/cfg_server/)中的说明，为该连接器添加至少一个具名 PXF 服务器配置。

PXF 为每个对象存储连接器提供了一个模板配置文件。这些模板文件位于 `<PXF_INSTALL_DIR>/templates/` 目录中。


### Azure Blob Storage 服务器配置 {#azure-blob-storage-server-configuration}

Azure Blob Storage 的模板配置文件是 `<PXF_INSTALL_DIR>/templates/wasbs-site.xml`。配置 Azure Blob Storage 服务器时，必须提供以下服务器配置属性，并将模板值替换为你的账户名称：

| 属性 | 说明 | 值 |
|----------------|--------------------------------------------|-------|
| fs.adl.oauth2.access.token.provider.type | 令牌类型。 | 必须指定 `ClientCredential`。 |
| fs.azure.account.key.\<YOUR_AZURE_BLOB_STORAGE_ACCOUNT_NAME\>.blob.core.windows.net | Azure 账户密钥。 | 将 `<YOUR_AZURE_BLOB_STORAGE_ACCOUNT_NAME>` 替换为你的账户密钥。 |
| fs.AbstractFileSystem.wasbs.impl | 文件系统类名。 | 必须指定 `org.apache.hadoop.fs.azure.Wasbs`。 |


### Azure Data Lake Storage Gen2 服务器配置 {#azure-data-lake-storage-gen2-server-configuration}

Azure Data Lake Storage Gen2 的模板配置文件是 `<PXF_INSTALL_DIR>/templates/abfss-site.xml`。配置 Azure Data Lake Storage Gen2 服务器时，必须提供以下服务器配置属性，并将模板值替换为你的凭据：

| 属性 | 说明 | 值 |
|----------------|--------------------------------------------|-------|
| fs.azure.account.auth.type | 账户授权类型。 | 必须指定 `OAuth`。 |
| fs.azure.account.oauth.provider.type | 令牌类型。 | 必须指定 `org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider`。 |
| fs.azure.account.oauth2.client.endpoint | 要连接的 Azure 端点。 | 你的刷新 URL。 |
| fs.azure.account.oauth2.client.id | Azure 账户客户端 ID。 | 你的客户端 ID (UUID)。 |
| fs.azure.account.oauth2.client.secret | Azure 账户客户端 ID 的密码。 | 你的密码。 |


### Google Cloud Storage 服务器配置 {#google-cloud-storage-server-configuration}

Google Cloud Storage 的模板配置文件是 `<PXF_INSTALL_DIR>/templates/gs-site.xml`。配置 Google Cloud Storage 服务器时，必须提供以下服务器配置属性，并将模板值替换为你的凭据：

| 属性 | 说明 | 值 |
|----------------|--------------------------------------------|-------|
| google.cloud.auth.service.account.enable | 启用服务账户授权。 | 必须指定 `true`。 |
| google.cloud.auth.service.account.json.keyfile | Google Storage 密钥文件。 | 你的密钥文件路径。 |
| fs.AbstractFileSystem.gs.impl | 文件系统类名。 | 必须指定 `com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS`。 |


## 服务器配置示例步骤 {#example-server-configuration-procedure}

在本步骤中，你将为 Google Cloud Storage (GCS) 连接器命名并在 Apache Cloudberry Coordinator 主机的 `$PXF_BASE/servers` 目录中添加一个 PXF 服务器配置。然后使用 `pxf cluster sync` 命令将服务器配置同步到 Apache Cloudberry 集群。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 为服务器选择一个名称。你需要把该名称提供给需要引用对象存储中文件的最终用户。

3. 创建 `$PXF_BASE/servers/<server_name>` 目录。例如，使用以下命令为名为 `gs_public` 的 Google Cloud Storage 服务器创建服务器配置：

    ```shell
    gpadmin@coordinator$ mkdir $PXF_BASE/servers/gs_public
    ````

3. 将 GCS 的 PXF 模板文件复制到服务器配置目录。例如：

    ```shell
    gpadmin@coordinator$ cp <PXF_INSTALL_DIR>/templates/gs-site.xml $PXF_BASE/servers/gs_public/
    ```
        
4. 在你选择的编辑器中打开模板服务器配置文件，并根据你的环境提供适当的属性值。例如，如果 Google Cloud Storage 密钥文件位于 `/home/gpadmin/keys/gcs-account.key.json`：

    ```text
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
        <property>
            <name>google.cloud.auth.service.account.enable</name>
            <value>true</value>
        </property>
        <property>
            <name>google.cloud.auth.service.account.json.keyfile</name>
            <value>/home/gpadmin/keys/gcs-account.key.json</value>
        </property>
        <property>
            <name>fs.AbstractFileSystem.gs.impl</name>
            <value>com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS</value>
        </property>
    </configuration>
    ```
5. 保存更改并退出编辑器。

4. 使用 `pxf cluster sync` 命令，将新的服务器配置复制到 Apache Cloudberry 集群：
    
    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```
