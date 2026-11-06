---
title: "配置系统资源限制"
description: "Apache Cloudberry 等数据库系统需要设置特定的系统资源限制，才能高效运行。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/system-settings.md"
---

应为运行数据库进程的 `gpadmin` 用户配置这些限制。

1. 创建资源限制配置。

    创建用户资源限制配置文件：

    ```bash
    sudo tee /etc/security/limits.d/90-db-limits.conf << 'EOF'
    # Core dump file size limits for gpadmin
    gpadmin soft core unlimited
    gpadmin hard core unlimited
    # Open file limits for gpadmin
    gpadmin soft nofile 524288
    gpadmin hard nofile 524288
    # Process limits for gpadmin
    gpadmin soft nproc 131072
    gpadmin hard nproc 131072
    EOF
    ```

2. 了解各项限制。

    该配置设置了以下几类资源限制：

    - **核心转储**（`core`）：

        - 设为 `unlimited`，以允许生成完整的核心转储。
        - 对调试和故障排查至关重要。
        - 软限制和硬限制均不设上限。

    - **打开文件数**（`nofile`）：

        - 设为 `524288`（512K）个文件。
        - 处理大量并发数据库连接需要这一设置。
        - 对分布式操作和大型工作负载至关重要。

    - **进程数限制**（`nproc`）：

        - 设为 `131072`（128K）个进程。
        - 支持并行执行查询。
        - 支持 Cloudberry 的分布式架构。

3. 验证资源限制。

    ```bash
    # Check current limits
    sudo -u gpadmin bash -c "ulimit -a"
    ```
