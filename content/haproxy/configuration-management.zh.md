---
title: "10. 简化配置管理"
linkTitle: "10. 配置管理"
weight: 340
description: "让大型 HAProxy 配置更易维护的方法"
icon: fa-solid fa-screwdriver-wrench
module: [HAPROXY]
categories: [任务]
aliases:
  - /haproxy/management/configuration-management/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 10"
---

组成集群的两个 HAProxy 节点通常使用完全相同的配置，只有少数地址不同。与其为每个节点分别维护一份最终必然产生差异的重复配置，不如在配置中引用环境变量。这样，多个配置实例便可共用同一个文件，只需在系统级环境变量中保留少量差异。此功能始于 1.5 版，当时只有地址可以包含环境变量；1.6 版进一步支持在所有位置使用环境变量。其语法与 UNIX shell 相同：变量以美元符号（'\$'）开头，后接左花括号（'{'）、变量名和右花括号（'}'）。除地址外，环境变量只在双引号包围的参数中解析；这是为了避免破坏使用含美元符号正则表达式的现有配置。

环境变量也便于编写可在多个站点使用、仅地址不同的通用配置，还可以把密码从部分配置文件中移出。以下示例中的 "site1.env" 文件会在启动时由 init 脚本加载：

```shell
$ cat site1.env
LISTEN=192.168.1.1
CACHE_PFX=192.168.11
SERVER_PFX=192.168.22
LOGGER=192.168.33.1
STATSLP=admin:pa$$w0rd
ABUSERS=/etc/haproxy/abuse.lst
TIMEOUT=10s

$ cat haproxy.cfg
global
    log "${LOGGER}:514" local0

defaults
    mode http
    timeout client "${TIMEOUT}"
    timeout server "${TIMEOUT}"
    timeout connect 5s

frontend public
    bind "${LISTEN}:80"
    http-request reject if { src -f "${ABUSERS}" }
    stats uri /stats
    stats auth "${STATSLP}"
    use_backend cache if { path_end .jpg .css .ico }
    default_backend server

backend cache
    server cache1 "${CACHE_PFX}.1:18080" check
    server cache2 "${CACHE_PFX}.2:18080" check

backend server
    server cache1 "${SERVER_PFX}.1:8080" check
    server cache2 "${SERVER_PFX}.2:8080" check
```
