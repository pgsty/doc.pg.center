---
title: "配置客户端认证"
description: "本节介绍如何配置 Apache Cloudberry 的客户端连接和认证。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/security/client-auth.md"
---

Apache Cloudberry 系统首次初始化时，会包含一个预定义的*超级用户*角色。该角色与初始化 Apache Cloudberry 系统的操作系统用户同名，称为 `gpadmin`。默认情况下，系统配置为只允许 `gpadmin` 角色从本地连接数据库。如果希望允许其他角色连接，或允许来自远程主机的连接，就必须配置 Apache Cloudberry 以允许这些连接。本节介绍如何配置 Apache Cloudberry 的客户端连接和认证。

## 允许连接到 Apache Cloudberry {#allow-connections-to-apache-cloudberry}

客户端访问和认证由名为 `pg_hba.conf` 的配置文件控制，这是标准的 PostgreSQL 基于主机的认证文件。有关此文件的详细信息，请参阅 PostgreSQL 文档中的 [pg_hba.conf 文件](https://www.postgresql.org/docs/14/auth-pg-hba-conf.html)。

在 Apache Cloudberry 中，Coordinator 实例的 `pg_hba.conf` 文件控制客户端对 Cloudberry 系统的访问和认证。Segment 也有各自的 `pg_hba.conf` 文件，但这些文件已经正确配置为仅允许来自 Coordinator 主机的客户端连接。Segment 从不接受外部客户端连接，因此无需修改 Segment 上的 `pg_hba.conf` 文件。

`pg_hba.conf` 文件的基本格式是一组记录，每行一条。空行以及 \# 注释字符之后的文本都会被忽略。每条记录由多个字段组成，字段之间用空格和/或制表符分隔。如果字段值用引号括起，字段中可以包含空白字符。记录不能跨行续写。

记录可以采用以下七种格式之一：

```shell
local      <database>  <user>  <auth-method>  [<auth-options>]
host       <database>  <user>  <address>  <auth-method>  [<auth-options>]
hostssl    <database>  <user>  <address>  <auth-method>  [<auth-options>]
hostnossl  <database>  <user>  <address>  <auth-method>  [<auth-options>]
host       <database>  <user>  <IP-address>  <IP-mask>  <auth-method>  [<auth-options>]
hostssl    <database>  <user>  <IP-address>  <IP-mask>  <auth-method>  [<auth-options>]
hostnossl  <database>  <user>  <IP-address>  <IP-mask>  <auth-method>  [<auth-options>]
```

`pg_hba.conf` 各字段的含义如下：

**`local`**

匹配使用 UNIX 域套接字的连接尝试。如果没有此类记录，就不允许 UNIX 域套接字连接。

**`host`**

匹配使用 TCP/IP 的连接尝试。只有在启动服务器时为服务器配置参数 `listen_addresses` 设置了适当的值，才能建立远程 TCP/IP 连接。Apache Cloudberry 默认允许来自所有主机（`'*'`）的连接。

**`hostssl`**

匹配使用 TCP/IP 的连接尝试，但仅限使用 SSL 加密的连接。必须在服务器启动时将 `ssl` 配置参数设为 on，以启用 SSL。需要在 `postgresql.conf` 中配置 SSL 认证。请参阅[在 postgresql.conf 中配置 SSL 认证](#configure-postgresqlconf-for-ssl-authentication)。

**`hostnossl`**

匹配通过 TCP/IP 建立但不使用 SSL 的连接尝试。

**`database`**

指定此记录匹配的数据库名。值 `all` 表示匹配所有数据库。可以提供多个数据库名，以逗号分隔。在文件名前加上 `@`，可以指定一个包含数据库名的独立文件。

**`user`**

指定此记录匹配的数据库角色名。值 `all` 表示匹配所有角色。如果指定的角色是一个组，而且希望包含该组的所有成员，请在角色名前加上 `+`。可以提供多个角色名，以逗号分隔。在文件名前加上 `@`，可以指定一个包含角色名的独立文件。

**`address`**

指定此记录匹配的客户端机器地址。此字段可以包含主机名、IP 地址范围，或下文介绍的特殊关键字之一。

指定 IP 地址范围时，先用标准数字表示法写出该范围的起始地址，再加上斜杠（`/`）和 CIDR 掩码长度。掩码长度表示客户端 IP 地址中必须匹配的高位位数。给定 IP 地址中这些位右侧的位应为零。IP 地址、`/` 和 CIDR 掩码长度之间不得有任何空白字符。

按此方式指定 IPv4 地址范围的典型示例包括：`172.20.143.89/32` 表示单台主机，`172.20.143.0/24` 表示小型网络，`10.6.0.0/16` 表示较大的网络。IPv6 地址范围可以写成 `::1/128`，表示单台主机（这里为 IPv6 回环地址），也可以写成 `fe80::7a31:c1ff:0000:0000/96`，表示小型网络。`0.0.0.0/0` 表示所有 IPv4 地址，`::0/0` 表示所有 IPv6 地址。要指定单台主机，IPv4 使用掩码长度 32，IPv6 使用 128。不要省略网络地址末尾的零。

IPv4 格式的条目只匹配 IPv4 连接，IPv6 格式的条目只匹配 IPv6 连接，即使所表示的地址属于 IPv4-in-IPv6 范围也是如此。

> [!NOTE] 注意
> 如果主机系统的 C 库不支持 IPv6 地址，IPv6 格式的条目将被拒绝。

还可以使用 `all` 匹配任意 IP 地址，使用 `samehost` 匹配服务器自身的任意 IP 地址，或使用 `samenet` 匹配服务器直接连接的任意子网中的任意地址。

如果指定了主机名（不是 IP 地址、IP 地址范围或特殊关键字的地址会被视为主机名），系统会将该名称与客户端 IP 地址的反向名称解析结果进行比较（例如，使用 DNS 时进行反向 DNS 查询）。主机名比较不区分大小写。如果匹配，则对该主机名进行正向名称解析（例如正向 DNS 查询），检查解析得到的地址中是否有任何一个与客户端 IP 地址相同。只有正反两个方向都匹配，该条目才被视为匹配。

`pg_hba.conf` 中使用的主机名应当是对客户端 IP 地址进行地址到名称解析时返回的名称，否则该行不会匹配。一些主机名数据库允许将一个 IP 地址关联到多个主机名，但操作系统在解析 IP 地址时只会返回一个主机名。

以点（.）开头的主机名模式会匹配实际主机名的后缀。因此，`.example.com` 会匹配 `foo.example.com`（但不会匹配单独的 `example.com`）。

在 `pg_hba.conf` 中指定主机名时，应确保名称解析足够快。设置 `nscd` 等本地名称解析缓存可能有所帮助。另外，可以启用服务器配置参数 `log_hostname`，在日志中显示客户端主机名而不是 IP 地址。

**`IP-address`**<br />
**`IP-mask`**

这两个字段可以替代 CIDR 地址表示法。使用时，不指定掩码长度，而是在单独一列中指定实际掩码。例如，`255.0.0.0` 对应 IPv4 CIDR 掩码长度 8，`255.255.255.255` 对应 CIDR 掩码长度 32。

**`auth-method`**

指定连接匹配此记录时使用的认证方法。可用选项请参阅[认证方法](#authentication-methods)。

**`auth-options`**

在 `auth-method` 字段之后，可以有一个或多个 `name=value` 形式的字段，用于指定认证方法的选项。各认证方法有哪些可用选项，详见[认证方法](#authentication-methods)。

通过 @ 结构包含的文件会被读取为名称列表，名称之间可以用空白字符或逗号分隔。与 `pg_hba.conf` 一样，注释以 \# 开头，并且允许嵌套 @ 结构。除非 @ 后的文件名是绝对路径，否则会将其视为相对于引用文件所在目录的路径。

每次连接尝试都会按顺序检查 `pg_hba.conf` 中的记录，因此记录顺序很重要。通常，靠前的记录使用较严格的连接匹配条件和较弱的认证方法，靠后的记录使用较宽松的匹配条件和较强的认证方法。例如，可能希望对本地 TCP/IP 连接使用 `trust` 认证，而对远程 TCP/IP 连接要求密码。在这种情况下，对来自 127.0.0.1 的连接指定 `trust` 认证的记录，应放在对更大范围的客户端 IP 地址指定 `password` 认证的记录之前。

服务器启动时，以及主服务器进程收到 SIGHUP 信号时，都会读取 `pg_hba.conf` 文件。如果在运行中的系统上编辑此文件，必须使用以下命令重新加载：

```shell
$ gpstop -u
```

> [!WARNING] 警告
> 为提高系统安全性，请从 `pg_hba.conf` 文件中移除对远程连接使用 `trust` 认证的记录。`trust` 认证允许任何能够连接服务器的用户，以其指定的任意角色访问数据库。对于本地 UNIX 套接字连接，可以安全地将 `trust` 认证替换为 `ident` 认证。对于本地和远程 TCP 客户端，也可以使用 `ident` 认证，但客户端主机必须运行 ident 服务，而且必须 `trust`（信任）该机器的完整性。

## 编辑 pg_hba.conf 文件 {#edit-the-pg_hbaconf-file}

初始状态下，`pg_hba.conf` 文件为 gpadmin 用户设置了宽松的权限，而其他 Apache Cloudberry 角色没有数据库访问权。需要编辑 `pg_hba.conf` 文件，以允许用户访问数据库并保护 gpadmin 用户。请考虑移除使用 `trust` 认证的条目，因为它们允许任何能够访问服务器的人以任意角色连接。对于本地（UNIX 套接字）连接，请使用 `ident` 认证，它要求操作系统用户与指定角色匹配。对于本地和远程 TCP 连接，`ident` 认证要求客户端主机运行 indent 服务。可以在 Coordinator 主机上安装 ident 服务，然后对本地 TCP 连接（例如 `127.0.0.1/28`）使用 `ident` 认证。对远程 TCP 连接使用 `ident` 认证安全性较低，因为这要求信任客户端主机上 ident 服务的完整性。

> [!NOTE] 注意
> Cloudberry Command Center 提供了编辑 `pg_hba.conf` 文件的界面。它会在保存前验证条目，保留文件的版本历史以便重新加载旧版本，并将文件重新加载到 Apache Cloudberry 中。

以下示例展示如何编辑 Coordinator 主机上的 `pg_hba.conf` 文件，允许所有角色使用加密密码认证，从远程客户端访问所有数据库。

编辑 `pg_hba.conf` 的步骤如下：

1. 在文本编辑器中打开 `$COORDINATOR_DATA_DIRECTORY/pg_hba.conf` 文件。
2. 为每种希望允许的连接类型添加一行。记录按顺序读取，因此记录顺序很重要。通常，靠前的记录使用较严格的连接匹配条件和较弱的认证方法，靠后的记录使用较宽松的匹配条件和较强的认证方法。例如：

    ```
    # allow the gpadmin user local access to all databases
    # using ident authentication
    local   all   gpadmin   ident         sameuser
    host    all   gpadmin   127.0.0.1/32  ident
    host    all   gpadmin   ::1/128       ident
    # allow the 'dba' role access to any database from any
    # host with IP address 192.168.x.x and use md5 encrypted
    # passwords to authenticate the user
    # Note that to use SHA-256 encryption, replace md5 with
    # password in the line below
    host    all   dba   192.168.0.0/32  md5
    ```

## 认证方法 {#authentication-methods}

- [基本认证](#basic-authentication)
- [SSL 客户端认证](#ssl-client-authentication)

### 基本认证 {#basic-authentication}

**`Trust`**
无条件允许连接，无需密码或任何其他认证。`gpadmin` 角色，以及需要在节点之间连接且不能提示输入信息或密码的 Cloudberry 工具（例如 `gpinitsystem`、`gpstop`、`gpstart` 等），都需要此条目。

> [!TIP] 提示
> 为提高系统安全性，请从 `pg_hba.conf` 文件中移除对远程连接使用 `trust` 认证的记录。`trust` 认证允许任何能够连接服务器的用户，以其指定的任意角色访问数据库。对于本地 UNIX 套接字连接，可以安全地将 `trust` 认证替换为 `ident` 认证。对于本地和远程 TCP 客户端，也可以使用 `ident` 认证，但客户端主机必须运行 ident 服务，而且必须 `trust`（信任）该机器的完整性。

**`Reject`**

拒绝与指定参数匹配的连接。通常应使用此方法限制来自特定主机的访问或不安全的连接。

**`Ident`**

根据客户端的操作系统用户名进行认证。对于本地套接字连接，此方法是安全的。对来自远程主机的 TCP 连接使用 `ident`，要求客户端主机运行 ident 服务。`ident` 认证方法只能用于可信封闭网络中的远程主机。

**`md5`**

要求客户端提供经过两次 MD5 哈希运算的密码进行认证。

**`password`**

要求客户端提供未加密的密码进行认证。由于密码以明文形式在网络上传输，不应在不可信的网络上使用此方法。

基于密码的认证方法有 `md5` 和 `password`。两者的工作方式类似，区别在于通过连接发送密码的方式：前者发送 MD5 哈希值，后者发送明文。

只要对密码“嗅探”攻击有所顾虑，就应优先选择 `md5`。应尽可能避免使用明文 `password` 认证。如果连接受到 SSL 加密保护，则可以安全地使用 `password`（不过，如果依赖 SSL，SSL 证书认证可能是更好的选择）。

以下是 `pg_hba.conf` 中基本认证条目的示例：

```shell
hostnossl    all   all        0.0.0.0   reject
hostssl      all   testuser   0.0.0.0/0 md5
local        all   gpuser               ident
```

或者：

```shell
local    all           gpadmin         ident 
host     all           gpadmin         localhost      trust 
host     all           gpadmin         cdw            trust 
local    replication   gpadmin         ident 
host     replication   gpadmin         samenet       trust 
host     all           all             0.0.0.0/0     md5
```

## SSL 客户端认证 {#ssl-client-authentication}

SSL 认证会将连接客户端在 SSL 握手期间提供的 SSL 证书的 Common Name（通用名称，cn）属性，与请求使用的数据库用户名进行比较。该数据库用户应已在数据库中存在。可以使用映射文件，在系统用户名与数据库用户名之间建立映射。

### SSL 认证参数 {#ssl-authentication-parameters}

认证方法：

- **`Cert`**

    认证选项：

    **`Hostssl`**

    连接类型必须为 hostssl。

    **`map=mapping`**

    映射。

    在 `pg_ident.conf` 中指定，或在服务器设置 `ident_file` 指定的文件中指定。

    以下是 `pg_hba.conf` 中 SSL 客户端认证条目的示例：

    ```shell
    Hostssl testdb certuser 192.168.0.0/16 cert
    Hostssl testdb all 192.168.0.0/16 cert map=gpuser
    ```

### OpenSSL 配置 {#openssl-configuration}

要修改 OpenSSL 配置，可以更新 OpenSSL 安装目录下的 `openssl.cnf` 文件，或 `$OPENSSL_CONF` 引用的文件（如果存在），然后重新启动 Apache Cloudberry 服务器。

### 创建自签名证书 {#create-a-self-signed-certificate}

自签名证书可以用于测试，但在生产环境中应使用证书颁发机构（CA）签发的证书（全球 CA 或本地 CA 均可），以便客户端验证服务器身份。如果所有客户端都位于组织内部，建议使用本地 CA。

为服务器创建自签名证书的步骤如下：

1. 输入以下 `openssl` 命令：

    ```shell
    openssl req -new -text -out server.req
    ```

2. 根据提示输入所需信息。

    输入所需信息。在 Common Name 中填写本地主机名。challenge password（挑战密码）可以留空。

3. 程序会生成受口令短语保护的密钥；它不接受少于四个字符的口令短语。要移除口令短语（如果希望服务器自动启动，则必须移除），请运行以下命令：

    ```shell
    openssl rsa -in privkey.pem -out server.key
    rm privkey.pem
    ```

4. 输入旧口令短语以解锁现有密钥。然后运行以下命令：

    ```shell
    openssl req -x509 -in server.req -text -key server.key -out server.crt
    ```

    此命令会将证书转换为自签名证书，并将密钥和证书复制到服务器查找它们的位置。

5. 最后运行以下命令：

    ```shell
    chmod og-rwx server.key
    ```

有关如何创建服务器私钥和证书的更多详细信息，请参阅 OpenSSL 文档。

### 在 postgresql.conf 中配置 SSL 认证 {#configure-postgresqlconf-for-ssl-authentication}

以下服务器设置需要在 `postgresql.conf` 配置文件中指定：

- `ssl` *布尔值*。启用 SSL 连接。
- `ssl_renegotiation_limit` *整数*。指定重新协商密钥前的数据上限。
- `ssl_ciphers` *字符串*。配置允许使用的 SSL 加密套件列表。`ssl_ciphers` 会*覆盖* `/etc/openssl.cnf` 中指定的任何加密套件字符串。默认值 `ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH` 会启用除 ADH、LOW、EXP 和 MD5 加密套件之外的所有加密套件，并按强度优先排列加密套件。

  > [!NOTE] 注意
  > 对于 TLS 1.2，MEDIUM 和 HIGH 强度的某些加密套件仍使用 NULL 加密（传输过程中不加密），而默认的 `ssl_ciphers` 字符串允许这些套件。要在 TLS 1.2 中绕过 NULL 加密套件，请使用类似 `TLSv1.2:!eNULL:!aNULL` 的字符串。
  >
  > 可以使用 `NULL-SHA` 或 `NULL-MD5` 加密套件，在没有加密开销的情况下进行认证。不过，中间人可以读取并转发客户端与服务器之间的通信。此外，与认证的开销相比，加密开销很小。因此，不应使用 NULL 加密套件。

以下 SSL 服务器文件的默认位置是 Apache Cloudberry Coordinator 数据目录（`$COORDINATOR_DATA_DIRECTORY`）：

- `server.crt` - 服务器证书。
- `server.key` - 服务器私钥。
- `root.crt` - 受信任的证书颁发机构。
- `root.crl` - 被证书颁发机构吊销的证书。

如果启用了 Apache Cloudberry Coordinator 镜像和 SSL 客户端认证，*不应将* SSL 服务器文件放在默认目录 `$COORDINATOR_DATA_DIRECTORY` 中。如果执行 `gpinitstandby` 操作，`$COORDINATOR_DATA_DIRECTORY` 的内容会从 Coordinator 复制到 Standby Coordinator，而错误的 SSL 密钥和证书文件（Coordinator 的文件，而不是 Standby Coordinator 的文件）会阻止 Standby Coordinator 启动。

可以使用 `postgresql.conf` 参数 `sslcert`、`sslkey`、`sslrootcert` 和 `sslcrl`，为 SSL 服务器文件指定其他目录。

### 配置 SSL 客户端连接 {#configure-the-ssl-client-connection}

SSL 选项：

**`sslmode`**

指定保护级别。

**`require`**

仅使用 SSL 连接。如果存在根 CA 文件，则按照指定 `verify-ca` 时的方式验证证书。

**`verify-ca`**

仅使用 SSL 连接。验证服务器证书是否由受信任的 CA 签发。

**`verify-full`**

仅使用 SSL 连接。验证服务器证书是否由受信任的 CA 签发，并验证服务器主机名是否与证书中的名称匹配。

**`sslcert`**

客户端 SSL 证书的文件名。默认为 `$COORDINATOR_DATA_DIRECTORY/postgresql.crt`。

**`sslkey`**

用于客户端证书的密钥。默认为 `$COORDINATOR_DATA_DIRECTORY/postgresql.key`。

**`sslrootcert`**

包含 SSL 证书颁发机构证书的文件名。默认为 `$COORDINATOR_DATA_DIRECTORY/root.crt`。

**`sslcrl`**

SSL 证书吊销列表的名称。默认为 `$COORDINATOR_DATA_DIRECTORY/root.crl`。

可以使用以下环境变量设置客户端连接参数：

- `sslmode` – `PGSSLMODE`
- `sslcert` – `PGSSLCERT`
- `sslkey` – `PGSSLKEY`
- `sslrootcert` – `PGSSLROOTCERT`
- `sslcrl` – `PGSSLCRL`

例如，运行以下命令，从 `localhost` 连接到 `postgres` 数据库，并验证 `$COORDINATOR_DATA_DIRECTORY` 下默认位置中的证书：

```shell
psql "sslmode=verify-ca host=localhost dbname=postgres"
```

## 限制并发连接数 {#limit-concurrent-connections}

Apache Cloudberry 会按连接分配一些资源，因此建议设置允许的最大连接数。

要限制 Apache Cloudberry 系统中的活动并发会话数，可以配置服务器配置参数 `max_connections`。这是一个*本地*参数，意味着必须在 Coordinator、Standby Coordinator 以及每个 Segment 实例（主 Segment 和镜像 Segment）的 `postgresql.conf` 文件中设置该参数。Segment 上建议的 `max_connections` 值是 Coordinator 上该值的 5-10 倍。

设置 `max_connections` 时，还必须设置其依赖参数 `max_prepared_transactions`。该值必须至少等于 Coordinator 上的 `max_connections` 值，Segment 实例应设为与 Coordinator 相同的值。

例如：

- 在 `$COORDINATOR_DATA_DIRECTORY/postgresql.conf` 中（包括 Standby Coordinator）：

    ```shell
    max_connections=100
    max_prepared_transactions=100
    ```

- 在所有 Segment 实例的 `SEGMENT_DATA_DIRECTORY/postgresql.conf` 中：

    ```shell
    max_connections=500
    max_prepared_transactions=100
    ```

以下步骤使用 Apache Cloudberry 工具 `gpconfig` 设置参数值。

### 更改允许的连接数 {#change-the-number-of-allowed-connections}

1. 以 Apache Cloudberry 管理员身份登录 Apache Cloudberry Coordinator 主机，并加载 `$GPHOME/greenplum_path.sh` 文件。
2. 设置 `max_connections` 参数的值。此 `gpconfig` 命令将 Segment 上的值设为 1000，将 Coordinator 上的值设为 200。

    ```shell
    $ gpconfig -c max_connections -v 1000 -m 200
    ```

    Segment 上的值必须大于 Coordinator 上的值。Segment 上建议的 `max_connections` 值是 Coordinator 上该值的 5-10 倍。

3. 设置 `max_prepared_transactions` 参数的值。此 `gpconfig` 命令会将 Coordinator 和所有 Segment 上的值设为 200。

    ```shell
    $ gpconfig -c max_prepared_transactions -v 200
    ```

    `max_prepared_transactions` 的值必须大于或等于 Coordinator 上的 `max_connections` 值。

4. 停止并重新启动 Apache Cloudberry 系统。

    ```shell
    $ gpstop -r
    ```

5. 可以使用 `gpconfig` 的 `-s` 选项检查 Coordinator 和 Segment 上的参数值。此 `gpconfig` 命令显示 `max_connections` 参数的值。

    ```
    $ gpconfig -s max_connections
    ```

> [!NOTE] 注意
> 提高这些参数的值可能导致 Apache Cloudberry 请求更多共享内存。为减轻这一影响，可以考虑降低 `gp_cached_segworkers_threshold` 等其他与内存有关的参数。

## 加密客户端/服务器连接 {#encrypt-clientserver-connections}

启用 Apache Cloudberry 客户端连接的 SSL，可以加密客户端与数据库之间通过网络传输的数据。

Apache Cloudberry 原生支持客户端与 Coordinator 服务器之间的 SSL 连接。SSL 连接可以防止第三方窥探数据包，也能防止中间人攻击。当客户端连接经过不安全链路时，应使用 SSL；使用客户端证书认证时，则必须使用 SSL。

以 SSL 模式启用 Apache Cloudberry 需要以下条件：

- 客户端以及 Coordinator 服务器主机（Coordinator 和 Standby Coordinator）上都已安装 OpenSSL。
- 已为 Coordinator 主机和 Standby Coordinator 主机正确生成 SSL 文件 server.key（服务器私钥）和 server.crt（服务器证书）。

    - 私钥不应受口令短语保护。服务器不会提示输入私钥口令短语；如果需要口令短语，Apache Cloudberry 会因错误而启动失败。
    - 在生产系统中，Coordinator 主机和 Standby Coordinator 主机应各有一对密钥和证书，其主题 CN（Common Name）分别对应 Coordinator 主机和 Standby Coordinator 主机。

    自签名证书可用于测试，但生产环境应使用证书颁发机构（CA）签发的证书，以便客户端验证服务器身份。可以使用全球 CA 或本地 CA。如果所有客户端都位于组织内部，建议使用本地 CA。

- 确保 Apache Cloudberry 可以访问 server.key 和 server.crt，以及其他认证文件，例如 `root.crt`（受信任的证书颁发机构）。以 SSL 模式启动时，Apache Cloudberry Coordinator 会查找 server.key 和 server.crt。默认情况下，如果这些文件不在 Coordinator 数据目录（`$COORDINATOR_DATA_DIRECTORY`）中，Apache Cloudberry 不会启动。此外，如果使用 `root.crt`（受信任的证书颁发机构）等其他 SSL 认证文件，这些文件也必须位于 Coordinator 主机上。

    如果启用了 Apache Cloudberry Coordinator 镜像和 SSL 客户端认证，SSL 认证文件必须同时位于 Coordinator 主机和 Standby Coordinator 主机上，*不应将*其放在默认目录 `$COORDINATOR_DATA_DIRECTORY` 中。启用 Coordinator 镜像时，`initstandby` 操作会将 `$COORDINATOR_DATA_DIRECTORY` 的内容从 Coordinator 复制到 Standby Coordinator，而错误的 SSL 密钥和证书文件（Coordinator 的文件，而不是 Standby Coordinator 的文件）会阻止 Standby Coordinator 启动。

    可以使用 `postgresql.conf` 参数 `sslcert`、`sslkey`、`sslrootcert` 和 `sslcrl`，为 SSL 服务器文件指定其他目录。

可以在 Coordinator 和 Standby Coordinator 主机的 `postgresql.conf` 文件中，将服务器配置参数 `ssl=on` 设为启用，从而在启用 SSL 的情况下启动 Apache Cloudberry。以下 `gpconfig` 命令设置该参数：

```shell
gpconfig -c ssl -m on -v off
```

设置此参数需要重启服务器。此命令会重启系统：`gpstop -ra`。

### 创建不带口令短语、仅供测试使用的自签名证书 {#create-a-self-signed-certificate-without-a-passphrase-for-testing-only}

要为服务器创建用于测试的快速自签名证书，请使用以下 OpenSSL 命令：

```
# openssl req -new -text -out server.req
```

输入提示所要求的信息。务必将本地主机名填写为*Common Name*。challenge password（挑战密码）可以留空。

程序会生成受口令短语保护的密钥，并且不接受少于四个字符的口令短语。

要将此证书用于 Apache Cloudberry，请使用以下命令移除口令短语：

```
# openssl rsa -in privkey.pem -out server.key
# rm privkey.pem
```

出现提示时，输入旧口令短语以解锁现有密钥。

然后，输入以下命令，将证书转换为自签名证书，并将密钥和证书复制到服务器查找它们的位置。

```
# openssl req -x509 -in server.req -text -key server.key -out server.crt
```

最后，使用以下命令修改密钥权限。权限如果比以下设置更宽松，服务器将拒绝该文件。

```
# chmod og-rwx server.key
```

有关如何创建服务器私钥和证书的更多详细信息，请参阅 [OpenSSL 文档](https://www.openssl.org/docs/)。
