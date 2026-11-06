---
title: "安全最佳实践"
linkTitle: "安全"
description: "确保系统达到最高安全级别的最佳实践。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/best-practices/security-best-practices.md"
---

## 基本安全最佳实践 {#basic-security-best-practices}

- 保护 `gpadmin` 系统用户。Cloudberry 要求使用 UNIX 用户 ID 安装和初始化 Apache Cloudberry 系统。Cloudberry 文档将此系统用户称为 `gpadmin`。在 Apache Cloudberry 中，`gpadmin` 用户既是默认数据库超级用户，也是 Cloudberry 安装及其底层数据文件的文件系统所有者。默认管理员帐户是 Apache Cloudberry 设计的基础。系统无法在没有它的情况下运行，也无法限制 `gpadmin` 用户 ID 的访问。这个 `gpadmin` 用户可以绕过 Apache Cloudberry 的所有安全功能。任何以该用户 ID 登录 Cloudberry 主机的人，都可以读取、更改或删除包括系统目录数据和数据库访问权限在内的任何数据。因此，保护 `gpadmin` 用户 ID、只允许必要的系统管理员访问它非常重要。管理员只能在执行升级或扩容等特定系统维护任务时，以 `gpadmin` 身份登录 Cloudberry。数据库用户绝不能以 `gpadmin` 身份登录，ETL 或生产工作负载也绝不能以 `gpadmin` 身份运行。
- 为每个登录用户分配独立角色。出于日志记录和审计目的，应为每个获准登录 Apache Cloudberry 的用户分配独立的数据库角色。对于应用或 Web 服务，可以考虑为每个应用或服务创建独立角色。
- 使用组管理访问权限。
- 限制具有 `SUPERUSER` 角色属性的用户。超级用户角色会绕过 Apache Cloudberry 中的所有访问权限检查和资源排队；只有系统管理员才应获得超级用户权限。

## 密码强度指南 {#password-strength-guidelines}

为保护网络免受入侵，系统管理员应验证组织内使用的密码足够强。以下建议可以增强密码强度：

- 建议的最小密码长度：至少 9 个字符。MD5 密码应为 15 个字符或更长。
- 混合使用大小写字母。
- 混合使用字母和数字。
- 包含非字母数字字符。
- 选择一个自己能够记住的密码。

以下是可以用来确定密码强度的密码破解软件建议：

- John The Ripper。这是一个快速、灵活的密码破解程序，支持使用多个词表，也能够执行暴力破解。可从网上的 [http://www.openwall.com/john/](http://www.commoncriteriaportal.org/products/?expand#ALL) 获取。
- Crack。Crack 可能是最知名的密码破解软件。它同样非常快速，但不如 John The Ripper 易于使用。可从网上的 [http://www.crypticide.com/alecm/security/crack/c50-faq.html](http://www.commoncriteriaportal.org/products/?expand#ALL) 获取。

整个系统的安全性取决于 root 密码的强度。该密码应至少包含 12 个字符，并混合使用大写字母、小写字母、特殊字符和数字。不应使用任何字典中的单词作为密码。

应配置密码过期参数。以下命令必须以 `root` 身份运行或使用 `sudo` 运行。

确保 `/etc/libuser.conf` 文件的 `[import]` 部分包含以下行。

```shell
login_defs = /etc/login.defs
```

确保 `[userdefaults]` 部分中没有以以下文本开头的行，因为这些词会覆盖 `/etc/login.defs` 中的设置：

- `LU_SHADOWMAX`
- `LU_SHADOWMIN`
- `LU_SHADOWWARNING`

确保以下命令没有输出。使用此命令列出的任何帐户都应锁定。

```shell
grep "^+:" /etc/passwd /etc/shadow /etc/group
```

注意：强烈建议客户在初次设置后修改密码。

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

为上一条命令列出的所有目录设置 sticky 位（`# chmod +t {dir}`）。

查找所有对所有用户可写的文件，并修复列出的每个文件。

```shell
find / -xdev -type f -perm -0002 -print
```

为上述命令列出的所有文件设置正确的权限（`# chmod o-w {file}`）。

查找所有不属于有效用户或组的文件，并根据情况为其分配所有者或删除文件。

```shell
find / -xdev ( -nouser -o -nogroup ) -print
```

查找所有对所有用户可写的目录，并确保其所有者是 root 或系统帐户之一（假定只有系统帐户的用户 ID 小于 500）。如果命令产生任何输出，请验证所有权设置是否正确，或将其重新分配给 root。

```shell
find / -xdev -type d -perm -0002 -uid +500 -print
```

可以使用可插拔认证模块（PAM）框架配置认证设置，例如密码质量、密码过期策略、密码复用、密码重试次数等。PAM 会在 `/etc/pam.d` 目录中查找特定于应用的配置信息。运行 `authconfig` 或 `system-config-authentication` 会重写 PAM 配置文件，销毁手动完成的修改并替换为系统默认值。

默认的 `pam_cracklib` PAM 模块提供密码强度检查。要按照美国国防部指南的建议，配置 `pam_cracklib`，要求密码至少包含一个大写字符、小写字符、数字和特殊字符，请编辑 `/etc/pam.d/system-auth` 文件，在与 password requisite `pam_cracklib.so try_first_pass` 对应的行中加入以下参数。

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
password required pam_cracklib.so try_first_pass retry=3\minlen=14 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1
```

可以根据安全策略要求设置这些参数。注意，这些密码限制不适用于 root 密码。

`pam_tally2` PAM 模块可以在指定次数的登录失败后锁定用户帐户。要强制执行密码锁定，请编辑 `/etc/pam.d/system-auth` 文件，加入以下行：

- 第一条 auth 行应包含：

    ```shell
    auth required pam_tally2.so deny=5 onerr=fail unlock_time=900
    ```

- 第一条 account 行应包含：

    ```shell
    account required pam_tally2.so
    ```

这里，deny 参数设为将重试次数限制为 5，`unlock_time` 设为 900 秒，使帐户锁定 900 秒后解锁。可以根据安全策略要求适当配置这些参数。可以使用 `pam_tally2` 工具手动解锁已锁定的帐户：

```shell
/sbin/pam_tally2 --user {username} --reset
```

可以使用 PAM 限制重复使用近期密码。可以为 `pam_unix` 模块设置 remember 选项，使其记住近期密码并阻止复用。为此，请编辑 `/etc/pam.d/system-auth` 中的相应行，加入 remember 选项。

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
