---
title: 启用 WAL 加密时备份
linkTitle: 启用 WAL 加密时备份
description: 启用 WAL 加密时使用 pg_tde_basebackup 备份和恢复，以及各备份模式的兼容性。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/how-to/backup-wal-enabled.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 550
upstream_source: percona
---

> [!DANGER]
> 备份运行期间不要轮换加密密钥，否则可能造成备份不一致并导致恢复失败。这适用于所有备份工具。
>
> 详见 [pg_tde 的限制](/zh/percona/index/tde-limitations/#limitations-when-using-pgtde)。

启用 WAL 加密时，按以下步骤创建备份：

1. 将源服务器数据目录中的 `pg_tde` 目录（例如 `/var/lib/postgresql/data/pg_tde/`），包括 `wal_keys` 和 `1664_providers` 文件，复制到 `pg_tde_basebackup` 将要写入备份的目标目录。

    同时，将提供商配置引用的外部文件（例如证书或密钥文件）复制到备份目标下相同的相对路径，以便 `pg_tde_basebackup -E` 定位并验证它们。

2. 运行：

    ```bash
    pg_tde_basebackup -D /path/to/backup -E [aes_128|aes_256]
    ```

    其中：

    - `-D /path/to/backup` 指定备份位置，你需要将 `pg_tde` 复制到此处。
    - `-E`（或 `--encrypt-wal`）启用 WAL 加密，并验证复制的 `pg_tde` 和提供商文件存在且服务器密钥可访问（必需）。`-E` 接受密码算法参数，目前支持 `aes_128` 和 `aes_256`。未指定 `-E` 时，`pg_tde_basebackup` 会尝试从服务器密钥判断算法；无法判断时，默认使用 `aes_128`。

> [!NOTE]
> - `-E` 仅适用于 `-X stream`（默认），不兼容 `-X none` 或 `-X fetch`。详见[备份方法与 WAL 加密的兼容性](#backup-method-compatibility-with-wal-encryption)。
> - `-E` 仅支持 plain 输出格式（`-F p`），不能用于 tar 输出格式（`-F t`）。

## 备份期间的密钥轮换 {#key-rotation-during-backups}

> [!DANGER]
> 备份进行期间不要轮换加密密钥。这适用于所有备份工具。
>
> 密钥轮换期间创建的备份可能在 WAL 重放时无法启动，还可能造成加密数据（表、索引和其他关系）损坏。
>
> 例如，可能出现以下错误：
>
> ```sql
> FATAL: failed to retrieve principal key "database_keyXXXX" from key provider "providerYYYY"
> CONTEXT: WAL redo at ... ROTATE_PRINCIPAL_KEY ...
> ```
>
> 为确保备库可恢复，请将密钥轮换安排在备份窗口之外，或在轮换完成后重新执行完整备份。

## 恢复启用 WAL 加密时创建的备份 {#restore-a-backup-created-with-wal-encryption}

恢复通过 `pg_tde_basebackup -E` 创建的备份时：

1. 确保提供商配置引用的所有外部文件（如证书或密钥文件）也位于相同的相对路径，且可以访问。
2. 使用恢复的数据目录启动 PostgreSQL。

## 备份方法与 WAL 加密的兼容性 {#backup-method-compatibility-with-wal-encryption}

Tar 格式（`-F t`）：

* 支持 `-X fetch`。
* 启用 WAL 加密时不支持 `-X stream`。使用 `pg_tde_basebackup -F t -X stream` 会创建无法正常工作的副本。

流模式（`-X stream`）：

* **必须**指定 `-E`（`--encrypt-wal`）。
* 未指定 `-E` 时，备份可能包含解密后的 WAL，而 `postgresql.conf` 仍保留 `wal_encryption=on`，并复制了 `pg_tde/wal_keys`。这会导致**启动失败，并使备份数据面临风险**。

Fetch 模式（`-X fetch`）：

* 兼容加密 WAL，无需额外选项。

None（`-X none`）：

* 备份不包含 WAL，不受 WAL 加密影响。

> [!NOTE]
> 如果源服务器存在 `pg_tde/wal_keys`，使用 `-X none` 或 `-X fetch` 运行 `pg_tde_basebackup` 会产生类似警告：
>
> ```sql
> pg_tde_basebackup: warning: the source has WAL keys, but no WAL encryption configured for the target backups
> pg_tde_basebackup: detail: This may lead to exposed data and broken backup
> pg_tde_basebackup: hint: Run pg_tde_basebackup with -E to encrypt streamed WAL
> ```
>
> 使用 `-X none` 或 `-X fetch` 时没有 WAL 流传输，可以安全忽略这些警告。
