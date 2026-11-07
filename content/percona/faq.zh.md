---
title: 常见问题
linkTitle: 常见问题
description: pg_tde 常见问题：加密范围、复制、密钥丢失、备份恢复、算法与运维要求。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/faq.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 900
upstream_source: percona
---

> [!NOTE] 本站勘误
> 临时文件加密范围和内部密钥轮换说明已依据当前限制与架构文档澄清。下文合规相关表述保留上游文档的语境，不构成对具体部署的认证。 详见[勘误记录](/zh/percona/site/errata/)。


## 为什么需要 TDE？ {#why-do-i-need-tde}

使用 TDE 有以下益处：

- 帮助满足《通用数据保护条例》（GDPR）、支付卡行业数据安全标准（PCI DSS）、《加利福尼亚消费者隐私法案》（CCPA）、《2018 年数据保护法》（DPA 2018）等安全和法律监管要求。
- 加密备份。即使有人获得备份的物理访问权限，加密也能确保数据仍然无法读取且受到保护。
- 对特定数据集进行精细加密，减少加密带来的性能开销。
- 在现有安全措施之上增加一层保护。

## 何时以及如何使用 TDE？ {#when-and-how-should-i-use-tde}

处理个人身份信息（PII）时，数据加密至关重要，尤其是在监管严格的领域：

* 金融服务：TDE 可帮助满足 PCI DSS。
* 医疗和保险：满足 HIPAA、HITECH、CCPA 等要求。
* 电信、政府和教育：确保数据机密性。

使用 TDE 有助于规避以下风险：

* 数据泄露。
* 身份盗用及其可能引发的金融欺诈等犯罪。
* 声誉受损，导致客户信任和业务流失。
* 不遵守数据保护规定带来的法律后果和经济损失。
* 滥用未加密敏感数据造成的内部威胁。

pg_tde 的加密范围包括使用 `tde_heap` 的表，以及启用 WAL 加密后的 WAL。临时表可以使用 `tde_heap`，但超出 `work_mem` 后写出的临时文件**不会加密**。详见[当前限制](/zh/percona/index/tde-limitations/)。

`pg_tde` 尚不加密系统目录，因此统计数据和数据库元数据不加密。

## 逻辑复制能与 pg_tde 一起使用吗？ {#will-logical-replication-work-with-pgtde}

可以，逻辑复制支持加密表。

## 逻辑复制会让订阅端的数据保持加密吗？ {#does-logical-replication-keep-data-encrypted-on-subscribers}

逻辑复制**不会**保留加密状态。如果发布端使用 `pg_tde` 而订阅端没有使用，复制的数据在订阅端将以**明文**存储。

由于逻辑复制的工作方式，加密不会在数据块层面传播。

> [!NOTE]
> 发布端加密**不能保证**逻辑副本也加密。

## 已使用磁盘级加密，为什么还需要 TDE？ {#i-use-disk-level-encryption-why-should-i-care-about-tde}

硬盘加密会加密全部数据，包括系统、应用程序和临时文件。

全盘加密可以防止取得设备物理访问权限的人读取数据，即使设备遗失或失窃也能提供保护。但系统启动后它不再提供这种保护：系统运行或授权用户请求数据时，数据会自动解密。

另一个考虑因素是个人账户号码（PAN）加密的 PCI DSS 合规要求。

* **PCI DSS 3.4.1** 在满足以下要求时，可能认为磁盘加密足以满足要求：

    * 将逻辑数据访问与操作系统认证分离。
    * 确保解密密钥不与用户账户关联。

    注意，上游原文指出 PCI DSS 3.4.1 于 2025 年 3 月 31 日退役，因此建议转向 PCI DSS 4.0。

* **PCI DSS 4.0** 认为，仅采用磁盘和分区级加密不足以保护 PAN，需要额外的安全层，`pg_tde` 可以提供这层保护。

`pg_tde` 专门处理数据文件，提供更精细的加密控制。数据在运行期间仍以加密形式保存在磁盘上；移动到其他目录、系统或存储时，也保持加密。例如，备份移动到备份存储后仍然加密。

因此，可以使用 TDE 在表级加密敏感数据，再通过磁盘级加密保护存放这些数据的卷或整个磁盘。

## 仅使用 TDE 足以确保数据安全吗？ {#is-tde-enough-to-ensure-data-security}

**不够。** 透明数据加密（TDE）为静态数据增加一层保护。还应考虑以下安全措施：

* 访问控制和认证。
* TLS 等强网络安全措施。
* 磁盘加密。
* 定期监控与审计。
* 对敏感字段采取额外保护，例如应用层加密。

## pg_tde 如何保护数据？ {#how-does-pgtde-make-my-data-safe}

`pg_tde` 使用两类密钥加密数据：

* 内部加密密钥用于加密数据，以加密形式统一保存在内部的 `$PGDATA/pg_tde` 目录中。
* 主密钥用于加密内部加密密钥，保存在外部密钥管理系统（KMS）中。

可以使用以下 KMS：

* [HashiCorp Vault](https://developer.hashicorp.com/vault/docs/what-is-vault)。`pg_tde` 支持 Vault 的 KV secrets engine v2，详见 [Vault 配置](/zh/percona/global-key-provider-configuration/vault/)。
* [OpenBao](https://openbao.org/)，Vault 的一种实现。
* 兼容 KMIP 的服务器。KMIP 是处理密码学工作负载和秘密管理的标准化协议，详见 [KMIP 配置](/zh/percona/global-key-provider-configuration/kmip-server/)。

> [!NOTE]
> HashiCorp Vault 也可以作为 KMIP 服务器，为使用 KMIP 协议的客户端管理密码学密钥。
> *（KMIP 功能仅在 Vault 企业版中提供。）*

加密过程分为两部分：

### 数据文件加密 {#encryption-of-data-files}

首先，数据文件由内部密钥加密。每个具有不同[对象标识符（OID）](https://www.postgresql.org/docs/current/datatype-oid.html) 的文件都有一个内部密钥。例如，一个带 4 个索引的表有 5 个内部密钥：表一个，每个索引各一个。

最初根据 PostgreSQL 的表访问方法决定加密哪些文件。在 `CREATE` 或 `ALTER TABLE` 中使用 `USING tde_heap` 子句时，新建的数据文件被标记为加密，后续文件操作负责加解密。如果原文件因 `TRUNCATE` 或 `VACUUM FULL` 重新创建，新文件会继承加密信息，决定是否加密。

主密钥用于加密内部密钥，并保存在密钥管理存储中。查询表时，系统从密钥存储获取主密钥进行解密，再使用该表的内部密钥解密数据。

### WAL 加密 {#wal-encryption}

WAL 加密作用于整个数据库集群。集群中所有数据库的修改都写入同一份 WAL，以维持数据一致性和完整性，并确保集群能够恢复到一致状态。因此，WAL 采用全局加密。

启用 WAL 加密并启动服务器后，`pg_tde` 从第一次 WAL 写入开始对 WAL 文件进行加密。

WAL 与表数据采用相同的双层密钥方式：先用内部密钥加密 WAL 页面，再用全局主密钥加密内部密钥。

WAL 加密可以启用或关闭，因此 WAL 可能同时包含加密和未加密数据。WAL 加密 GUC 参数只影响写入。

恢复过程或工具读取 WAL 时，完全依据 WAL 加密密钥的元数据判断哪些内容需要解密。

## 是否应该加密所有数据？ {#should-i-encrypt-all-my-data}

这取决于业务要求和数据敏感程度。加密所有数据是良好实践，但可能影响性能。

可以考虑只加密保存敏感数据的表，自行决定加密哪些表、使用哪个密钥。[配置多租户](/zh/percona/how-to/multi-tenant-setup/)介绍了这种方式。

上游建议，只有当全部数据都敏感（例如 PII），或没有其他办法满足数据安全要求时，才加密整个数据库。

## pg_tde 使用哪些密码算法？ {#what-cipher-mechanisms-are-used-by-pgtde}

`pg_tde` 当前使用：

* `AES-128-CBC`、`AES-256-CBC`：使用内部密钥加密数据库文件。
* `AES-128-CTR`、`AES-256-CTR`：使用内部密钥加密 WAL。
* `AES-128-GCM`、`AES-256-GCM`：使用主密钥加密内部密钥。

## 是否支持后量子加密？ {#is-post-quantum-encryption-supported}

尚不支持。上游原文说明，其实现依赖的 OpenSSL 库尚不支持后量子加密。

## 能否加密已有表？ {#can-i-encrypt-an-existing-table}

可以。执行以下 `ALTER TABLE` 命令：

```sql
ALTER TABLE table_name SET ACCESS METHOD tde_heap;
```

`SET ACCESS METHOD` 会丢弃提示位，可能影响性能，建议执行 `SELECT count(*)`，检查每个元组的可见性并设置提示位。详见[更改已有表](/zh/percona/test/)。

## 加密数据需要重启数据库吗？ {#do-i-have-to-restart-the-database-to-encrypt-the-data}

以下情况必须重启数据库以应用变更：

* 启用 `pg_tde` 扩展后。
* 启用 WAL 加密时。

此后，无需再重启数据库。使用 `tde_heap` 访问方法创建或修改表时，相关文件会被标记为需要加密。加密发生在存储管理器层，在事务写入磁盘之前完成。详见 [tde_heap 的工作原理](/zh/percona/index/table-access-method/#how-tdeheap-works-with-pgtde)。

## 丢失主密钥后，数据会怎样？ {#what-happens-to-my-data-if-i-lose-a-principal-key}

如果丢失加密密钥，尤其是主密钥，数据就会丢失。因此，安全备份加密密钥并使用密钥管理服务至关重要。

## pg_tde 可以用于多租户吗？ {#can-i-use-pgtde-in-a-multi-tenant-setup}

多租户是一种多个用户或租户共享同一资源的架构。共享资源可以是数据库、模式或整个集群。

`pg_tde` 通过为每个数据库使用独立主密钥来支持多租户。数据库所有者可以决定加密其中哪些表，同一数据库中可以同时存在加密表和未加密表。

可以使用基于角色的访问控制（RBAC）控制用户对数据库的访问。

## 备份安全吗？可以从中恢复吗？ {#are-my-backups-safe-can-i-restore-from-them}

`pg_tde` 加密静态数据，即数据以加密形式保存在磁盘上。备份时，已经加密的数据文件从磁盘复制到存储中，因此备份中的数据仍受到保护。

由于加密发生在数据库层，工具和应用程序仍以相同方式处理数据。

恢复加密备份时，必须拥有当初用于加密备份文件的同一主密钥。

## 使用 FIPS 模式的 OpenSSL 时，pg_tde 是否符合要求？可以使用自己的 FIPS 模式 OpenSSL 库吗？ {#i-m-using-openssl-in-fips-mode-and-need-to-use-pgtde-does-pgtde-comply-with-fips-requirements-can-i-use-my-own-fips-mode-openssl-library-with-pgtde}

可以。`pg_tde` 支持符合 FIPS 要求的 OpenSSL，无论该库由操作系统提供还是自行提供。使用自己的库时，应确保它们经过 FIPS 认证。

## 如何轮换 pg_tde 的内部加密密钥？ {#how-do-i-rotate-internal-encryption-keys-in-pgtde}

没有专用的内部密钥轮换函数，因为每当表的数据文件被完整重写时，实际上就完成了一次密钥轮换。`VACUUM FULL`、`TRUNCATE` 和部分（并非所有）`ALTER TABLE` 命令会自动生成新的内部密钥。

`VACUUM FULL` 会重写表并生成新的内部密钥；普通 `VACUUM` 不会完整重写表。执行前应规划所需的排他锁和磁盘空间。

## 哪些工具支持 pg_tde WAL 加密？ {#what-tools-are-supported-with-pgtde-wal-encryption}

支持工具的完整列表见 [pg_tde 的限制](/zh/percona/index/tde-limitations/)。
