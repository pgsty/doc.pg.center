---
title: pg_tde_archive_decrypt
linkTitle: 归档 WAL
description: 在 WAL 归档前解密日志，并通过包装归档命令交给 cp 或 pgBackRest。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/command-line-tools/pg-tde-archive-decrypt.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 720
upstream_source: percona
---

`pg_tde_archive_decrypt` 包装归档命令，在归档之前解密 WAL 文件，使外部工具能够访问未加密的 WAL。之所以需要这样做，是因为双层密钥结构中的 WAL 加密密钥与主机相关，在重放主机上可能不可用。

> [!TIP]
> 加密架构和密钥层次详见[架构](/zh/percona/architecture/overview/)。

该工具通常与 [pg_tde_restore_encrypt](/zh/percona/command-line-tools/pg-tde-restore-encrypt/) 配合，用于 WAL 归档。

## 工作原理 {#how-it-works}

1. 将 WAL 段解密到 RAM 磁盘（`/dev/shm`）中的临时文件。
2. 将归档命令中的 `%p` 和 `%f` 替换为解密文件的路径和名称。
3. 执行归档命令。

> [!NOTE]
>
> 为确保安全，应使用 `PgBackRest` 等工具对 WAL 归档中的文件进行加密。

## 用法 {#usage}

```bash
pg_tde_archive_decrypt [OPTION]
pg_tde_archive_decrypt DEST-NAME SOURCE-PATH ARCHIVE-COMMAND
```

## 参数说明 {#parameter-descriptions}

* `DEST-NAME`：要发送到归档的 WAL 文件名。
* `SOURCE-PATH`：原始加密 WAL 文件的路径。
* `ARCHIVE-COMMAND`：需要包装的归档命令。`%p` 和 `%f` 分别替换为解密后的 WAL 文件路径和 WAL 文件名。

## 选项 {#options}

* `-V, --version`：显示版本信息后退出。
* `-?, --help`：显示帮助信息后退出。

> [!NOTE]
>
> 在 `postgresql.conf` 的 `archive_command` 中使用时，`ARCHIVE-COMMAND` 内的 `%f` 或 `%p` 必须分别转义为 `%%f` 或 `%%p`。

## 示例 {#examples}

### 使用 cp {#using-cp}

```ini
archive_command='pg_tde_archive_decrypt %f %p "cp %%p /mnt/server/archivedir/%%f"'
```

### 使用 PgBackRest {#using-pgbackrest}

```ini
archive_command='pg_tde_archive_decrypt %f %p "pgbackrest --stanza=your_stanza archive-push %%p"'
```

> [!WARNING] 必需配置
>
> 启用 WAL 加密的部署必须在 `archive_command` 中使用 `pg_tde_archive_decrypt`，并在 `restore_command` 中使用 [`pg_tde_restore_encrypt`](/zh/percona/command-line-tools/pg-tde-restore-encrypt/)，否则不受支持。
>
> 在适用的 pgBackRest 配置节中关闭以下功能：
>
> ```ini
> archive-async=n
> archive-header-check=n
> checksum-page=n
> ```
