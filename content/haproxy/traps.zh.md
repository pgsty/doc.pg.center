---
title: "11. 应避免的常见陷阱"
linkTitle: "11. 常见陷阱"
weight: 350
description: "应避免的运维失误与反直觉行为"
icon: fa-solid fa-triangle-exclamation
module: [HAPROXY]
categories: [任务]
aliases:
  - /haproxy/management/traps/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 11"
---

有时会有人报告：系统重启后 HAProxy 服务没有启动，但手动启动又能正常工作。这通常出现在使用 keepalived 等集群 IP 地址机制、只把服务 IP 分配给主节点的环境中。HAProxy 绑定 0.0.0.0 时一切正常，改为绑定虚拟 IP 后却无法启动。原因是服务启动时，本地节点尚未持有该虚拟 IP；HAProxy 尝试绑定时，系统会因其不是本地 IP 地址而拒绝操作。正确的解决办法不是推迟 HAProxy 服务启动——这无法应对服务重启——而是把系统配置为允许绑定非本地地址。在 Linux 上，将 net.ipv4.ip_nonlocal_bind sysctl 设为 1 即可。如果需要透明截获经 HAProxy 转发到特定目标地址的 IP 流量，也必须启用此设置。

多进程配置若使用源端口范围，表面上可能运行正常，却会在高负载下随机失败：多个进程可能同时尝试使用同一源端口连接同一服务器，而这是不允许的。系统会报告错误并使用其他端口重试。增大 "retries" 参数可以在一定程度上掩盖问题，但也会增加 CPU 开销和处理时间，日志中仍会出现一定数量的重试记录。因此，多进程配置应避免使用端口范围。

HAProxy 使用 SO_REUSEPORT，并允许多个独立进程绑定同一个 IP:port。故障排查时，可能出现旧进程尚未停止、新进程便已启动的情况。这会产生荒谬的测试结果，看起来仿佛配置变更完全没有生效。实际上，即使新进程已经使用新配置重启，旧进程仍会接收并处理部分传入连接，从而返回意外结果。如有疑问，只需停止新进程后再次测试；如果服务仍然可用，很可能是旧进程依然存活，必须将其停止。Linux 的 "netstat -lntp" 命令在此很有帮助。

通过命令行向 ACL 添加条目时（例如将某个源地址加入黑名单），务必注意：这些条目不会同步写入文件，一旦有人重载配置，更新便会丢失。对于黑名单场景，这往往正是期望的效果；但如果该变更本是针对某个问题的修复，就可能不符合预期。详见 CLI 接口的 "add acl" 动作。
