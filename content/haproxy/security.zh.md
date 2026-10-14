---
title: "13. 安全注意事项"
linkTitle: "13. 安全"
weight: 370
description: "特权隔离、攻击面、Linux 能力及安全运行"
icon: fa-solid fa-shield-halved
module: [HAPROXY]
categories: [任务]
aliases:
  - /haproxy/management/security/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 13"
---

HAProxy 旨在以极低的权限运行。使用它的标准方式是将其隔离到 chroot 环境中，并将其权限降级为非 root 用户，且该用户在该环境内没有任何权限，从而确保未来若发现任何漏洞，其被攻破也不会影响系统其余部分。

为执行 chroot 操作，进程首先需要以 root 用户身份启动。手动构建 chroot 环境并在其中启动进程毫无意义，这类 chroot 环境难以构建，从不会得到妥善维护，且包含的缺陷总是远多于主文件系统。一旦发生入侵，攻击者还可以利用这个特意构建的文件系统。不幸的是，许多系统管理员混淆了“以 root 身份启动”与“以 root 身份运行”的区别，导致在启动 HAProxy 之前就更改了用户 ID，从而削弱了实际的安全限制。

HAProxy 需要以 root 身份启动，才能实现以下目的：

- 调整文件描述符限制
- 绑定到特权端口号
- 绑定到特定网络接口
- 透明地监听外部地址
- 将自身隔离在 chroot 环境中
- 降权至另一个非特权 UID

HAProxy 可能需要以 root 身份运行，以实现以下目的：

- 绑定到接口以发起出站连接
- 绑定到特权源端口以发起出站连接
- 透明地绑定到外部地址以发起出站连接

大多数用户永远不需要“以 root 身份运行”的情形。但“以 root 身份启动”涵盖了大多数使用场景。

安全的配置应满足以下要求：

- 一个指向空位置且无任何访问权限的 chroot 语句。可通过 UNIX 命令行按如下方式准备：

```shell
# mkdir /var/empty && chmod 0 /var/empty || echo "Failed"
```

并在 HAProxy 配置的 global 段中以如下方式引用：

```text
chroot /var/empty
```

- 在 global 段中同时使用 uid/user 和 gid/group 语句：

```text
user haproxy
group haproxy
```

- 设置统计信息套接字的模式、所有者用户 ID 和所有者组 ID，使其与允许访问 CLI 的用户和/或组匹配，以防止未经授权的用户访问：

```text
stats socket /var/run/haproxy.stat uid hatop gid hatop mode 600
```

## 13.1. Linux 能力支持 {#section-13-1}

自 v2.9 版本起，HAProxy 支持 Linux 能力。若二进制文件编译时 USE_LINUX_CAP=1，则在从 root 用户切换至非 root 用户时，能够保留通过 'setcap' 关键字赋予的能力。

自 v3.1 版本起，HAProxy 还会通过 capget 系统调用检查 'setcap' 关键字指定的能力是否已由管理员设置在其二进制文件的 Permitted set（允许集）中。若是，则在以非 root 用户运行时，会通过 capset 系统调用将这些能力转移到进程的 Effective set（有效集）。

此举旨在避免 HAProxy 以 root 用户启动并运行时可能出现的所有使用场景：透明代理模式、绑定到特权端口。

'setcap' 关键字支持以下网络能力：

- cap_net_admin：透明代理、将套接字绑定到特定网络接口、使用 set-mark 动作；
- cap_net_raw（cap_net_admin 的子集）：透明代理；
- cap_net_bind_service：将套接字绑定到特权端口；
- cap_sys_admin：在特定网络命名空间中创建套接字。

如果这些能力未列为 'setcap' 参数，HAProxy 绝不会将它们从 Permitted set（允许集）转移到 Effective set（有效集）。有关 'setcap' 关键字及所支持能力的更多信息，请参见配置指南第 3.1 节“进程管理与安全”。

系统管理员可通过以下命令向 HAProxy 二进制文件的 Permitted set（允许集）添加所需能力：

示例：

```haproxy
# setcap cap_net_admin,cap_net_bind_service=p /usr/local/sbin/haproxy
```

添加的能力将在进程启动后出现在其 Permitted set 中。如果相同的能力也是 'setcap' 关键字的参数，则它们还会出现在进程的 Effective set 中。可通过以下命令检查：

示例：

```haproxy
# grep Cap /proc/<haproxy PID>/status
```

    CapInh: 0000000000000000
    CapPrm: 0000000000001400
    CapEff: 0000000000001400
    CapBnd: 000001ffffffffff
    CapAmb: 0000000000000000

有关 setcap 和能力集的更多详细信息，请参阅 Linux 手册页（capabilities(7)）。

在某些使用场景中，例如透明代理或在特定网络命名空间中创建套接字时，配置文件解析器会检测到需要 cap_net_raw 或 cap_sys_admin 或其他受支持的能力。随后，在初始化阶段，HAProxy 进程会检查这些能力能否放入其 Effective set。若因 capget 或 capset 系统调用失败（某些安全模块如 SELinux、Seccomp 等对系统调用施加了限制）而无法完成，进程将发出诊断警告（使用 -dD 启动）。

由于需要支持多种不同平台及其各异的系统设置，解析器无法从配置文件中推断出是否会绑定到特权端口。因此，在权限不足（以非 root 用户运行）的情况下，进程将仅以如下告警信息终止。用户需自行复查其配置以及 HAProxy 二进制文件的能力集。

示例：

```shell
$ haproxy -dD -f haproxy.cfg
...
[ALERT]    (96797): Binding [haproxy.cfg:36] for frontend fe: cannot bind socket (Permission denied) for [0.0.0.0:80]
[ALERT]    (96797): [haproxy.main()] Some protocols failed to start their listeners! Exiting.
```
