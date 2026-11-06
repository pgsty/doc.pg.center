---
title: "安全最佳实践"
description: "介绍应遵循的基本安全最佳实践，以确保系统达到最高安全级别。"
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/security/security-best-practices.md"
---

Apache Cloudberry 的默认安全配置如下：

- 只允许本地连接。
- 为超级用户（`gpadmin`）配置基本认证。
- 超级用户有权执行任何操作。
- 只有数据库角色密码经过加密。

## 系统用户（gpadmin） {#system-user-gpadmin}

保护并限制对 `gpadmin` 系统用户的访问。

Cloudberry 需要一个 UNIX 用户 ID 来安装和初始化 Apache Cloudberry 系统。Cloudberry 文档将此系统用户称为 `gpadmin`。`gpadmin` 用户既是 Apache Cloudberry 中默认的数据库超级用户，也是 Cloudberry 安装文件及其底层数据文件的文件系统所有者。默认管理员账户是 Apache Cloudberry 设计的基础。没有它，系统就无法运行，而且无法限制 `gpadmin` 用户 ID 的访问权限。

`gpadmin` 用户可以绕过 Apache Cloudberry 的所有安全功能。任何使用此用户 ID 登录 Cloudberry 主机的人，都能读取、修改或删除任何数据，包括系统目录数据和数据库访问权限。因此，保护 `gpadmin` 用户 ID 非常重要，只有必需的系统管理员才应获得其访问权。

管理员只有在执行某些系统维护任务（如升级或扩容）时，才应以 `gpadmin` 身份登录 Cloudberry。

数据库用户绝不应以 `gpadmin` 身份登录，ETL 或生产工作负载也绝不应以 `gpadmin` 身份运行。

## 超级用户 {#superusers}

被授予 `SUPERUSER` 属性的角色就是超级用户。超级用户会绕过所有访问权限检查和资源队列。只有系统管理员才应获得超级用户权限。

## 登录用户 {#login-users}

为每个登录用户分配独立的角色，并设置 `LOGIN` 属性。

为满足日志记录和审计的需要，每个获准登录 Apache Cloudberry 的用户都应拥有自己的数据库角色。对于应用程序或 Web 服务，可考虑为每个应用程序或服务创建独立的角色。请参阅《Apache Cloudberry 管理员指南》中的“创建新角色（用户）”。

每个登录角色都应分配到一个独立的非默认资源队列。

## 组 {#groups}

使用组管理访问权限。

为每一类逻辑上的对象权限或访问权限组合创建一个组。

每个登录用户都应属于一个或多个角色。使用 `GRANT` 语句向角色添加组访问权限。使用 `REVOKE` 语句从角色移除组访问权限。

组角色不应设置 `LOGIN` 属性。

请参阅《Apache Cloudberry 管理员指南》中的“创建组（角色成员关系）”。

## 对象权限 {#object-privileges}

新对象只有所有者和超级用户拥有完整权限。必须授予权限，其他角色（用户或组）才能访问对象。不同类型的数据库对象可以授予不同的权限。使用 `GRANT` 语句向角色添加权限，使用 `REVOKE` 语句移除权限。

可以使用 `REASSIGN OWNED BY` 语句更改对象所有者。例如，准备删除某个角色时，应更改该角色所拥有对象的所有者。使用 `DROP OWNED BY` 可以删除角色拥有的对象，包括依赖对象。

可以使用模式加强一层对象权限检查，但模式权限不会覆盖为模式内对象设置的对象权限。

## 操作系统用户和文件系统 {#operating-system-users-and-file-system}

> [!NOTE] 注意
> 本节所示命令应以 root 用户身份运行。

为防止网络遭到入侵，系统管理员应确认组织内使用的密码足够强。以下建议可以增强密码强度：

- 建议的最小密码长度：至少 9 个字符。MD5 密码应为 15 个字符或更长。
- 混合使用大写和小写字母。
- 混合使用字母和数字。
- 包含非字母数字字符。
- 选择一个自己能记住的密码。

整个系统的安全性取决于 root 密码的强度。该密码至少应有 12 个字符，并混合使用大写字母、小写字母、特殊字符和数字。不应使用任何字典中的单词作为密码基础。

应配置密码过期参数。以下命令必须以 `root` 身份运行或使用 `sudo`。

确保 `/etc/libuser.conf` 文件的 `[import]` 部分包含以下行。

```
login_defs = /etc/login.defs
```

确保 `[userdefaults]` 部分中没有任何行以以下文本开头，因为这些词会覆盖 `/etc/login.defs` 中的设置：

- `LU_SHADOWMAX`
- `LU_SHADOWMIN`
- `LU_SHADOWWARNING`

确保以下命令没有输出。运行此命令列出的任何账户都应锁定。

```shell
grep "^+:" /etc/passwd /etc/shadow /etc/group
```

注意：我们强烈建议客户在初始设置后修改密码。

```shell
cd /etc
chown root:root passwd shadow group gshadow
chmod 644 passwd group
chmod 400 shadow gshadow
```

查找所有对所有用户可写且未设置 sticky 位的文件。

```shell
find / -xdev -type d ( -perm -0002 -a ! -perm -1000 ) -print
```

为运行上一条命令得到的所有目录设置 sticky 位（`# chmod +t {dir}`）。

查找所有对所有用户可写的文件，并修复列出的每个文件。

```shell
find / -xdev -type f -perm -0002 -print
```

为运行上述命令生成的所有文件设置正确的权限（`# chmod o-w {file}`）。

查找所有不属于有效用户或组的文件，并根据情况为其指定所有者或删除文件。

```shell
find / -xdev ( -nouser -o -nogroup ) -print
```

查找所有对所有用户可写的目录，并确保其所有者是 root 或系统账户之一（假定只有系统账户的用户 ID 小于 500）。如果命令产生任何输出，请确认所有者设置正确，或将其重新指定为 root。

```shell
find / -xdev -type d -perm -0002 -uid +500 -print
```

可以使用可插拔认证模块（PAM）框架配置认证设置，例如密码质量、密码过期策略、密码复用、密码重试次数等。PAM 会在 `/etc/pam.d` 目录中查找特定于应用程序的配置信息。运行 `authconfig` 或 `system-config-authentication` 会重写 PAM 配置文件，销毁手动所做的更改，并以系统默认值替换。

默认的 `pam_cracklib` PAM 模块会检查密码强度。要按美国国防部指南的建议，将 `pam_cracklib` 配置为至少要求一个大写字符、小写字符、数字和特殊字符，请编辑 `/etc/pam.d/system-auth` 文件，在对应于 password requisite `pam_cracklib.so try_first_pass` 的行中加入以下参数。

```shell
retry=3:
dcredit=-1. Require at least one digit
ucredit=-1. Require at least one upper case character
ocredit=-1. Require at least one special character
lcredit=-1. Require at least one lower case character
minlen-14. Require a minimum password length of 14.
```

例如：

```shell
password required pam_cracklib.so try_first_pass retry=3minlen=14 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1
```

可以根据安全策略要求设置这些参数。请注意，密码限制不适用于 root 密码。

`pam_tally2` PAM 模块能够在登录失败次数达到指定数量后锁定用户账户。要强制执行密码锁定，请编辑 `/etc/pam.d/system-auth` 文件，加入以下行：

- 第一条 auth 行应包含：

    ```shell
    auth required pam_tally2.so deny=5 onerr=fail unlock_time=900
    ```

- 第一条 account 行应包含：

    ```shell
    account required pam_tally2.so
    ```

此处，deny 参数设为将重试次数限制为 5，`unlock_time` 设为 900 秒，使账户在解锁前保持锁定 900 秒。可以根据安全策略要求适当配置这些参数。可以使用 `pam_tally2` 工具手动解锁锁定的账户：

```shell
/sbin/pam_tally2 --user {username} --reset
```

可以使用 PAM 限制近期密码的复用。`pam_ unix` 模块的 remember 选项可以设置为记住近期密码并防止复用。为此，请编辑 `/etc/pam.d/system-auth` 中相应的行，加入 remember 选项。

例如：

```shell
password sufficient pam_unix.so [ … existing_options …] 
remember=5
```

可以根据安全策略要求设置要记住的历史密码数量。

```shell
cd /etc
chown root:root passwd shadow group gshadow
chmod 644 passwd group
chmod 400 shadow gshadow
```
