---
title: "pg_authid"
description: "`pg_catalog` 模式中的 `pg_authid` 表包含数据库授权标识符（角色）的信息。"
weight: 170
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-authid.md"
---

角色涵盖用户和组的概念。用户是设置了 `rolcanlogin` 标志的角色。任何角色（无论是否设置 `rolcanlogin`）都可以包含其他角色作为成员。参见 [`pg_auth_members`](/cloudberry/reference/sys-catalogs/sys-tables/pg-auth-members/)。

由于此目录包含密码，不能允许公开读取。`pg_roles` 是基于 `pg_authid` 的公开可读视图，其中密码字段已清空。

由于用户身份的作用域是整个系统，`pg_authid` 由 Apache Cloudberry 系统中的所有数据库共享：每个系统只有一份 `pg_authid`，并非每个数据库各有一份。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |行标识符。|
|`rolname`|name| |角色名。|
|`rolsuper`|boolean| |角色具有超级用户权限。|
|`rolinherit`|boolean| |角色自动继承其所属角色的权限。|
|`rolcreaterole`|boolean| |角色可以创建其他角色。|
|`rolcreatedb`|boolean| |角色可以创建数据库。|
|`rolcanlogin`|boolean| |角色可以登录，即可以将此角色用作会话初始授权标识符。|
|`rolreplication`|boolean| |角色是复制角色，即可以发起流复制，并使用 `pg_start_backup` 和 `pg_stop_backup` 启用或停用系统备份模式。|
|`rolbypassrls`|boolean| |角色绕过所有行级安全策略。|
|`rolconnlimit`|int4| |对于可以登录的角色，此值设置该角色允许的最大并发连接数。`-1` 表示不限制。|
| `rolenableprofile` | `boolean` |  |角色具有配置档案。|
|`rolpassword`|text| |密码（可能已加密）；没有则为 NULL。如果密码已加密，此列以字符串 `md5` 开头，后接一个 32 字符的十六进制 MD5 哈希。计算 MD5 哈希时，将用户密码与用户名拼接。例如，用户 `joe` 的密码为 `xyzzy` 时，Apache Cloudberry 存储 `xyzzyjoe` 的 md5 哈希。Apache Cloudberry 将不符合此格式的密码视为未加密密码。|
|`rolvaliduntil`|timestamptz| |密码过期时间（仅用于密码认证）；永不过期则为 NULL。|
| `rolprofile` | `oid` |  |关联配置档案在 `pg_profile` 中的对象 ID。|
| `rolaccountstatus` | smallint |  |角色的账户状态。|
| `rolfailedlogins` | integer | |登录失败的尝试次数。|
| `rolpasswordsetat` | timestamptz | |最后一次设置密码的时间。|
| `rollockdate`  | timestamptz | |角色被锁定的时间。|
| `rolpasswordexpire` | timestamptz | |密码将过期的时间。|
|`rolresqueue`|oid| |关联资源队列在 `pg_resqueue` 中的对象 ID。|
|`rolcreaterextgpfd`|boolean| |使用 `gpfdist` 或 `gpfdists` 协议创建可读外部表的权限。|
|`rolcreaterexhttp`|boolean| |使用 `http` 协议创建可读外部表的权限。|
|`rolcreatewextgpfd`|boolean| |使用 `gpfdist` 或 `gpfdists` 协议创建可写外部表的权限。|
|`rolresgroup`|oid| |关联资源组在 `pg_resgroup` 中的对象 ID。|
