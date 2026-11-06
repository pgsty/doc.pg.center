---
title: "在 Apache Cloudberry 中保护密码"
linkTitle: "保护密码"
description: "在默认配置下，Apache Cloudberry 将登录用户密码的 MD5 或 SCRAM-SHA-256 哈希值保存在 `pg_authid` 系统目录中，而不保存明文密码。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/security/protect-passwords.md"
---

任何能够查看 `pg_authid` 表的人都能看到哈希字符串，但看不到密码。这也确保了将数据库转储为备份文件时，密码仍然不会以明文呈现。

使用以下任一命令设置密码时，都会执行哈希函数：

- `CREATE USER name WITH PASSWORD 'password'`
- `CREATE ROLE name WITH LOGIN PASSWORD 'password'`
- `ALTER USER name WITH PASSWORD 'password'`
- `ALTER ROLE name WITH PASSWORD 'password'`

> [!NOTE] 注意
> SQL 命令语法和 `password_encryption` 配置变量中虽然使用了 *encrypt*（加密）一词，但严格来说，密码并没有经过加密。它们经过的是*哈希运算*，因此无法解密。

哈希值根据拼接后的明文密码和角色名计算得出。MD5 哈希会生成以 `md5` 开头的 32 字节十六进制字符串，而 SCRAM-SHA-256 哈希会生成以 `SCRAM-SHA-256` 开头的 64 字节十六进制字符串。密码的哈希值保存在 `pg_authid` 系统表的 `rolpassword` 列中。

要全局设置 `password_encryption`，请编辑 `postgresql.conf` 文件，将 `password_encryption` 参数设为 `md5` 或 `scram-sha-256`。

要在会话中设置 `password_encryption`，请使用 SQL `SET` 命令：

```sql
SET password_encryption = 'md5';
```
