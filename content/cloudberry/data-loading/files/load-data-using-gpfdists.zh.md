---
title: "使用 gpfdists 安全加载数据"
linkTitle: "使用 gpfdists 加载数据（安全）"
description: "`gpfdists` 协议是 `gpfdist` 协议的安全版本，可在 Apache Cloudberry 与 gpfdist 文件服务器之间实现加密通信。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/data-loading/load-data-using-gpfdists.md"
---

使用 `gpfdists` 时，所有数据传输都通过 SSL 加密，以防止窃听和中间人攻击。

`gpfdists` 提供与 `gpfdist` 相同的高性能并行数据加载能力，并增加了处理敏感数据的生产环境所必需的安全功能。

## 安全功能 {#security-features}

- Apache Cloudberry Segment 与 gpfdist 服务器之间传输的所有数据都使用 SSL/TLS 协议加密，以防止窃听和数据截获。
- 通过客户端证书强制执行双向认证，确保 Apache Cloudberry 和 gpfdist 服务器在建立连接之前互相验证身份。
- 该实现使用 TLSv1 协议和 AES_128_CBC_SHA 加密算法，为传输中的数据提供强加密保护。
- 安全的服务器身份识别机制可防止未经授权的系统冒充合法 gpfdist 服务器，从而抵御中间人攻击。

## 开始之前 {#before-you-begin}

要使用 `gpfdists`，请确保：

- 所有 Segment 主机都已配置 SSL 证书。
- 文件服务器主机上可使用 gpfdist 工具。
- Segment 主机与 gpfdist 服务器之间网络连通。
- 所需的 SSL 证书文件位于正确的位置。

## 步骤 1：设置 SSL 证书 {#step-1-set-up-ssl-certificates}

### 必需的证书文件 {#required-certificate-files}

每个 Apache Cloudberry Segment 主机的 `$PGDATA/gpfdists` 目录中必须存在以下证书文件：

#### 完整 SSL 认证（推荐）： {#for-full-ssl-authentication-recommended}

- `client.key`：客户端私钥文件
- `client.crt`：客户端证书文件
- `root.crt`：受信任的证书颁发机构（CA）的证书文件

#### 不同配置的证书要求： {#certificate-requirements-by-configuration}

| verify_gpfdists_cert | --ssl_verify_peer | 必需的证书文件 |
|---------------------|-------------------|---------------------------|
| on（默认） | on（默认） | `client.key`、`client.crt`、`root.crt` |
| on | off | `root.crt` |
| off | on | `client.key`、`client.crt` |
| off | off | 无 |

### 安装证书 {#install-certificates}

1. 在每个 Segment 主机上创建 gpfdists 目录：

    ```shell
    mkdir -p $PGDATA/gpfdists
    ```

2. 将证书文件复制到每个 Segment 主机：

    ```shell
    # Copy to all segment hosts
    scp client.key client.crt root.crt gpadmin@segment-host:$PGDATA/gpfdists/
    ```

3. 设置适当的权限：

    ```shell
    chmod 600 $PGDATA/gpfdists/client.key
    chmod 644 $PGDATA/gpfdists/client.crt
    chmod 644 $PGDATA/gpfdists/root.crt
    ```

## 步骤 2：启用 SSL 启动 gpfdist {#step-2-start-gpfdist-with-ssl}

使用 `--ssl` 选项启动 gpfdist 工具，以启用安全连接：

```shell
gpfdist -p 8081 -d /data/load_files --ssl /path/to/certificates &
```

### gpfdist 的 SSL 选项 {#ssl-options-for-gpfdist}

- `--ssl <certificates_path>`：启用 SSL 并指定证书目录
- `--ssl_verify_peer on|off`：控制对端验证（默认：on）

### 示例：启动多个安全的 gpfdist 实例 {#example-start-multiple-secure-gpfdist-instances}

```shell
# Starts the first secure gpfdist instance.
gpfdist -d /var/load_files1 -p 8081 --ssl /home/gpadmin/certs \
        --ssl_verify_peer on -l /home/gpadmin/log1 &

# Starts the second secure gpfdist instance.
gpfdist -d /var/load_files2 -p 8082 --ssl /home/gpadmin/certs \
        --ssl_verify_peer on -l /home/gpadmin/log2 &
```

## 步骤 3：使用 gpfdists 创建外部表 {#step-3-create-external-tables-with-gpfdists}

在 `LOCATION` 子句中使用 `gpfdists://` 协议创建安全的外部表：

### 可读外部表 {#readable-external-table}

```sql
CREATE EXTERNAL TABLE secure_sales_data (
    transaction_id int,
    product_name text,
    sale_date date,
    amount decimal(10,2)
)
LOCATION ('gpfdists://etl-server1:8081/sales/*.txt',
          'gpfdists://etl-server2:8082/sales/*.txt')
FORMAT 'TEXT' (DELIMITER '|' NULL ' ');
```

### 可写外部表 {#writable-external-table}

```sql
CREATE WRITABLE EXTERNAL TABLE secure_export (
    transaction_id int,
    product_name text,
    sale_date date,
    amount decimal(10,2)
)
LOCATION ('gpfdists://etl-server1:8081/exports/sales_data.txt')
FORMAT 'TEXT' (DELIMITER '|')
DISTRIBUTED BY (transaction_id);
```

### 启用错误处理 {#with-error-handling}

```sql
CREATE EXTERNAL TABLE secure_data_with_errors (
    id int,
    name text,
    value decimal(10,2)
)
LOCATION ('gpfdists://etl-server:8081/data/*.csv')
FORMAT 'CSV' (HEADER)
LOG ERRORS SEGMENT REJECT LIMIT 100;
```

## 配置参数 {#configuration-parameters}

### Apache Cloudberry 参数 {#apache-cloudberry-parameters}

在 `postgresql.conf` 中配置以下参数：

```ini
# Enables/disables SSL certificate verification (default: on)
verify_gpfdists_cert = on

# Control segment parallelism
gp_external_max_segs = 64
```

### gpfdist SSL 参数 {#gpfdist-ssl-parameters}

gpfdist 工具支持以下 SSL 相关选项：

| 参数 | 说明 | 默认值 |
|-----------|-------------|---------|
| `--ssl` | 启用 SSL 并指定证书路径 | 禁用 |
| `--ssl_verify_peer` | 验证客户端证书 | on |

## 安全最佳实践 {#security-best-practices}

### 证书管理 {#certificate-management}

- 通过受信任的证书颁发机构生成所有证书，以确保正确验证并建立信任链。
- 制定定期证书轮换计划，以增强安全性并避免证书过期引发的问题。
- 将私钥保存在安全的位置，并限制访问权限，确保只有获得授权的人员可以访问。
- 安全保存所有证书文件的备份，以便在系统故障或文件损坏时快速恢复。

### 网络安全 {#network-security}

- 配置防火墙规则，限制对 gpfdists 端口的访问，只允许获得授权的 Apache Cloudberry Segment 主机连接。
- 使用 VPN 或专用网络等安全网络连接，防止未经授权的访问者接入数据传输通道。
- 持续监控 SSL 连接和证书到期时间，以便主动处理安全问题。

### 访问控制 {#access-control}

- 遵循最小权限原则，仅授予用户和应用程序执行所需功能必需的最低权限。
- 实施可靠的认证机制，并在适当情况下使用多因素认证，以验证用户身份。
- 启用全面的审计日志记录，跟踪所有访问尝试、成功连接和安全相关事件，以满足合规要求并进行安全监控。

## 故障排查 {#troubleshooting}

### SSL 连接错误 {#ssl-connection-errors}

检查证书配置：

```shell
# Verifies certificate files exist.
ls -la $PGDATA/gpfdists/

# Checks certificate validity.
openssl x509 -in $PGDATA/gpfdists/client.crt -text -noout
```

### 排查证书验证问题 {#troubleshoot-certificate-verification-issues}

1. 验证 `root.crt` 文件包含正确的证书颁发机构链，并且已正确包含所有用于验证的中间证书。
2. 使用 `openssl x509 -dates` 等工具检查证书到期时间，确保证书尚未过期，并提前制定续期计划。
3. 使用证书验证工具，确认私钥文件 `client.key` 与 `client.crt` 中的公钥证书完全对应。

### 常见错误消息 {#common-error-messages}

| 错误 | 原因 | 解决方法 |
|-------|-------|----------|
| "SSL certificate verify failed" | 证书无效或已过期 | 检查证书有效性和 CA |
| "SSL handshake failed" | SSL 配置不匹配 | 核对双方的 SSL 设置 |
| "Permission denied" | 文件权限不正确 | 为证书文件设置正确的权限 |

### 调试 SSL 连接 {#debug-ssl-connections}

启用详细日志记录：

```shell
gpfdist -d /data -p 8081 --ssl /certs -V --ssl_verify_peer on
```

## 性能注意事项 {#performance-considerations}

- SSL 加密会在数据传输过程中引入计算开销，相较于未加密连接，可能降低整体吞吐量，尤其是在传输大量数据时。
- 证书缓存机制通过在多次数据传输操作之间复用已建立的安全连接，有助于减少 SSL 握手对性能的影响。
- 在不同主机或网络接口上部署多个 gpfdists 实例，以分散负载，提高并发数据操作的总吞吐量。
- 确保网络基础设施在 Apache Cloudberry Segment 与 gpfdist 服务器之间提供充足带宽和较低延迟，以尽量减少性能瓶颈。

## 从 gpfdist 迁移到 gpfdists {#migration-from-gpfdist-to-gpfdists}

将现有的 gpfdist 使用方式迁移到 gpfdists：

- 在所有 Apache Cloudberry Segment 主机上安装和配置所需的 SSL 证书，确保权限正确，并正确验证证书链。
- 更新所有外部表定义，将其 LOCATION 子句中的协议从 `gpfdist://` 改为 `gpfdists://`。
- 启用 `--ssl` 选项并重启 gpfdist 文件服务器，指定适当的证书目录和 SSL 验证设置。
- 全面测试所有 Apache Cloudberry Segment 发起的安全连接，验证数据加载操作能够通过新的加密协议正常运行。
- 更新所有相关自动化脚本、监控工具和操作流程，使其适应新的安全协议要求和证书管理任务。

### 迁移示例 {#example-migration}

迁移前（不安全）：

```sql
LOCATION ('gpfdist://etl-server:8081/data.txt')
```

迁移后（安全）：

```sql
LOCATION ('gpfdists://etl-server:8081/data.txt')
```

## 限制 {#limitations}

- 不能在同一个外部表定义中混用 `gpfdist://` 和 `gpfdists://` 协议。
- 所有 Apache Cloudberry Segment 主机都必须正确配置 SSL 证书和信任关系。
- SSL 加密会引入计算开销，相较于未加密的 gpfdist，可能降低数据传输吞吐量。
- 必须持续管理证书生命周期，包括续期、轮换和吊销。

## 进一步了解 {#learn-more}

- [使用 gpfdist 加载数据](/cloudberry/data-loading/files/load-data-using-gpfdist/)
- [SSL 证书管理](https://www.sslshopper.com/ssl-converter.html)
