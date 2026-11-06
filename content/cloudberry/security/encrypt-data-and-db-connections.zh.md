---
title: "加密数据与数据库连接"
description: "本文介绍如何加密数据库中的静态数据和网络中传输的数据，以防止窃听和中间人攻击。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/security/encrypt-data-and-db-connections.md"
---

- 客户端与 Coordinator 数据库之间的连接可以使用 SSL 加密。此功能由 `ssl` 服务器配置参数启用，该参数默认为 `off`。将 `ssl` 参数设为 `on` 后，客户端与 Coordinator 之间的通信就可以加密。必须为 Coordinator 数据库配置 SSL。有关使用 SSL 加密客户端连接的详细信息，请参阅[配置 OpenSSL](/cloudberry/security/client-auth/#openssl-configuration)。
- Apache Cloudberry 支持对 Cloudberry 并行文件分发服务器 `gpfdist` 与 Segment 主机之间传输的数据进行 SSL 加密。有关详细信息，请参阅[加密 gpfdist 连接](#encrypt-gpfdist-connections)。
- `pgcrypto` 加密/解密函数模块可以保护数据库中的静态数据。列级加密可以保护社会保障号码、信用卡号码等敏感信息。有关详细信息，请参阅[使用 pgcrypto 加密静态数据](#encrypt-data-at-rest-with-pgcrypto)。

## 加密 gpfdist 连接 {#encrypt-gpfdist-connections}

`gpfdists` 协议是 `gpfdist` 协议的安全版本，可以安全地识别文件服务器和 Apache Cloudberry，并加密两者之间的通信。使用 `gpfdists` 可以防止窃听和中间人攻击。

`gpfdists` 协议实现了客户端/服务器 SSL 安全，具有以下重要特性：

- 必须使用客户端证书。
- 不支持多语言证书。
- 不支持证书吊销列表（CRL）。
- 最低 TLS 版本要求为 1.2。
- 支持 SSL 重新协商。
- SSL 忽略主机不匹配参数设为 false。
- `gpfdist` 文件服务器（server.key）或 Apache Cloudberry（client.key）不支持包含口令短语的私钥。
- 用户有责任签发适合所用操作系统的证书。通常支持将证书转换为所需格式，例如使用 [https://www.sslshopper.com/ssl-converter.html](http://www.commoncriteriaportal.org/products/?expand#ALL) 中的 SSL Converter。

使用 `--ssl` 选项启动的 `gpfdist` 服务器只能与 `gpfdists` 协议通信。不使用 `--ssl` 选项启动的 `gpfdist` 服务器只能与 `gpfdist` 协议通信。有关 `gpfdist` 的更多详细信息，请参阅[`gpfdist`](/cloudberry/data-loading/files/load-data-using-gpfdist/)。

启用 `gpfdists` 协议有两种方式：

- 使用 `--ssl` 选项运行 `gpfdist`，然后在 `CREATE EXTERNAL TABLE` 语句的 `LOCATION` 子句中使用 `gpfdists` 协议。
- 使用 SSL 选项设为 true 的 YAML 控制文件运行 `gpload`。运行 `gpload` 会使用 `--ssl` 选项启动 `gpfdist` 服务器，然后使用 `gpfdists` 协议。

使用 gpfdists 时，以下客户端证书必须位于每个 Segment 的 `$PGDATA/gpfdists` 目录中：

- 客户端证书文件 `client.crt`
- 客户端私钥文件 `client.key`
- 受信任的证书颁发机构 `root.crt`

> [!WARNING] 警告
> 不要使用口令短语保护私钥。服务器不会提示输入私钥口令短语；如果需要口令短语，加载数据时会因错误而失败。

使用带 SSL 的 `gpload` 时，在 YAML 控制文件中指定服务器证书的位置。使用带 SSL 的 `gpfdist` 时，通过 --ssl 选项指定服务器证书的位置。

以下示例展示如何安全地将数据加载到外部表中。示例使用 `gpfdists` 协议，从所有扩展名为 `txt` 的文件创建名为 `ext_expenses` 的可读外部表。文件使用竖线（`|`）作为列分隔符，并使用空格表示 null。

1. 在 Segment 主机上使用 `--ssl` 选项运行 `gpfdist`。
2. 登录数据库并运行以下命令：

    ```sql
    =# CREATE EXTERNAL TABLE ext_expenses 
       ( name text, date date, amount float4, category text, desc1 text )
    LOCATION ('gpfdists://etlhost-1:8081/*.txt', 'gpfdists://etlhost-2:8082/*.txt')
    FORMAT 'TEXT' ( DELIMITER '|' NULL ' ') ;
    ```

## 使用 pgcrypto 加密静态数据 {#encrypt-data-at-rest-with-pgcrypto}

Apache Cloudberry 的 pgcrypto 模块提供用于加密数据库中静态数据的函数。管理员可以加密社会保障号码、信用卡号码等敏感信息所在的列，从而增加一层保护。以加密形式存储的数据库数据无法被没有加密密钥的用户读取，也无法直接从磁盘读取。

安装 Apache Cloudberry 时默认会安装 pgcrypto。必须在每个希望使用该模块的数据库中显式启用 pgcrypto。

pgcrypto 支持使用对称和非对称加密进行 PGP 加密。对称加密使用同一个密钥加密和解密数据，速度比非对称加密快。在交换秘密密钥不存在问题的环境中，对称加密是首选方法。非对称加密使用公钥加密数据，使用私钥解密数据。它比对称加密慢，并且需要更强的密钥。

使用 pgcrypto 总会带来性能和可维护性成本。只对需要加密的数据使用加密非常重要。此外请注意，无法通过为加密数据建立索引来搜索加密数据。

实现数据库内加密前，请考虑以下 PGP 限制。

- 不支持签名。这也意味着不会检查加密子密钥是否属于 Coordinator 密钥。
- 不支持将加密密钥作为 Coordinator 密钥。通常不建议这样做，因此这一限制不应造成问题。
- 不支持多个子密钥。这看似可能造成问题，因为多子密钥是常见做法。但另一方面，不应将常规 GPG/PGP 密钥与 pgcrypto 配合使用，而应创建新密钥，因为两者的使用场景差异很大。

Apache Cloudberry 默认使用 zlib 编译；这样 PGP 加密函数就能在加密前压缩数据。使用 OpenSSL 编译时，将有更多算法可用。

由于 pgcrypto 函数在数据库服务器内部运行，数据和密码会以明文形式在 pgcrypto 与客户端应用程序之间传输。为获得最佳安全性，应在本地连接或使用 SSL 连接，并且应信任系统管理员和数据库管理员。

pgcrypto 会根据 PostgreSQL 主配置脚本的检测结果进行配置。

使用 `zlib` 编译时，pgcrypto 加密函数能够在加密前压缩数据。

Pgcrypto 提供从基础到高级的多种内置加密函数。下表列出了支持的加密算法。

|功能/值|内置|使用 OpenSSL|
|:------------------|:-------|:-----------|
|MD5|是|是|
|SHA1|是|是|
|SHA224/256/384/512|是|是 |
|其他摘要算法|否|是|
|Blowfish|是|是|
|AES|是|是|
|DES/3DES/CAST5|否|是|
|原始加密|是|是|
|PGP 对称密钥|是|是|
|PGP 公钥|是|是|

### 创建 PGP 密钥 {#create-pgp-keys}

要在 Apache Cloudberry 中使用 PGP 非对称加密，必须先创建并安装公钥和私钥。

本节假定你在安装了 Gnu Privacy Guard（`gpg`）命令行工具的 Linux 计算机上安装 Apache Cloudberry。请使用最新版本的 GPG 创建密钥。请从 [https://www.gnupg.org/download/](https://www.gnupg.org/download/) 为所用操作系统下载并安装 Gnu Privacy Guard（GPG）。GnuPG 网站提供常用 Linux 发行版的安装程序，以及 Windows 和 Mac OS X 安装程序的链接。

1. 以 root 身份运行以下命令，并从菜单中选择选项 1：

    ```shell
    # gpg --gen-key 
    gpg (GnuPG) 2.0.14; Copyright (C) 2009 Free Software Foundation, Inc.
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.
     
    gpg: directory '/root/.gnupg' created
    gpg: new configuration file '/root/.gnupg/gpg.conf' created
    gpg: WARNING: options in '/root/.gnupg/gpg.conf' are not yet active during this run
    gpg: keyring '/root/.gnupg/secring.gpg' created
    gpg: keyring '/root/.gnupg/pubring.gpg' created
    Please select what kind of key you want:
     (1) RSA and RSA (default)
     (2) DSA and Elgamal
     (3) DSA (sign only)
     (4) RSA (sign only)
    Your selection? **1**
    ```

2. 根据提示输入信息并按照说明操作，如下例所示：

    ```shell
    RSA keys may be between 1024 and 4096 bits long.
    What keysize do you want? (2048) Press enter to accept default key size
    Requested keysize is 2048 bits
    Please specify how long the key should be valid.
     0 = key does not expire
     <n> = key expires in n days
     <n>w = key expires in n weeks
     <n>m = key expires in n months
     <n>y = key expires in n years
     Key is valid for? (0) **365**
    Key expires at Wed 13 Jan 2016 10:35:39 AM PST
    Is this correct? (y/N) **y**
    
    GnuPG needs to construct a user ID to identify your key.
    
    Real name: **John Doe**
    Email address: **jdoe@email.com**
    Comment: 
    You selected this USER-ID:
     "John Doe <jdoe@email.com>"
    
    Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? **O**
    You need a Passphrase to protect your secret key.
    *(For this demo the passphrase is blank.)*
    can't connect to '/root/.gnupg/S.gpg-agent': No such file or directory
    You don't want a passphrase - this is probably a *bad* idea!
    I will do it anyway.  You can change your passphrase at any time,
    using this program with the option "--edit-key".
    
    We need to generate a lot of random bytes. It is a good idea to perform
    some other action (type on the keyboard, move the mouse, utilize the
    disks) during the prime generation; this gives the random number
    generator a better chance to gain enough entropy.
    We need to generate a lot of random bytes. It is a good idea to perform
    some other action (type on the keyboard, move the mouse, utilize the
    disks) during the prime generation; this gives the random number
    generator a better chance to gain enough entropy.
    gpg: /root/.gnupg/trustdb.gpg: trustdb created
    gpg: key 2027CC30 marked as ultimately trusted
    public and secret key created and signed.
    
    gpg:  checking the trustdbgpg: 
          3 marginal(s) needed, 1 complete(s) needed, PGP trust model
    gpg:  depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 1u
    gpg:  next trustdb check due at 2016-01-13
    pub   2048R/2027CC30 2015-01-13 [expires: 2016-01-13]
          Key fingerprint = 7EDA 6AD0 F5E0 400F 4D45   3259 077D 725E 2027 CC30
    uid                  John Doe <jdoe@email.com>
    sub   2048R/4FD2EFBB 2015-01-13 [expires: 2016-01-13]
    ```

3. 输入以下命令列出 PGP 密钥：

    ```shell
    gpg --list-secret-keys 
    /root/.gnupg/secring.gpg
    ------------------------
    sec   2048R/2027CC30 2015-01-13 [expires: 2016-01-13]
    uid                  John Doe <jdoe@email.com>
    ssb   2048R/4FD2EFBB 2015-01-13
    ```

    2027CC30 是公钥，将用于加密数据库中的数据。4FD2EFBB 是私钥（秘密密钥），将用于解密数据。

4. 使用以下命令导出密钥：

    ```shell
    # gpg -a --export 4FD2EFBB > public.key
    # gpg -a --export-secret-keys 2027CC30 > secret.key
    ```

有关 PGP 加密函数的更多信息，请参阅 [pgcrypto](https://www.postgresql.org/docs/14/pgcrypto.html) 文档。

### 使用 PGP 加密表中的数据 {#encrypt-data-in-tables-using-pgp}

本节展示如何使用生成的 PGP 密钥加密插入列中的数据。

1. 转储 `public.key` 文件的内容，然后将其复制到剪贴板：

    ```shell
    # cat public.key
    -----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: GnuPG v2.0.14 (GNU/Linux)
                
    mQENBFS1Zf0BCADNw8Qvk1V1C36Kfcwd3Kpm/dijPfRyyEwB6PqKyA05jtWiXZTh
    2His1ojSP6LI0cSkIqMU9LAlncecZhRIhBhuVgKlGSgd9texg2nnSL9Admqik/yX
    R5syVKG+qcdWuvyZg9oOOmeyjhc3n+kkbRTEMuM3flbMs8shOwzMvstCUVmuHU/V
    vG5rJAe8PuYDSJCJ74I6w7SOH3RiRIc7IfL6xYddV42l3ctd44bl8/i71hq2UyN2
    /Hbsjii2ymg7ttw3jsWAx2gP9nssDgoy8QDy/o9nNqC8EGlig96ZFnFnE6Pwbhn+
    ic8MD0lK5/GAlR6Hc0ZIHf8KEcavruQlikjnABEBAAG0HHRlc3Qga2V5IDx0ZXN0
    a2V5QGVtYWlsLmNvbT6JAT4EEwECACgFAlS1Zf0CGwMFCQHhM4AGCwkIBwMCBhUI
    AgkKCwQWAgMBAh4BAheAAAoJEAd9cl4gJ8wwbfwH/3VyVsPkQl1owRJNxvXGt1bY
    7BfrvU52yk+PPZYoes9UpdL3CMRk8gAM9bx5Sk08q2UXSZLC6fFOpEW4uWgmGYf8
    JRoC3ooezTkmCBW8I1bU0qGetzVxopdXLuPGCE7hVWQe9HcSntiTLxGov1mJAwO7
    TAoccXLbyuZh9Rf5vLoQdKzcCyOHh5IqXaQOT100TeFeEpb9TIiwcntg3WCSU5P0
    DGoUAOanjDZ3KE8Qp7V74fhG1EZVzHb8FajR62CXSHFKqpBgiNxnTOk45NbXADn4
    eTUXPSnwPi46qoAp9UQogsfGyB1XDOTB2UOqhutAMECaM7VtpePv79i0Z/NfnBe5
    AQ0EVLVl/QEIANabFdQ+8QMCADOipM1bF/JrQt3zUoc4BTqICaxdyzAfz0tUSf/7
    Zro2us99GlARqLWd8EqJcl/xmfcJiZyUam6ZAzzFXCgnH5Y1sdtMTJZdLp5WeOjw
    gCWG/ZLu4wzxOFFzDkiPv9RDw6e5MNLtJrSp4hS5o2apKdbO4Ex83O4mJYnav/rE
    iDDCWU4T0lhv3hSKCpke6LcwsX+7liozp+aNmP0Ypwfi4hR3UUMP70+V1beFqW2J
    bVLz3lLLouHRgpCzla+PzzbEKs16jq77vG9kqZTCIzXoWaLljuitRlfJkO3vQ9hO
    v/8yAnkcAmowZrIBlyFg2KBzhunYmN2YvkUAEQEAAYkBJQQYAQIADwUCVLVl/QIb
    DAUJAeEzgAAKCRAHfXJeICfMMOHYCACFhInZA9uAM3TC44l+MrgMUJ3rW9izrO48
    WrdTsxR8WkSNbIxJoWnYxYuLyPb/shc9k65huw2SSDkj//0fRrI61FPHQNPSvz62
    WH+N2lasoUaoJjb2kQGhLOnFbJuevkyBylRz+hI/+8rJKcZOjQkmmK8Hkk8qb5x/
    HMUc55H0g2qQAY0BpnJHgOOQ45Q6pk3G2/7Dbek5WJ6K1wUrFy51sNlGWE8pvgEx
    /UUZB+dYqCwtvX0nnBu1KNCmk2AkEcFK3YoliCxomdOxhFOv9AKjjojDyC65KJci
    Pv2MikPS2fKOAg1R3LpMa8zDEtl4w3vckPQNrQNnYuUtfj6ZoCxv
    =XZ8J
    -----END PGP PUBLIC KEY BLOCK-----
    ```

2. 创建名为 `userssn` 的表，并插入一些敏感数据；本例中插入 Bob 和 Alice 的社会保障号码。在 `dearmor(` 后粘贴 public.key 的内容。

    ```
    CREATE TABLE userssn( ssn_id SERIAL PRIMARY KEY, 
        username varchar(100), ssn bytea); 
    
    INSERT INTO userssn(username, ssn)
    SELECT robotccs.username, pgp_pub_encrypt(robotccs.ssn, keys.pubkey) AS ssn
    FROM ( 
            VALUES ('Alice', '123-45-6788'), ('Bob', '123-45-6799')) 
                AS robotccs(username, ssn)
    CROSS JOIN  (SELECT  dearmor('-----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: GnuPG v2.0.14 (GNU/Linux)
                
    mQENBFS1Zf0BCADNw8Qvk1V1C36Kfcwd3Kpm/dijPfRyyEwB6PqKyA05jtWiXZTh
    2His1ojSP6LI0cSkIqMU9LAlncecZhRIhBhuVgKlGSgd9texg2nnSL9Admqik/yX
    R5syVKG+qcdWuvyZg9oOOmeyjhc3n+kkbRTEMuM3flbMs8shOwzMvstCUVmuHU/V
    vG5rJAe8PuYDSJCJ74I6w7SOH3RiRIc7IfL6xYddV42l3ctd44bl8/i71hq2UyN2
    /Hbsjii2ymg7ttw3jsWAx2gP9nssDgoy8QDy/o9nNqC8EGlig96ZFnFnE6Pwbhn+
    ic8MD0lK5/GAlR6Hc0ZIHf8KEcavruQlikjnABEBAAG0HHRlc3Qga2V5IDx0ZXN0
    a2V5QGVtYWlsLmNvbT6JAT4EEwECACgFAlS1Zf0CGwMFCQHhM4AGCwkIBwMCBhUI
    AgkKCwQWAgMBAh4BAheAAAoJEAd9cl4gJ8wwbfwH/3VyVsPkQl1owRJNxvXGt1bY
    7BfrvU52yk+PPZYoes9UpdL3CMRk8gAM9bx5Sk08q2UXSZLC6fFOpEW4uWgmGYf8
    JRoC3ooezTkmCBW8I1bU0qGetzVxopdXLuPGCE7hVWQe9HcSntiTLxGov1mJAwO7
    TAoccXLbyuZh9Rf5vLoQdKzcCyOHh5IqXaQOT100TeFeEpb9TIiwcntg3WCSU5P0
    DGoUAOanjDZ3KE8Qp7V74fhG1EZVzHb8FajR62CXSHFKqpBgiNxnTOk45NbXADn4
    eTUXPSnwPi46qoAp9UQogsfGyB1XDOTB2UOqhutAMECaM7VtpePv79i0Z/NfnBe5
    AQ0EVLVl/QEIANabFdQ+8QMCADOipM1bF/JrQt3zUoc4BTqICaxdyzAfz0tUSf/7
    Zro2us99GlARqLWd8EqJcl/xmfcJiZyUam6ZAzzFXCgnH5Y1sdtMTJZdLp5WeOjw
    gCWG/ZLu4wzxOFFzDkiPv9RDw6e5MNLtJrSp4hS5o2apKdbO4Ex83O4mJYnav/rE
    iDDCWU4T0lhv3hSKCpke6LcwsX+7liozp+aNmP0Ypwfi4hR3UUMP70+V1beFqW2J
    bVLz3lLLouHRgpCzla+PzzbEKs16jq77vG9kqZTCIzXoWaLljuitRlfJkO3vQ9hO
    v/8yAnkcAmowZrIBlyFg2KBzhunYmN2YvkUAEQEAAYkBJQQYAQIADwUCVLVl/QIb
    DAUJAeEzgAAKCRAHfXJeICfMMOHYCACFhInZA9uAM3TC44l+MrgMUJ3rW9izrO48
    WrdTsxR8WkSNbIxJoWnYxYuLyPb/shc9k65huw2SSDkj//0fRrI61FPHQNPSvz62
    WH+N2lasoUaoJjb2kQGhLOnFbJuevkyBylRz+hI/+8rJKcZOjQkmmK8Hkk8qb5x/
    HMUc55H0g2qQAY0BpnJHgOOQ45Q6pk3G2/7Dbek5WJ6K1wUrFy51sNlGWE8pvgEx
    /UUZB+dYqCwtvX0nnBu1KNCmk2AkEcFK3YoliCxomdOxhFOv9AKjjojDyC65KJci
    Pv2MikPS2fKOAg1R3LpMa8zDEtl4w3vckPQNrQNnYuUtfj6ZoCxv
    =XZ8J
    -----END PGP PUBLIC KEY BLOCK-----' AS pubkey) AS keys;
    ```

3. 验证 `ssn` 列已加密。

    ```shell
    test_db=# select * from userssn;
    ssn_id   | 1
    username | Alice
    ssn      | \301\300L\003\235M%_O\322\357\273\001\010\000\272\227\010\341\216\360\217C\020\261)_\367
    [\227\034\313:C\354d<\337\006Q\351('\2330\031lX\263Qf\341\262\200\3015\235\036AK\242fL+\315g\322
    7u\270*\304\361\355\220\021\330"\200%\264\274}R\213\377\363\235\366\030\023)\364!\331\303\237t\277=
    f \015\004\242\231\263\225%\032\271a\001\035\277\021\375X\232\304\305/\340\334\0131\325\344[~\362\0
    37-\251\336\303\340\377_\011\275\301/MY\334\343\245\244\372y\257S\374\230\346\277\373W\346\230\276\
    017fi\226Q\307\012\326\3646\000\326\005:E\364W\252=zz\010(:\343Y\237\257iqU\0326\350=v0\362\327\350\
    315G^\027:K_9\254\362\354\215<\001\304\357\331\355\323,\302\213Fe\265\315\232\367\254\245%(\\\373
    4\254\230\331\356\006B\257\333\326H\022\013\353\216F?\023\220\370\035vH5/\227\344b\322\227\026\362=\
    42\033\322<\001}\243\224;)\030zqX\214\340\221\035\275U\345\327\214\032\351\223c\2442\345\304K\016\
    011\214\307\227\237\270\026'R\205\205a~1\263\236[\037C\260\031\205\374\245\317\033k|\366\253\037
    ---------+--------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------
    ssn_id   | 2
    username | Bob
    ssn      | \301\300L\003\235M%_O\322\357\273\001\007\377t>\345\343,\200\256\272\300\012\033M4\265\032L
    L[v\262k\244\2435\264\232B\357\370d9\375\011\002\327\235<\246\210b\030\012\337@\226Z\361\246\032\00
    7'\012c\353]\355d7\360T\335\314\367\370;X\371\350*\231\212\260B\010#RQ0\223\253c7\0132b\355\242\233\34
    1\000\370\370\366\013\022\357\005i\202~\005\\z\301o\012\230Z\014\362\244\324&\243g\351\362\325\375
    \213\032\226$\2751\256XR\346k\266\030\234\267\201vUh\004\250\337A\231\223u\247\366/i\022\275\276\350\2
    20\316\306|\203+\010\261;\232\254tp\255\243\261\373Rq;\316w\357\006\207\374U\333\365\365\245hg\031\005
    \322\347ea\220\015l\212g\337\264\336b\263\004\311\210.4\340G+\221\274D\035\375\2216\241'\346a0\273wE\2
    12\342y^\202\262|A7\202t\240\333p\345G\373\253\243oCO\011\360\247\211\014\024{\272\271\322<\001\267
    \347\240\005\213\0078\036\210\307$\317\322\311\222\035\354\006<\266\264\004\376\251q\256\220(+\030\
    3270\013c\327\272\212%\363\033\252\322\337\354\276\225\232\201\212^\304\210\2269@\3230\370{
    ```

4. 从数据库中提取 public.key ID：

    ```shell
    SELECT pgp_key_id(dearmor('-----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: GnuPG v2.0.14 (GNU/Linux)
    
    mQENBFS1Zf0BCADNw8Qvk1V1C36Kfcwd3Kpm/dijPfRyyEwB6PqKyA05jtWiXZTh
    2His1ojSP6LI0cSkIqMU9LAlncecZhRIhBhuVgKlGSgd9texg2nnSL9Admqik/yX
    R5syVKG+qcdWuvyZg9oOOmeyjhc3n+kkbRTEMuM3flbMs8shOwzMvstCUVmuHU/V
    vG5rJAe8PuYDSJCJ74I6w7SOH3RiRIc7IfL6xYddV42l3ctd44bl8/i71hq2UyN2
    /Hbsjii2ymg7ttw3jsWAx2gP9nssDgoy8QDy/o9nNqC8EGlig96ZFnFnE6Pwbhn+
    ic8MD0lK5/GAlR6Hc0ZIHf8KEcavruQlikjnABEBAAG0HHRlc3Qga2V5IDx0ZXN0
    a2V5QGVtYWlsLmNvbT6JAT4EEwECACgFAlS1Zf0CGwMFCQHhM4AGCwkIBwMCBhUI
    AgkKCwQWAgMBAh4BAheAAAoJEAd9cl4gJ8wwbfwH/3VyVsPkQl1owRJNxvXGt1bY
    7BfrvU52yk+PPZYoes9UpdL3CMRk8gAM9bx5Sk08q2UXSZLC6fFOpEW4uWgmGYf8
    JRoC3ooezTkmCBW8I1bU0qGetzVxopdXLuPGCE7hVWQe9HcSntiTLxGov1mJAwO7
    TAoccXLbyuZh9Rf5vLoQdKzcCyOHh5IqXaQOT100TeFeEpb9TIiwcntg3WCSU5P0
    DGoUAOanjDZ3KE8Qp7V74fhG1EZVzHb8FajR62CXSHFKqpBgiNxnTOk45NbXADn4
    eTUXPSnwPi46qoAp9UQogsfGyB1XDOTB2UOqhutAMECaM7VtpePv79i0Z/NfnBe5
    AQ0EVLVl/QEIANabFdQ+8QMCADOipM1bF/JrQt3zUoc4BTqICaxdyzAfz0tUSf/7
    Zro2us99GlARqLWd8EqJcl/xmfcJiZyUam6ZAzzFXCgnH5Y1sdtMTJZdLp5WeOjw
    gCWG/ZLu4wzxOFFzDkiPv9RDw6e5MNLtJrSp4hS5o2apKdbO4Ex83O4mJYnav/rE
    iDDCWU4T0lhv3hSKCpke6LcwsX+7liozp+aNmP0Ypwfi4hR3UUMP70+V1beFqW2J
    bVLz3lLLouHRgpCzla+PzzbEKs16jq77vG9kqZTCIzXoWaLljuitRlfJkO3vQ9hO
    v/8yAnkcAmowZrIBlyFg2KBzhunYmN2YvkUAEQEAAYkBJQQYAQIADwUCVLVl/QIb
    DAUJAeEzgAAKCRAHfXJeICfMMOHYCACFhInZA9uAM3TC44l+MrgMUJ3rW9izrO48
    WrdTsxR8WkSNbIxJoWnYxYuLyPb/shc9k65huw2SSDkj//0fRrI61FPHQNPSvz62
    WH+N2lasoUaoJjb2kQGhLOnFbJuevkyBylRz+hI/+8rJKcZOjQkmmK8Hkk8qb5x/
    HMUc55H0g2qQAY0BpnJHgOOQ45Q6pk3G2/7Dbek5WJ6K1wUrFy51sNlGWE8pvgEx
    /UUZB+dYqCwtvX0nnBu1KNCmk2AkEcFK3YoliCxomdOxhFOv9AKjjojDyC65KJci
    Pv2MikPS2fKOAg1R3LpMa8zDEtl4w3vckPQNrQNnYuUtfj6ZoCxv
    =XZ8J
    -----END PGP PUBLIC KEY BLOCK-----'));
    
    pgp_key_id | 9D4D255F4FD2EFBB
    ```

    这表明用于加密 `ssn` 列的 PGP 密钥 ID 是 `9D4D255F4FD2EFBB`。建议每次创建新密钥时都执行此步骤，然后保存该 ID 以便跟踪。

    可以使用此密钥查看用于加密数据的密钥对：

    ```shell
    SELECT username, pgp_key_id(ssn) As key_used
    FROM userssn;
    username | Bob
    key_used | 9D4D255F4FD2EFBB
    ---------+-----------------
    username | Alice
    key_used | 9D4D255F4FD2EFBB
    
    ```

    > [!NOTE] 注意
    > 不同的密钥可能具有相同的 ID。这种情况很少见，但属于正常现象。客户端应用程序应尝试使用每个密钥解密，以确定哪个密钥适用——类似于处理 `ANYKEY`。请参阅 pgcrypto 文档中的 [`pgp_key_id()`](https://www.postgresql.org/docs/14/pgcrypto.html)。

5. 使用私钥解密数据。

    ```sql
    SELECT username, pgp_pub_decrypt(ssn, keys.privkey) 
                     AS decrypted_ssn FROM userssn
                     CROSS JOIN
                     (SELECT dearmor('-----BEGIN PGP PRIVATE KEY BLOCK-----
    Version: GnuPG v2.0.14 (GNU/Linux)
    
    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
    =fa+6
    -----END PGP PRIVATE KEY BLOCK-----') AS privkey) AS keys;
    
    username | decrypted_ssn 
    ----------+---------------
     Alice    | 123-45-6788
     Bob      | 123-45-6799
    (2 rows)
    ```

    如果创建的密钥带有口令短语，可能需要在此处输入该口令短语。不过，就本例而言，口令短语为空。

### 密钥管理 {#key-management}

无论使用的是对称（单个私钥）还是非对称（公钥和私钥）加密，都必须安全地存储 Coordinator 密钥或私钥。密钥可以存储在文件系统、密钥保管库、加密 USB、可信平台模块（TPM）或硬件安全模块（HSM）等多种位置。

规划密钥管理时，请考虑以下问题：

- 密钥将存储在哪里？
- 密钥应在何时过期？
- 如何保护密钥？
- 如何访问密钥？
- 如何恢复和吊销密钥？

开放 Web 应用程序安全项目（OWASP）提供了非常全面的[加密密钥安全指南](https://www.owasp.org/index.php/Cryptographic_Storage_Cheat_Sheet)。

## 使用 TDE 加密数据 {#encrypt-data-using-tde}

为满足保护用户数据安全的要求，Apache Cloudberry 支持透明数据加密（TDE）。

TDE 是一种用于加密数据库数据文件的技术：

- “数据”指数据库中的数据。
- 文件在硬盘上以密文存储，在内存中以明文处理。TDE 用于保护静态数据，因此也称为静态数据加密。
- “透明”意味着用户不需要改变操作习惯。TDE 自动管理加密/解密过程，无需用户或应用程序干预。

详情请参阅[透明数据加密](/cloudberry/security/transparent-data-encryption/)。
