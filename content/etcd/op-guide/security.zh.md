---
title: 传输安全模型
weight: 4125
description: 确保数据传输安全
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/security.md"
---

etcd 支持自动 TLS，以及通过客户端证书实现的客户端到服务器和对等成员（服务器到服务器 / 集群）通信的身份认证。请注意，etcd 默认不启用 [基于 RBAC 的身份认证][auth] 或传输层的身份认证功能，以降低用户入门时的使用门槛。此外，更改此默认设置将对该项目造成破坏性变更，该项目自 2013 年确立以来一直保持该设定。未启用安全功能的 etcd 集群可能使数据暴露于任意客户端。

要快速上手，请先准备一个 CA 证书以及一个成员的已签名密钥对。建议为集群中的每个成员创建并签署新的密钥对。

为方便起见，[cfssl] 工具提供了便捷的证书生成接口，我们在此提供一个使用该工具的示例 [here][tls-setup]。或者，可参考此 [指南以生成自签名密钥对][tls-guide]。

以下提供的标志列表可能因持续开发变更而未能保持最新。如需获取最新可用的标志，请运行 `etcd --help` 或查阅 [etcd help][]。

## 基本配置 {#basic-setup}

etcd 支持多个与证书相关的配置选项，可通过命令行标志或环境变量进行设置：

**客户端到服务器通信:**

`--cert-file=<path>`：用于与 etcd 建立 SSL/TLS 连接的证书。设置此选项后，advertise-client-urls 可使用 HTTPS 方案。

`--key-file=<path>`：证书的键。必须为未加密的。

`--client-cert-auth`：启用此选项后，etcd 将检查所有传入的 HTTPS 请求，确保其包含由受信任 CA 签发的客户端证书；未提供有效客户端证书的请求将失败。若 [身份认证][auth] 已启用，证书中的通用名称（Common Name）字段将提供用户的用户名凭证。

`--trusted-ca-file=<path>`：受信任的证书颁发机构。

`--auto-tls`：对与客户端的 TLS 连接使用自动生成的自签名证书。

**对等通信（服务器间/集群）:**

对等成员选项的工作方式与客户端到服务器选项相同：

`--peer-cert-file=<path>`：用于对等成员之间 SSL/TLS 连接的证书。该证书将同时用于在对等成员地址上监听以及向其他对等成员发送请求。

`--peer-key-file=<path>`：证书的键。必须为未加密的。

`--peer-client-cert-auth`：启用后，etcd 将检查来自集群的所有对等成员请求，确保其客户端证书由指定的 CA 签发。

`--peer-trusted-ca-file=<path>`：受信任的证书颁发机构。

`--peer-auto-tls`：对等成员之间的 TLS 连接使用自动生成的自签名证书。

若提供客户端到服务器证书或对等成员证书，则必须同时设置密钥。所有这些配置选项也可通过环境变量 `ETCD_CA_FILE`、`ETCD_PEER_CA_FILE` 等进行设置。

**常用选项:**

`--cipher-suites`：服务器/客户端与对等成员之间支持的 TLS 密码套件列表，以逗号分隔（空值将由 Go 自动填充）。

`--tls-min-version=<version>` 设置 etcd 支持的最低 TLS 版本。

`--tls-max-version=<version>` 设置 etcd 支持的最大 TLS 版本。若未设置，则使用 Go 支持的最大版本。

### TLS 证书 keyUsage 和 extendedKeyUsage {#tls-certificate-keyusage-and-extendedkeyusage}

在为 etcd 传输层安全生成 X.509 证书时，证书应根据其角色包含适当的 `keyUsage` 和 `extendedKeyUsage` 字段。etcd 依赖 Go 的 `crypto/tls` 和 `crypto/x509` 库进行证书验证，这些库会在 TLS 握手过程中强制执行这些用途。

下表总结了常见证书角色的推荐用法：

| 证书角色 | keyUsage | extendedKeyUsage |
| ---------------- | -------- | ---------------- |
| 服务器（客户端到服务器） | digitalSignature, keyEncipherment | serverAuth |
| 客户端 | digitalSignature, keyEncipherment | clientAuth |
| 对等成员（服务器到服务器） | digitalSignature, keyEncipherment | serverAuth, clientAuth |

注意事项：

- 当启用 `--peer-client-cert-auth` 时，对等成员之间使用证书进行双向 TLS，因此必须同时配置 `serverAuth` 和 `clientAuth`。
- 与 `--client-cert-auth` 一起使用的客户端证书应包含 `clientAuth`。

## 示例 1: 使用 HTTPS 的客户端到服务器传输安全 {#example-1-client-to-server-transport-security-with-https}

为此，请准备好 CA 证书（`ca.crt`）以及已签名的密钥对（`server.crt`、`server.key`）。

请逐步配置 etcd 以提供简单的 HTTPS 传输安全：

```sh
$ etcd --name infra0 --data-dir infra0 \
  --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls=https://127.0.0.1:2379 --listen-client-urls=https://127.0.0.1:2379
```

这应能正常启动，可通过向 etcd 发送 HTTPS 请求来测试配置：

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

该命令应显示握手成功。由于我们使用自签名证书并采用自有的证书颁发机构，因此必须通过 `--cacert` 选项将 CA 传递给 curl。另一种方法是将 CA 证书添加至系统的受信任证书目录（通常位于 `/etc/pki/tls/certs` 或 `/etc/ssl/certs`）。

**OSX 10.9+ 用户**：OSX 10.9+ 上的 curl 7.30.0 不支持在命令行中传递证书。

请将 dummy ca.crt 直接导入钥匙串，或向 curl 添加 `-k` 标志以忽略错误。

若要不使用 `-k` 标志进行测试，请运行 `open ./tests/fixtures/ca/ca.crt` 并按照提示操作。

测试完成后请删除该证书！

如有可行的变通方法，请告知我们。

## 示例 2：使用 HTTPS 客户端证书进行客户端到服务器的身份认证 {#example-2-client-to-server-authentication-with-https-client-certificates}

目前，etcd 客户端已具备验证服务器身份并提供传输安全的能力。然而，我们还可以使用客户端证书来防止未经授权的访问。

客户端将向服务器提供其证书，服务器将检查该证书是否由提供的 CA 签发，并据此决定是否响应请求。

与第一个示例中提到的文件相同，本例也需要一个由同一证书颁发机构签名的客户端密钥对（`client.crt`、`client.key`）。

```sh
$ etcd --name infra0 --data-dir infra0 \
  --client-cert-auth --trusted-ca-file=/path/to/ca.crt --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls https://127.0.0.1:2379 --listen-client-urls https://127.0.0.1:2379
```

现在以相同请求尝试此服务器：

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

请求应被服务器拒绝：

```
...
routines:SSL3_READ_BYTES:sslv3 alert bad certificate
...
```

为使操作成功，需将由 CA 签署的客户端证书提供给服务器：

```sh
$ curl --cacert /path/to/ca.crt --cert /path/to/client.crt --key /path/to/client.key \
  -L https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

输出应包含：

```
...
SSLv3, TLS handshake, CERT verify (15):
...
TLS handshake, Finished (20)
```

同时，服务器的响应如下：

```json
{
    "action": "set",
    "node": {
        "createdIndex": 12,
        "key": "/foo",
        "modifiedIndex": 12,
        "value": "bar"
    }
}
```

指定要阻止的加密套件 [弱 TLS 加密套件](https://github.com/etcd-io/etcd/issues/8320)。

当客户端使用无效的加密套件请求 Client Hello 时，TLS 握手将失败。

例如：

```bash
$ etcd \
  --cert-file ./server.crt \
  --key-file ./server.key \
  --trusted-ca-file ./ca.crt \
  --cipher-suites TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

然后，客户端请求必须指定服务器中指定的加密套件之一：

```bash
# valid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-AES128-GCM-SHA256

# request succeeds
etcd_server_version{server_version="3.2.22"} 1
...
```

```bash
# invalid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-DES-CBC3-SHA

# request fails with
(35) error:14094410:SSL routines:ssl3_read_bytes:sslv3 alert handshake failure
```

## 示例 3：集群中的传输安全与客户端证书 {#example-3-transport-security--client-certificates-in-a-cluster}

etcd 支持与上述相同的模型用于 **对等成员通信**，即集群中 etcd 成员之间的通信。

假设我们已拥有 `ca.crt`，以及两个分别使用该 CA 签署其密钥对的成员（`member1.crt` 与 `member1.key`，`member2.crt` 与 `member2.key`），则按如下方式启动 etcd：


```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member1.crt --peer-key-file=/path/to/member1.key \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member2.crt --peer-key-file=/path/to/member2.key \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

etcd 成员将组成一个集群，集群内成员之间的所有通信均将使用客户端证书进行加密和身份认证。etcd 的输出将显示其连接的地址使用 HTTPS。

## 示例 4：自动生成的自签名传输安全 {#example-4-automatic-self-signed-transport-security}

> [!WARNING]
> 指定 ClientAutoTLS 和 PeerAutoTLS 时，etcd 自动生成的客户端证书和对等成员证书的有效期仅为 1 年。可以指定 --self-signed-cert-validity 标志来设置证书的有效期（以年为单位）。

当仅需通信加密而无需身份认证时，etcd 支持使用自动生成的自签名证书对消息进行加密。此举简化了部署流程，无需在 etcd 外部管理证书和密钥。

通过标志 `--auto-tls` 和 `--peer-auto-tls` 配置 etcd，使其对客户端和对等成员连接使用自签名证书：

```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

自签名证书无法验证身份，因此 curl 会返回错误：

```sh
curl: (60) SSL certificate problem: Invalid certificate chain
```

要禁用证书链检查，请使用 `-k` 标志调用 curl：

```sh
$ curl -k https://127.0.0.1:2379/v2/keys/foo -Xput -d value=bar -v
```

## DNS SRV 服务记录说明 {#notes-for-dns-srv}

自 v3.1.0 版本起（v3.2.9 除外），发现 SRV 引导通过 `ServerName` 的根域名来认证 `--discovery-srv` 标志指定的域名。此举旨在防止中间人证书攻击，要求证书的 Subject Alternative Name（SAN）字段中必须包含与根域名匹配的条目。例如，`etcd --discovery-srv=etcd.local` 仅在提供的证书中包含根域名 `etcd.local` 作为 SAN 字段条目时，才会认证对等成员/客户端。

## etcd 代理使用说明 {#notes-for-etcd-proxy}

etcd 代理在连接安全时终止来自客户端的 TLS，并使用在 `--peer-key-file` 和 `--peer-cert-file` 中指定的代理自身密钥/证书与 etcd 成员通信。

代理通过给定成员的 `--advertise-client-urls` 和 `--advertise-peer-urls` 与 etcd 成员通信。它将客户端请求转发至 etcd 成员的已通告客户端 URL，同时通过 etcd 成员的已通告对等成员 URL 同步初始集群配置。

当为 etcd 成员启用客户端身份认证时，系统管理员必须确保代理的 `--peer-cert-file` 选项中指定的对等成员证书适用于该身份认证。如果启用了对等成员身份认证，则代理的对等成员证书也必须适用于对等成员身份认证。

## TLS 身份认证注意事项 {#notes-for-tls-authentication}

自 [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09) 起，客户端每次连接时都会重新加载 [TLS 证书](https://github.com/etcd-io/etcd/pull/7829)。此机制在无需停止 etcd 服务器的情况下替换过期证书时非常有用；可通过用新证书覆盖旧证书来实现。每次连接时刷新证书的开销不应过大，但未来可通过引入缓存层进一步优化。示例测试可参见 [这里](https://github.com/etcd-io/etcd/blob/b041ce5d514a4b4aaeefbffb008f0c7570a18986/integration/v3_grpc_test.go#L1601-L1757)。

自 [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09) 起，[服务器拒绝包含错误 IP 地址的对等成员证书 `SAN`](https://github.com/etcd-io/etcd/pull/7687)。例如，若对等成员证书的 Subject Alternative Name (SAN) 字段中包含任何 IP 地址，服务器仅在远程 IP 地址与其中任一 IP 地址匹配时才认证该对等成员。此举旨在防止未经授权的端点加入集群。例如，对等成员 B 的 CSR（含 `cfssl`）为：

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local",
    "10.138.0.27"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "L": "CA",
      "ST": "San Francisco"
    }
  ]
}
```

当对等成员 B 的实际 IP 地址为 `10.138.0.2` 时，而非 `10.138.0.27`。当对等成员 B 尝试加入集群时，对等成员 A 将以错误 `x509: certificate is valid for 10.138.0.27, not 10.138.0.2` 拒绝 B 的加入请求，因为 B 的远程 IP 地址与 Subject Alternative Name (SAN) 字段中的地址不匹配。

自 [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09) 起，[服务器在检查 `SAN`](https://github.com/etcd-io/etcd/pull/7767) 时会解析 TLS `DNSNames`。例如，若对等成员证书的 Subject Alternative Name（SAN）字段中仅包含 DNS 名称（无 IP 地址），则服务器仅在对这些 DNS 名称执行正向查找（`dig b.com`）并确认其解析出的 IP 地址与远程 IP 地址匹配时，才完成对等成员的身份认证。例如，对等成员 B 的 CSR（含 `cfssl`）为：

```json
{
  "CN": "etcd peer",
  "hosts": [
    "b.com"
  ],
```

当对等成员 B 的远程 IP 地址为 `10.138.0.2` 时。当对等成员 B 尝试加入集群时，对等成员 A 会查找入站主机 `b.com` 以获取 IP 地址列表（例如 `dig b.com`）。如果该列表不包含 IP `10.138.0.2`，则拒绝 B 的加入请求，并返回错误 `tls: 10.138.0.2 does not match any of DNSNames ["b.com"]`。

自 [v3.2.2](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v322-2017-07-07) 起，[服务器在 IP 地址匹配时接受连接，不再检查 DNS 条目](https://github.com/etcd-io/etcd/pull/8223)。例如，若对等成员证书中的 Subject Alternative Name (SAN) 字段包含 IP 地址和 DNS 名称，且远程 IP 地址与其中任一 IP 地址匹配，服务器将直接接受连接，不再进一步验证 DNS 名称。例如，对等成员 B 的 CSR（含 `cfssl`）为：

```json
{
  "CN": "etcd peer",
  "hosts": [
    "invalid.domain",
    "10.138.0.2"
  ],
```

当对等成员 B 的远程 IP 地址为 `10.138.0.2` 且 `invalid.domain` 为无效主机时，对等成员 B 尝试加入集群，对等成员 A 可成功对 B 进行身份认证，因为主题备用名称（SAN）字段包含有效的匹配 IP 地址。详情请参见 [issue#8206](https://github.com/etcd-io/etcd/issues/8206)。

自 [v3.2.5](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v325-2017-08-04) 起，[服务器支持对通配符 DNS 的反向查找 `SAN`](https://github.com/etcd-io/etcd/pull/8281)。例如，若对等成员证书中的 Subject Alternative Name（SAN）字段仅包含 DNS 名称（无 IP 地址），服务器首先对远程 IP 地址执行反向查找，以获取映射到该地址的一组名称（例如 `nslookup IPADDR`）。若这些名称中存在与对等成员证书中 DNS 名称匹配的名称（通过精确匹配或通配符匹配），则接受连接。若无匹配项，服务器将对证书中的每个 DNS 条目执行正向查找（例如，当条目为 `*.example.default.svc` 时，查找 `example.default.svc`），仅当主机解析出的地址中包含与对等成员远程 IP 地址匹配的 IP 地址时，才接受连接。例如，对等成员 B 的 CSR（含 `cfssl`）为：

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local"
  ],
```

当对等成员 B 的远程 IP 地址为 `10.138.0.2` 时。对等成员 B 尝试加入集群，对等成员 A 会反向查找 IP `10.138.0.2` 以获取主机名列表，并将主机名与对等成员 B 证书中 Subject Alternative Name (SAN) 字段的 DNS 名称进行精确匹配或通配符匹配。若反向或正向查找均失败，将返回错误 `"tls: "10.138.0.2" does not match any of DNSNames ["*.example.default.svc","*.example.default.svc.cluster.local"]`。详情请参见 [issue#8268](https://github.com/etcd-io/etcd/issues/8268)。

[v3.3.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) 引入 [`etcd --peer-cert-allowed-cn`](https://github.com/etcd-io/etcd/pull/8616) 标志，以支持对等成员间连接的 [基于 CN（通用名称）的身份认证](https://github.com/etcd-io/etcd/issues/8262)。Kubernetes TLS 引导机制涉及为 etcd 成员及其他系统组件（例如 API 服务器、kubelet 等）生成动态证书。为每个组件维护不同的 CA 可提供对 etcd 集群更严格的访问控制，但通常较为繁琐。当指定 --peer-cert-allowed-cn 标志时，节点仅能以匹配的通用名称加入集群，即使使用共享 CA 亦然。匹配方式为与证书的通用名称（CN）字段进行精确字符串比较——不支持通配符或前缀匹配。对于基于主机名的过滤，使用 --peer-cert-allowed-hostname 或 --client-cert-allowed-hostname 时，匹配采用 Go 的 x509.Certificate.VerifyHostname() 函数，支持精确主机名及通配符条目（例如 *.example.com）。例如，三节点集群中每个成员使用 CSRs（通过 cfssl）配置如下：




```json
{
  "CN": "etcd.local",
  "hosts": [
    "m1.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m2.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m3.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

若提供了 `--peer-cert-allowed-cn etcd.local`，则仅对等成员中 Common Name 匹配的才会被认证。若证书签名请求（CSR）中的 CN 不同，或 `--peer-cert-allowed-cn` 不同，则节点将被拒绝：

```bash
$ etcd --peer-cert-allowed-cn m1.etcd.local

I | embed: rejected connection from "127.0.0.1:48044" (error "CommonName authentication failed", ServerName "m1.etcd.local")
I | embed: rejected connection from "127.0.0.1:55702" (error "remote error: tls: bad certificate", ServerName "m3.etcd.local")
```

每个进程应以以下方式启动：

```bash
etcd --peer-cert-allowed-cn etcd.local

I | pkg/netutil: resolving m3.etcd.local:32380 to 127.0.0.1:32380
I | pkg/netutil: resolving m2.etcd.local:22380 to 127.0.0.1:22380
I | pkg/netutil: resolving m1.etcd.local:2380 to 127.0.0.1:2380
I | etcdserver: published {Name:m3 ClientURLs:[https://m3.etcd.local:32379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m1 ClientURLs:[https://m1.etcd.local:2379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m2 ClientURLs:[https://m2.etcd.local:22379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | embed: serving client requests on 127.0.0.1:32379
I | embed: serving client requests on 127.0.0.1:22379
I | embed: serving client requests on 127.0.0.1:2379
```

[v3.2.19](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md) 和 [v3.3.4](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) 修复了当 [证书 SAN 字段仅包含 IP 地址而无域名](https://github.com/etcd-io/etcd/issues/9541) 时的 TLS 重载问题。例如，成员使用如下 CSRs（含 `cfssl`）进行配置：

```json
{
  "CN": "etcd.local",
  "hosts": [
    "127.0.0.1"
  ],
```

在 Go 中，仅当服务器的 `(*tls.Config).Certificates` 字段非空，或客户端提供了有效 SNI 且 `(*tls.ClientHelloInfo).ServerName` 非空时，服务器才会调用 `(*tls.Config).GetCertificate` 以重新加载 TLS。此前，etcd 始终在初始客户端 TLS 握手时填充 `(*tls.Config).Certificates`（非空）。因此，客户端始终需提供匹配的 SNI，以通过 TLS 验证并触发 `(*tls.Config).GetCertificate` 重新加载 TLS 资产。

不过，如果证书的 SAN 字段 [不包含任何域名而只有 IP 地址](https://github.com/etcd-io/etcd/issues/9541)，请求中的 `*tls.ClientHelloInfo` 会带有空的 `ServerName` 字段，导致初始 TLS 握手无法触发 TLS 重载；需要在线替换过期证书时，这就会成为问题。

现在，`(*tls.Config).Certificates` 在初始 TLS 客户端握手时被创建为空，首先用于触发 `(*tls.Config).GetCertificate`，然后在每次新的 TLS 连接时填充其余证书，即使客户端 SNI 为空（例如，证书仅包含 IP 地址）。

## 主机白名单说明 {#notes-for-host-whitelist}

`etcd --host-whitelist` 标志指定可接受的 HTTP 客户端请求主机名。客户端来源策略可防范针对不安全 etcd 服务器的 [“DNS 重绑定”](https://en.wikipedia.org/wiki/DNS_rebinding) 攻击。即，任何网站均可创建一个合法的 DNS 名称，并将 DNS 指向 `"localhost"`（或其他任意地址）。随后，监听在 `"localhost"` 上的 etcd 服务器所有 HTTP 端点均可能被访问，从而面临 DNS 重绑定攻击。详情请参见 [CVE-2018-5702](https://bugs.chromium.org/p/project-zero/issues/detail?id=1447#c2)。

客户端来源策略的工作方式如下：

1. 若客户端通过 HTTPS 安全连接，则允许任意主机名。
2. 若客户端连接不安全且 `"HostWhitelist"` 非空，则仅允许 Host 字段在白名单中的 HTTP 请求。

请注意，无论是否启用身份认证，客户端来源策略均会被强制执行，以实现更严格的控制。

默认情况下，`etcd --host-whitelist` 和 `embed.Config.HostWhitelist` 被设置为 *空*，以允许所有主机名。请注意，指定主机名时，环回地址不会自动添加。如需允许环回接口，应手动将其添加至白名单（例如 `"localhost"`、`"127.0.0.1"` 等）。

## 常见问题解答 {#frequently-asked-questions}

### 我在使用 TLS 客户端身份认证时遇到 SSLv3 握手失败错误？ {#im-seeing-a-sslv3-alert-handshake-failure-when-using-tls-client-authentication}

`crypto/tls` 包中的 `golang` 在使用证书公钥前会检查其键用途。
要使用证书公钥进行客户端认证，创建证书公钥时需在 `clientAuth` 中添加 `Extended Key Usage`。

操作方法如下：

在 OpenSSL.cnf 中添加以下章节：

```
[ ssl_client ]
...
  extendedKeyUsage = clientAuth
...
```

生成证书时，请确保在 `-extensions` 标志中引用该证书：

```
$ openssl ca -config openssl.cnf -policy policy_anything -extensions ssl_client -out certs/machine.crt -infiles machine.csr
```

### 使用对等证书身份认证时，我收到“证书有效域名是 127.0.0.1，不是$MY_IP” {#with-peer-certificate-authentication-i-receive-certificate-is-valid-for-127001-not-my_ip}
请确保使用成员的公网 IP 地址作为证书的主体名称（Subject Name）进行签名。例如，`etcd-ca` 工具为 `new-cert` 命令提供了 `--ip=` 选项。

证书需在成员的完全限定域名（FQDN）作为其主题名称（Subject Name）时进行签名，使用主题备用名称（IP SANs）添加 IP 地址。`etcd-ca` 工具为 `new-cert` 命令提供 `--domain=` 选项，OpenSSL 也可实现 [it][alt-name]。

### etcd 是否对磁盘上存储的数据进行加密？ {#does-etcd-encrypt-data-stored-on-disk-drives}
etcd 不会对存储在磁盘驱动器上的键值数据进行加密。若用户需要对存储在 etcd 中的数据进行加密，可选择以下方案：
* 由客户端应用程序负责对数据进行加密和解密
* 使用底层存储系统的加密功能，例如 [dm-crypt]

### 我看到一条日志警告，内容是“目录 X 存在但没有推荐的权限 -rwx------” {#im-seeing-a-log-warning-that-directory-x-exist-without-recommended-permission--rwx}
当 etcd 创建某些新目录时，会将文件权限设置为 700，以尽可能防止非特权访问。然而，如果用户已使用自定义偏好创建了目录，etcd 将使用现有目录，并在权限与 700 不同时记录警告消息。

[alt-name]: http://wiki.cacert.org/FAQ/subjectAltName
[auth]: /zh/etcd/op-guide/authentication/
[cfssl]: https://github.com/cloudflare/cfssl
[dm-crypt]: https://en.wikipedia.org/wiki/Dm-crypt
[tls-guide]: https://github.com/coreos/docs/blob/master/os/generate-self-signed-certificates.md
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
[etcd help]: https://github.com/etcd-io/etcd/blob/main/server/etcdmain/help.go
