---
title: pg_tde_restore_encrypt
linkTitle: 恢复 WAL
description: 从 WAL 归档恢复日志，并以 pg_tde 兼容的加密格式写入数据目录。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/command-line-tools/pg-tde-restore-encrypt.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 730
upstream_source: percona
---

> [!NOTE] 本站勘误
> 恢复命令占位符的说明已按工具内置帮助修正。 详见[勘误记录](/zh/percona/site/errata/)。


`pg_tde_restore_encrypt` 包装普通的 WAL 归档恢复命令，将恢复的数据以兼容 `pg_tde` 的格式写入磁盘。

> [!NOTE]
>
> 此命令通常与 [pg_tde_archive_decrypt](/zh/percona/command-line-tools/pg-tde-archive-decrypt/) 配合使用。

## 工作原理 {#how-it-works}

1. 将恢复命令中的 `%f` 和 `%p` 替换为 WAL 文件名和临时文件路径（位于 `/dev/shm`）。
2. 执行恢复命令，从归档获取未加密 WAL，写入临时文件。
3. 加密临时文件，将其写入 PostgreSQL 数据目录中的目标路径。

## 用法 {#usage}

```bash
pg_tde_restore_encrypt [OPTION]
pg_tde_restore_encrypt SOURCE-NAME DEST-PATH RESTORE-COMMAND
```

## 参数说明 {#parameter-descriptions}

* `SOURCE-NAME`：要从归档获取的 WAL 文件名。
* `DEST-PATH`：加密 WAL 文件的写入路径。
* `RESTORE-COMMAND`：需要包装的恢复命令；`%f` 和 `%p` 分别替换为 WAL 文件名和写入未加密 WAL 的路径。

## 选项 {#options}

* `-V, --version`：显示版本信息后退出。
* `-?, --help`：显示帮助信息后退出。

> [!NOTE]
>
> 在 `postgresql.conf` 的 `restore_command` 中使用时，`RESTORE-COMMAND` 内的 `%f` 或 `%p` 必须分别转义为 `%%f` 或 `%%p`。

## 示例 {#examples}

### 使用 cp {#using-cp}

```ini
restore_command='pg_tde_restore_encrypt %f %p "cp /mnt/server/archivedir/%%f %%p"'
```

### 使用 PgBackRest {#using-pgbackrest}

```ini
restore_command='pg_tde_restore_encrypt %f %p "pgbackrest --stanza=your_stanza archive-get %%f \"%%p\""'
```

> [!WARNING] 必需配置
>
> 启用 WAL 加密的部署必须在 `archive_command` 中使用 [`pg_tde_archive_decrypt`](/zh/percona/command-line-tools/pg-tde-archive-decrypt/)，并在 `restore_command` 中使用 `pg_tde_restore_encrypt`，否则不受支持。
>
> 在适用的 pgBackRest 配置节中关闭以下功能：
>
> ```ini
> archive-async=n
> archive-header-check=n
> checksum-page=n
> ```
