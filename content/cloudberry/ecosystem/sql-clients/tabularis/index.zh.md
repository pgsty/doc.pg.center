---
title: "Tabularis"
description: "通过 PostgreSQL 驱动将 Tabularis 桌面 SQL 工作区连接到 Apache Cloudberry。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/ecosystem/sql-clients/tabularis.md"
---

[Tabularis](https://tabularis.dev) 是一款适用于 Windows、macOS 和 Linux 的开源桌面 SQL 工作区，提供模式浏览器、SQL 编辑器、可视化 `EXPLAIN`、实体关系图和 SQL 笔记本。它使用内置的 PostgreSQL 驱动，通过 PostgreSQL 网络协议连接 Apache Cloudberry，方式与连接 PostgreSQL 本身相同。

## 前提条件 {#prerequisites}

- Apache Cloudberry 已部署，且已在 `pg_hba.conf` 中正确设置数据库访问权限。
- 已安装 [Tabularis](https://github.com/TabularisDB/tabularis/releases) v0.24.0 或更高版本。可通过 WinGet、Homebrew、Snap、Flatpak 和 AUR 获取软件包。
- 已准备好 Coordinator 主机、端口、数据库名称及用于连接的角色。

## 操作步骤 {#steps}

1. 启动 Tabularis，在连接管理器中点击 **Add Connection（添加连接）**。

2. 在 **Database type（数据库类型）** 中选择 **PostgreSQL**。Cloudberry 没有独立的连接类型：它使用 PostgreSQL 网络协议，因此应选择 PostgreSQL 驱动。

3. 为连接命名，然后填写 Coordinator 主机和端口、用户名、密码及数据库名称。也可以将 `postgresql://gpadmin:password@coordinator-host:5432/postgres` 这样的连接字符串粘贴到 **Connection string（连接字符串）** 字段中，一次填入这些信息。

4. 点击 **Test Connection（测试连接）** 进行验证，再点击 **Save（保存）**。

5. 从连接管理器中打开连接。左侧的模式浏览器列出模式、表、视图和例程；右侧的编辑器用于运行查询，并在数据网格中显示结果。

![Tabularis 连接和查询界面](tabularis1.png)

现在可以浏览模式、直接编辑表格中的行，并在编辑器中运行查询，包括连接查询和聚合查询。
