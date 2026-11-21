---
title: "pg_tde 2.3.0（2026-11-17）"
weight: 1
upstream_source: percona-20261121
upstream_link: https://github.com/percona/pg_tde/blob/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a/documentation/docs/release-notes/release-notes-v2.3.0.md
---

> [!NOTE] 发布日期
> 2.3.0 标签发布于 2026 年 11 月 17 日。在本次固定的源码修订中，上游文档的日期变量仍为 `TBD`。

Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

## 版本亮点 {#release-highlights}

`pg_tde` 2.3.0 新增 PostgreSQL 19 支持，并使 `pg_tde_waldump` 能够识别 `pg_tde` 自定义资源管理器。详见[变更日志](#changelog)。

## 已知问题 {#known-issues}

* ARM64 架构上的 Rocky Linux 8 默认 `mlock` 限制等于内存页大小，为 64 Kb。父进程已经达到内存上限，导致使用 `pg_tde` 的子进程无法再分配一个内存页。

    为避免这一问题，可以将 `mlock` 限制提高到至少两倍内存页大小：

    * 使用 `ulimit -l <value>` 临时修改当前会话。
    * 在 `/etc/security/limits.conf` 中设置新的硬限制，需要超级用户权限。

    请谨慎调整，因为这也会影响系统中的其他进程。

## 变更日志 {#changelog}

`pg_tde` 2.3.0 引入以下变更：

### 新功能 {#new-features}

- [PG-2536](https://perconadev.atlassian.net/browse/PG-2536)、[PG-2813](https://perconadev.atlassian.net/browse/PG-2813)：支持 PostgreSQL 19。

### 改进 {#improvements}

- [PG-2754](https://perconadev.atlassian.net/browse/PG-2754)：`pg_tde_waldump` 现在能够识别 `pg_tde` 自定义资源管理器，正确输出其记录的数据，并允许在 `--rmgr` 过滤器中指定它。
