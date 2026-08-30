---
title: 基于角色的访问控制
weight: 4100
description: 一个基于角色的基本身份认证和访问控制指南
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/authentication/rbac.md"
---

## 概述 {#overview}

身份认证功能自 etcd 2.1 版本起引入。etcd v3 API 对身份认证功能的 API 和用户界面进行了轻微调整，以更好地适配新的数据模型。本文旨在帮助用户在 etcd v3 中设置基本的身份认证和基于角色的访问控制。

## 特殊用户和角色 {#special-users-and-roles}

有一个特殊用户 `root`，以及一个特殊角色 `root`。

### 用户 `root` {#user-root}

`root` 用户在激活身份认证前必须先创建，该用户拥有对 etcd 的完全访问权限。`root` 用户的设计初衷是用于系统管理：管理角色和普通用户。`root` 用户必须拥有 `root` 角色，并被允许修改 etcd 内的任意内容。

### 角色 `root` {#role-root}

角色 `root` 可授予任意用户，包括根用户。拥有 `root` 角色的用户具备全局读写权限，并可更新集群的身份认证配置。此外，`root` 角色授予用户执行常规集群维护的权限，包括修改集群成员关系、整理碎片以及创建快照。

## 使用用户 {#working-with-users}

`user` 子命令用于 `etcdctl`，负责处理与用户账户相关的所有事项。

用户列表可通过以下方式获取：

```
$ etcdctl user list
```

创建用户的方法如下：

```
$ etcdctl user add myusername
```

创建新用户时将提示输入新密码。当提供选项 `--interactive=false` 时，可从标准输入提供密码。也可使用 `--new-user-password` 来提供密码。

创建无法通过密码认证的用户也是可行的，方法如下：

```
$ etcdctl user add myusername --no-password
```

此类用户只能通过 TLS 通用名称 [进行认证](#using-tls-common-name)。

> [!NOTE]
> etcd 不支持通过 `--user username:` 使用空密码进行身份认证。例如，使用空密码创建的用户，如 `etcdctl user add anonymous:''`，无法通过用户名/密码请求进行身份认证，类似 `etcdctl --user anonymous: get foo` 的请求将失败并返回 `user name is empty`。

用户的角色可使用以下方式授予或撤销：

```
$ etcdctl user grant-role myusername foo
$ etcdctl user revoke-role myusername bar
```

用户设置可通过以下方式检查：

```
$ etcdctl user get myusername
```

用户密码可通过以下方式更改：

```
$ etcdctl user passwd myusername
```

更改密码后，将再次提示输入新密码。当提供选项 `--interactive=false` 时，密码可从标准输入提供。

使用以下命令删除账户：
```
$ etcdctl user delete myusername
```


## 使用角色 {#working-with-roles}

`role` 子命令用于 `etcdctl`，负责处理与特定角色访问控制相关的所有事项，这些权限已授予个别用户。

列出角色：

```
$ etcdctl role list
```

创建新角色，使用：

```
$ etcdctl role add myrolename
```

角色无密码；它仅用于定义一组新的访问权限。

角色被授予对单个键或键范围的访问权限。

范围可指定为区间 [起始键、结束键)，其中起始键在字典序上应小于结束键。

访问权限可授予为读取、写入或两者兼有，例如以下示例所示：

```
# Give read access to a key /foo
$ etcdctl role grant-permission myrolename read /foo

# Give read access to keys with a prefix /foo/. The prefix is equal to the range [/foo/, /foo0)
$ etcdctl role grant-permission myrolename --prefix=true read /foo/

# Give write-only access to the key at /foo/bar
$ etcdctl role grant-permission myrolename write /foo/bar

# Give full access to keys in a range of [key1, key5)
$ etcdctl role grant-permission myrolename readwrite key1 key5

# Give full access to keys with a prefix /pub/
$ etcdctl role grant-permission myrolename --prefix=true readwrite /pub/
```

要查看已授予的权限，可随时查看角色：

```
$ etcdctl role get myrolename
```

权限撤销以相同逻辑方式进行：

```
$ etcdctl role revoke-permission myrolename /foo/bar
```

如移除角色本身：

```
$ etcdctl role delete myrolename
```

## 启用身份认证 {#enabling-authentication}

启用身份认证的最小步骤如下。系统管理员可根据偏好，在启用身份认证之前或之后设置用户和角色。

确保已创建 root 用户：

```
$ etcdctl user add root
Password of root:
```

启用身份认证：

```
$ etcdctl auth enable
```

此后，etcd 已启用身份认证运行。如需出于任何原因禁用身份认证，请使用对应的反向命令：

```
$ etcdctl --user root:rootpw auth disable
```

## 身份认证的安全范围 {#security-scope-of-authentication}

当启用身份认证 `etcdctl auth enable` 时，可保护 V3 gRPC API 操作（get、put、delete、watch 等）。

`/metrics` 和 `/health` HTTP 端点使用独立的处理器，**不**受 V3 RBAC 身份认证保护。此设计允许 Prometheus 和负载均衡器在无需 gRPC 身份认证的情况下抓取指标，同时仍可保护键值数据。

为保障可观测性端点的安全：

- 使用 `--cert-file`、`--key-file` 和 `--client-cert-auth` 启用 mTLS
- 或通过 `--listen-metrics-urls` 将指标绑定到私有接口
- 或使用网络策略/防火墙规则限制访问

## 使用 `etcdctl` 进行身份认证 {#using-etcdctl-to-authenticate}

`etcdctl` 支持与 `curl` 类似的身份认证标志。

```
$ etcdctl --user user:password get foo
```

密码可从提示中获取：

```
$ etcdctl --user user get foo
```

密码也可以从命令行标志 `--password` 获取：

```
$ etcdctl --user user --password password get foo
```


否则，所有 `etcdctl` 命令保持不变。用户和角色仍可创建和修改，但需由具备根角色的用户进行身份认证。

## 使用 TLS 共用名称 {#using-tls-common-name}
从 v3.2 版本起，若 etcd 服务器以选项 `--client-cert-auth=true` 启动，则客户端 TLS 证书中的通用名称（CN）字段将用作 etcd 用户。在此情况下，通用名称用于身份认证，客户端无需提供密码。请注意，若同时满足以下两个条件：1. `--client-cert-auth=true` 被传递且客户端提供了通用名称，以及 2. 客户端提供了用户名和密码，则基于用户名和密码的身份认证将被优先使用。请注意，此功能无法与 gRPC-proxy 或 gRPC-gateway 一同使用。这是因为 gRPC-proxy 会终止来自其客户端的 TLS 连接，导致所有客户端共享代理的证书。gRPC-gateway 内部使用 TLS 连接将 HTTP 请求转换为 gRPC 请求，因此存在相同的限制。因此，客户端无法正确向服务器提供其通用名称。若给定证书的通用名称非空，gRPC-proxy 将报错并停止运行。gRPC-proxy 返回错误，提示客户端证书中包含非空的通用名称。

## 密码强度说明 {#notes-on-password-strength}
`etcdctl` 和 etcd API 在用户创建或更新用户密码操作期间不强制要求特定密码长度。系统管理能力应负责实施此类要求。为避免与密码强度相关的安全风险，可使用 [TLS Common Name 基于的身份认证](#using-tls-common-name)，或通过 `--no-password` 选项创建的用户。
