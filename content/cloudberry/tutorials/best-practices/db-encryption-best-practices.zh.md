---
title: "加密数据与数据库连接"
description: "实施加密和管理密钥的最佳实践。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/best-practices/db-encryption-best-practices.md"
---

可以通过以下方式使用加密保护 Apache Cloudberry 系统中的数据：

- 客户端与 Coordinator 数据库之间的连接可以使用 SSL 加密。将服务器配置参数 `ssl` 设为 `on` 并编辑 `pg_hba.conf` 文件即可启用此功能。
- Apache Cloudberry 支持对 Cloudberry 并行文件分发服务器 `gpfdist` 与 Segment 主机之间传输的数据进行 SSL 加密。更多信息请参见[加密 gpfdist 连接](#encrypt-gpfdist-connections)。
- Apache Cloudberry 集群中主机之间的网络通信可以使用 IPsec 加密。集群中的每对主机之间都会建立经过身份验证的加密 VPN。请查阅操作系统文档了解 IPsec 支持，或考虑使用 [Zettaset](https://www.zettaset.com) 提供的第三方方案。
- 提供加密和解密函数的 `pgcrypto` 模块可以保护数据库中静态存储的数据。列级加密可以保护密码、社会安全号码或信用卡号等敏感信息。示例请参见[使用 PGP 加密表中的数据](#encrypt-data-in-tables-using-pgp)。

## 最佳实践 {#best-practices}

- 加密可以确保只有拥有解密所需密钥的用户才能查看数据。
- 加密和解密数据会产生性能开销；只加密确实需要加密的数据。
- 在生产系统实施任何加密方案前执行性能测试。
- 生产 Apache Cloudberry 系统中的服务器证书应由证书颁发机构（CA）签名，使客户端能够对服务器进行身份验证。如果所有客户端都位于同一组织内，CA 可以是本地 CA。
- 客户端连接通过不安全链路时，应使用 SSL 加密连接 Apache Cloudberry。
- 对称加密方案使用同一个密钥进行加密和解密，性能优于非对称方案；只要能够安全共享密钥，就应使用对称加密。
- 使用 pgcrypto 模块中的函数加密磁盘上的数据。数据在数据库进程中加密和解密，因此必须使用 SSL 保护客户端连接，避免传输未加密的数据。
- 使用 gpfdists 协议保护 ETL 数据在加载到数据库或从数据库卸载时的安全。参见[加密 gpfdist 连接](#encrypt-gpfdist-connections)。

## 密钥管理 {#key-management}

无论使用对称密码（单个私钥）还是非对称密码（公钥和私钥），都必须安全地存储 Coordinator 密钥或私钥。存储加密密钥有多种选择，例如文件系统、密钥保管库、加密 USB、可信平台模块（TPM）或硬件安全模块（HSM）。

规划密钥管理时，请考虑以下问题：

- 密钥将存储在哪里？
- 密钥应在何时过期？
- 如何保护密钥？
- 如何访问密钥？
- 如何恢复和撤销密钥？

开放 Web 应用安全项目（OWASP）提供了非常全面的[保护加密密钥指南](https://www.owasp.org/index.php/Cryptographic_Storage_Cheat_Sheet)。

## 使用 pgcrypto 加密静态数据 {#encrypt-data-at-rest-with-pgcrypto}

Apache Cloudberry 的 pgcrypto 模块提供用于加密数据库中静态数据的函数。管理员可以加密包含社会安全号码或信用卡号等敏感信息的列，从而提供额外的保护层。以加密形式存储的数据库数据无法被没有加密密钥的用户读取，也无法直接从磁盘读取。

安装 Apache Cloudberry 时默认会安装 pgcrypto。必须在需要使用该模块的每个数据库中显式启用 pgcrypto。

pgcrypto 支持使用对称和非对称加密执行 PGP 加密。对称加密使用同一个密钥加密和解密数据，速度比非对称加密快。在交换密钥不存在问题的环境中，优先使用对称加密。非对称加密使用公钥加密数据，使用私钥解密数据。这比对称加密慢，并且需要更强的密钥。

使用 pgcrypto 总会带来性能和可维护性成本。只应对需要加密的数据使用加密功能。还要注意，无法通过为加密数据建立索引来搜索这些数据。

实施数据库内加密前，请考虑以下 PGP 限制。

- 不支持签名。这也意味着系统不会检查加密子密钥是否属于 Coordinator 密钥。
- 不支持将加密密钥作为 Coordinator 密钥。通常不建议这样做，因此这一限制不应造成问题。
- 不支持多个子密钥。这看起来可能是个问题，因为使用多个子密钥很常见。但另一方面，不应将常规 GPG/PGP 密钥用于 pgcrypto，而应创建新密钥，因为两者的使用场景差异很大。

Apache Cloudberry 默认使用 zlib 编译；这样 PGP 加密函数就能在加密前压缩数据。使用 OpenSSL 编译时，还会提供更多算法。

由于 pgcrypto 函数在数据库服务器内部运行，数据和密码会以明文形式在 pgcrypto 与客户端应用之间传输。为了获得最佳安全性，应使用本地连接或 SSL 连接，并且应信任系统管理员和数据库管理员。

pgcrypto 会根据 PostgreSQL 主配置脚本的检测结果自行配置。

使用 `zlib` 编译时，pgcrypto 加密函数能够在加密前压缩数据。

Pgcrypto 提供从基础到高级内置函数的不同加密级别。下表列出了支持的加密算法。

|值和功能|内置|使用 OpenSSL|
|:------------------|:-------|:-----------|
|MD5|是|是|
|SHA1|是|是|
|SHA224/256/384/512|是|是 |
|其他摘要算法|否|是 |
|Blowfish|是|是|
|AES|是|是|
|DES/3DES/CAST5|否|是|
|原始加密|是|是|
|PGP 对称密钥|是|是|
|PGP 公钥|是|是|

## 创建 PGP 密钥 {#create-pgp-keys}

要在 Apache Cloudberry 中使用 PGP 非对称加密，必须先创建并安装公钥和私钥。

本节假定你在安装了 Gnu Privacy Guard（`gpg`）命令行工具的 Linux 机器上安装 Apache Cloudberry。建议使用最新版本的 GPG 创建密钥。请从 [https://www.gnupg.org/download/](https://www.gnupg.org/download/) 下载并为你的操作系统安装 Gnu Privacy Guard（GPG）。GnuPG 网站提供常见 Linux 发行版的安装程序，以及 Windows 和 Mac OS X 安装程序的链接。

1. 以 root 身份运行以下命令，并在菜单中选择选项 1：

    ```shell
    # gpg --gen-key 
    gpg (GnuPG) 2.0.14; Copyright (C) 2009 Free Software Foundation, Inc.
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.
     
    gpg: directory `/root/.gnupg' created
    gpg: new configuration file `/root/.gnupg/gpg.conf' created
    gpg: WARNING: options in `/root/.gnupg/gpg.conf' are not yet active during this run
    gpg: keyring `/root/.gnupg/secring.gpg' created
    gpg: keyring `/root/.gnupg/pubring.gpg' created
    Please select what kind of key you want:
     (1) RSA and RSA (default)
     (2) DSA and Elgamal
     (3) DSA (sign only)
     (4) RSA (sign only)
    Your selection? 1
    ```

2. 按照提示回答问题并遵循说明，如下例所示：

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
     Key is valid for? (0) 365
    Key expires at Wed 13 Jan 2016 10:35:39 AM PST
    Is this correct? (y/N) y
    
    GnuPG needs to construct a user ID to identify your key.
    
    Real name: John Doe
    Email address: jdoe@email.com
    Comment: 
    You selected this USER-ID:
     "John Doe <jdoe@email.com>"
    
    Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O
    You need a Passphrase to protect your secret key.
    (For this demo the passphrase is blank.)
    can't connect to `/root/.gnupg/S.gpg-agent': No such file or directory
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

    2027CC30 是公钥，将用于*加密*数据库中的数据。4FD2EFBB 是私钥（秘密密钥），将用于*解密*数据。

4. 使用以下命令导出密钥：

    ```shell
    # gpg -a --export 4FD2EFBB > public.key
    # gpg -a --export-secret-keys 2027CC30 > secret.key
    ```

有关 PGP 加密函数的更多信息，请参见 [pgcrypto](https://www.postgresql.org/docs/14/pgcrypto.html) 文档。

## 使用 PGP 加密表中的数据 {#encrypt-data-in-tables-using-pgp}

本节介绍如何使用生成的 PGP 密钥加密插入列中的数据。

1. 转储 `public.key` 文件的内容，然后将其复制到剪贴板：

    ```shell
    # cat public.key
    -----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: GnuPG v2.0.14 (GNU/Linux)
                
    mQENBFS1Zf0BCADNw8Qvk1V1C36Kfcwd3Kpm/dijPfRyyEwB6PqKyA05jtWiXZTh
    2His1ojSP6LI0cSkIqMU9LAlncecZhRIhBhuVgKlGSgd9texg2nnSL9Admqik/yX
    R5syVKG+qcdWuvyZg9oOOmeyjhc3n+kkbRTEMuM3flbMs8shOwzMvstCUVmuHU/V
    . . .
    WH+N2lasoUaoJjb2kQGhLOnFbJuevkyBylRz+hI/+8rJKcZOjQkmmK8Hkk8qb5x/
    HMUc55H0g2qQAY0BpnJHgOOQ45Q6pk3G2/7Dbek5WJ6K1wUrFy51sNlGWE8pvgEx
    /UUZB+dYqCwtvX0nnBu1KNCmk2AkEcFK3YoliCxomdOxhFOv9AKjjojDyC65KJci
    Pv2MikPS2fKOAg1R3LpMa8zDEtl4w3vckPQNrQNnYuUtfj6ZoCxv
    =XZ8J
    -----END PGP PUBLIC KEY BLOCK-----
    ```

2. 启用 `pgcrypto` 扩展：

    ```sql
    CREATE EXTENSION pgcrypto;
    ```

3. 创建一个名为 `userssn` 的表，并在本例中插入一些敏感数据，即 Bob 和 Alice 的社会安全号码。将 public.key 的内容粘贴到 "dearmor(" 之后。

    ```sql
    CREATE TABLE userssn( ssn_id SERIAL PRIMARY KEY, 
        username varchar(100), ssn bytea); 
    
    INSERT INTO userssn(username, ssn)
    SELECT robotccs.username, pgp_pub_encrypt(robotccs.ssn, keys.pubkey) AS
    ssn
    FROM (
    VALUES ('Alice', '123-45-6788'), ('Bob', '123-45-6799'))
    AS robotccs(username, ssn)
    CROSS JOIN (SELECT dearmor('-----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: GnuPG v2.0.22 (GNU/Linux)
    
    mQENBGCb7NQBCADfCoMFIbjb6dup8eJHgTpo8TILiIubqhqASHqUPe/v3eI+p9W8
    mZbTZo+EUFCJmFZx8RWw0s0t4DG3fzBQOv5y2oBEu9sg3ofgFkK6TaQV7ueZfifx
    S1DxQE8kWEFrGsB13VJlLMMLPr4tdjtaYOdn5b+3N4/8GOJALn2CeWrP8lIXaget
    . . .
    T9dl2HhMOatlVhBUOcYrqSBEWgwtQbX36hFzhp1tNCDOvtDpsfLNHJr8vIpXAeyz
    juW0/vEgrAtSK8P2/kmRsmNM/LJIbCBHD+tTSTHZ194+QYUc1KYXW4NV5LLW08MY
    skETyovyVDFYEpTMVrRKJYLROhEBv8cqYgKq1XtcIH8eiwJIZ0L1L/1Cw7Z/BpRT
    WbrwmhXTpqi+/Vdm7q9gPFoAfw/ur44hJGsc13bQxdmluTigSN2f+qf9RzA=
    =xdQf
    -----END PGP PUBLIC KEY BLOCK-----')  as pubkey) AS keys;
    ```

4. 验证 `ssn` 列已加密。

    ```sql
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
    011\214\307\227\237\270\026`R\205\205a~1\263\236[\037C\260\031\205\374\245\317\033k|\366\253\037
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
    7`\012c\353]\355d7\360T\335\314\367\370;X\371\350*\231\212\260B\010#RQ0\223\253c7\0132b\355\242\233\34
    1\000\370\370\366\013\022\357\005i\202~\005\\z\301o\012\230Z\014\362\244\324&\243g\351\362\325\375
    \213\032\226$\2751\256XR\346k\266\030\234\267\201vUh\004\250\337A\231\223u\247\366/i\022\275\276\350\2
    20\316\306|\203+\010\261;\232\254tp\255\243\261\373Rq;\316w\357\006\207\374U\333\365\365\245hg\031\005
    \322\347ea\220\015l\212g\337\264\336b\263\004\311\210.4\340G+\221\274D\035\375\2216\241`\346a0\273wE\2
    12\342y^\202\262|A7\202t\240\333p\345G\373\253\243oCO\011\360\247\211\014\024{\272\271\322<\001\267
    \347\240\005\213\0078\036\210\307$\317\322\311\222\035\354\006<\266\264\004\376\251q\256\220(+\030\
    3270\013c\327\272\212%\363\033\252\322\337\354\276\225\232\201\212^\304\210\2269@\3230\370{
    
    ```

5. 从数据库中提取 public.key 的 ID：

    ```sql
    SELECT pgp_key_id(dearmor('-----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: GnuPG v2.0.14 (GNU/Linux)
    
    mQENBFS1Zf0BCADNw8Qvk1V1C36Kfcwd3Kpm/dijPfRyyEwB6PqKyA05jtWiXZTh
    2His1ojSP6LI0cSkIqMU9LAlncecZhRIhBhuVgKlGSgd9texg2nnSL9Admqik/yX
    R5syVKG+qcdWuvyZg9oOOmeyjhc3n+kkbRTEMuM3flbMs8shOwzMvstCUVmuHU/V
    . . .
    WH+N2lasoUaoJjb2kQGhLOnFbJuevkyBylRz+hI/+8rJKcZOjQkmmK8Hkk8qb5x/
    HMUc55H0g2qQAY0BpnJHgOOQ45Q6pk3G2/7Dbek5WJ6K1wUrFy51sNlGWE8pvgEx
    /UUZB+dYqCwtvX0nnBu1KNCmk2AkEcFK3YoliCxomdOxhFOv9AKjjojDyC65KJci
    Pv2MikPS2fKOAg1R3LpMa8zDEtl4w3vckPQNrQNnYuUtfj6ZoCxv
    =XZ8J
    -----END PGP PUBLIC KEY BLOCK-----'));
    
    pgp_key_id | 9D4D255F4FD2EFBB
    ```

    这表明用于加密 `ssn` 列的 PGP 密钥 ID 是 9D4D255F4FD2EFBB。每次创建新密钥时都建议执行此步骤，并保存该 ID 以便跟踪。

    可以使用这个密钥查看用于加密数据的密钥对：

    ```sql
    SELECT username, pgp_key_id(ssn) As key_used                                                                                                                       FROM userssn;                                                                                                                                                                 username | Bob
    key_used | 9D4D255F4FD2EFBB
    ---------+-----------------
    username | Alice
    key_used | 9D4D255F4FD2EFBB
    ```

    > **注意** 不同密钥可能具有相同的 ID。这种情况很少见，但属于正常现象。客户端应用应尝试使用每个密钥解密，以确定哪个密钥适用——类似于处理 `ANYKEY`。参见 pgcrypto 文档中的 [pgp_key_id()](https://www.postgresql.org/docs/14/pgcrypto.html)。

6. 使用私钥解密数据。

    ```sql
    SELECT username, pgp_pub_decrypt(ssn, keys.privkey) 
                     AS decrypted_ssn FROM userssn
                     CROSS JOIN
                     (SELECT dearmor('-----BEGIN PGP PRIVATE KEY BLOCK-----
    Version: GnuPG v2.0.14 (GNU/Linux)
    
    lQOYBFS1Zf0BCADNw8Qvk1V1C36Kfcwd3Kpm/dijPfRyyEwB6PqKyA05jtWiXZTh
    2His1ojSP6LI0cSkIqMU9LAlncecZhRIhBhuVgKlGSgd9texg2nnSL9Admqik/yX
    R5syVKG+qcdWuvyZg9oOOmeyjhc3n+kkbRTEMuM3flbMs8shOwzMvstCUVmuHU/V
    . . .
    QNPSvz62WH+N2lasoUaoJjb2kQGhLOnFbJuevkyBylRz+hI/+8rJKcZOjQkmmK8H
    kk8qb5x/HMUc55H0g2qQAY0BpnJHgOOQ45Q6pk3G2/7Dbek5WJ6K1wUrFy51sNlG
    WE8pvgEx/UUZB+dYqCwtvX0nnBu1KNCmk2AkEcFK3YoliCxomdOxhFOv9AKjjojD
    yC65KJciPv2MikPS2fKOAg1R3LpMa8zDEtl4w3vckPQNrQNnYuUtfj6ZoCxv
    =fa+6
    -----END PGP PRIVATE KEY BLOCK-----') AS privkey) AS keys;
    
    username | decrypted_ssn 
    ----------+---------------
     Alice    | 123-45-6788
     Bob      | 123-45-6799
    (2 rows)
    
    
    ```

    如果创建密钥时设置了密码短语，可能需要在此处输入密码短语。但在本例中，密码短语为空。

## 加密 gpfdist 连接 {#encrypt-gpfdist-connections}

`gpfdists` 协议是 `gpfdist` 协议的安全版本，可以安全地识别文件服务器和 Apache Cloudberry，并加密两者之间的通信。使用 `gpfdists` 可以防范窃听和中间人攻击。

`gpfdists` 协议实现了客户端/服务器 SSL 安全机制，具有以下显著特性：

- 必须使用客户端证书。
- 不支持多语言证书。
- 不支持证书撤销列表（CRL）。
- 使用 TLSv1 协议和 `TLS_RSA_WITH_AES_128_CBC_SHA` 加密算法。这些 SSL 参数不可更改。
- 支持 SSL 重新协商。
- SSL 忽略主机不匹配参数设为 false。
- `gpfdist` 文件服务器（server.key）和 Apache Cloudberry（client.key）均不支持包含密码短语的私钥。
- 用户有责任签发适用于所用操作系统的证书。通常支持将证书转换为所需格式，例如使用 [https://www.sslshopper.com/ssl-converter.html](http://www.commoncriteriaportal.org/products/?expand#ALL) 中的 SSL Converter。

使用 `--ssl` 选项启动的 `gpfdist` 服务器只能使用 `gpfdists` 协议通信。不使用 `--ssl` 选项启动的 `gpfdist` 服务器只能使用 `gpfdist` 协议通信。

有两种方式可以启用 `gpfdists` 协议：

- 使用 `--ssl` 选项运行 `gpfdist`，然后在 `CREATE EXTERNAL TABLE` 语句的 `LOCATION` 子句中使用 `gpfdists` 协议。
- 使用将 SSL 选项设为 true 的 YAML 控制文件运行 `gpload`。运行 `gpload` 会使用 `--ssl` 选项启动 `gpfdist` 服务器，然后使用 `gpfdists` 协议。

使用 gpfdists 时，每个 Segment 的 `$PGDATA/gpfdists` 目录中必须包含以下客户端证书：

- 客户端证书文件 `client.crt`
- 客户端私钥文件 `client.key`
- 受信任的证书颁发机构证书 `root.crt`

> **重要** 不要使用密码短语保护私钥。服务器不会提示输入私钥密码短语；如果私钥需要密码短语，加载数据会报错并失败。

使用带 SSL 的 `gpload` 时，在 YAML 控制文件中指定服务器证书的位置。使用带 SSL 的 `gpfdist` 时，通过 --ssl 选项指定服务器证书的位置。

以下示例展示如何安全地将数据加载到外部表中。该示例使用 `gpfdists` 协议，从所有扩展名为 `txt` 的文件创建名为 `ext_expenses` 的可读外部表。文件使用竖线（`|`）作为列分隔符，并使用空格表示空值。

1. 在 Segment 主机上使用 `--ssl` 选项运行 `gpfdist`。
2. 登录数据库并运行以下命令：

    ```sql
    =# CREATE EXTERNAL TABLE ext_expenses 
       ( name text, date date, amount float4, category text, desc1 text )
    LOCATION ('gpfdists://etlhost-1:8081/*.txt', 'gpfdists://etlhost-2:8082/*.txt')
    FORMAT 'TEXT' ( DELIMITER '|' NULL ' ') ;
    ```
