---
title: Visual Studio Code 快速入门
description: 安装 VS Code 扩展，通过 Docker 或 Linux 软件包连接 DocumentDB，并插入和读取你的第一个文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 40
translation_source_sha256: 979095c44b08fbdd3740a59e1c598648d055b1a8cf54667be1f8b5e1c22c6a42
translation_review: AI-assisted bilingual review; 2026-11-07
---

使用 Visual Studio Code 的 DocumentDB 扩展，可以直接在编辑器中配置本地 DocumentDB 实例、浏览示例数据，并创建第一个数据库。

扩展可以自动创建实例：拉取官方镜像，创建容器和持久化数据卷，生成凭据，等待数据库能够接受连接，然后保存连接。它不会安装 Docker。

已经运行 DocumentDB 时，可跳过实例创建步骤，直接[连接现有实例](#connect-an-existing-instance)。

## 前提条件 {#prerequisites}

- [Visual Studio Code](https://code.visualstudio.com/)
- [Visual Studio Code 的 DocumentDB 扩展](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb)
- Docker Desktop 或 Docker Engine，设置为 Linux 容器，并在 VS Code 所在环境运行
- 可选：[mongosh](https://www.mongodb.com/docs/mongodb-shell/install/) 用于独立连接测试

Docker 必须能从 VS Code 所在的运行环境中访问。如果使用 WSL、开发容器、SSH 远程环境或 Codespaces，Docker 也必须在那个环境中可用，仅在宿主机上安装还不够。配置流程会检查环境是否就绪，无法连接 Docker 时会说明需要修复的问题。

## 安装扩展 {#install-the-extension}

从 VS Code 市场安装扩展，或运行：

```bash
code --install-extension ms-azuretools.vscode-documentdb
```

若要更新旧版本安装，请添加 `--force`；不添加此参数，命令将保留你当前的版本。安装或更新后，请重新加载 VS Code，因为运行中的窗口会继续使用旧版本，直到重新加载为止。

<span id="set-up-document-db-local"></span>

## 配置 DocumentDB Local {#set-up-documentdb-local}

通过引导式配置，让扩展创建 DocumentDB Local 并保存连接，无需手动执行 Docker 命令。

1. 通过以下任一方式打开配置流程：
   - 在活动栏中选择 DocumentDB 图标，在 Connections（连接）视图中展开 **Your own DocumentDB**（自己的 DocumentDB），选择 **Set up DocumentDB Local**（配置 DocumentDB Local）。
   - 从命令面板运行 **DocumentDB: Set up DocumentDB Local**（配置 DocumentDB Local）。
   - 在浏览器中打开 `vscode://ms-azuretools.vscode-documentdb/local`，并确认相关提示。这要求扩展版本为 0.10.1 或更新版本，所以请先安装或更新扩展；该链接并不总能自动安装扩展。
2. 在 **Introduction**（介绍）步骤中选择 **Continue**（继续）。进入下一步之前不会下载或创建任何内容。
3. 在 **Configure**（配置）步骤中检查默认值，再选择 **Start DocumentDB Local**（启动 DocumentDB Local）。默认设置会选择可用端口（从 `10260` 开始）、生成凭据、使用官方 `latest` 镜像，并提供可选的示例数据。展开高级选项后，可以自行指定端口、镜像标签或凭据。
4. 等待配置完成。扩展会创建名为 `vscode-documentdb-local` 的容器及持久化卷，然后等待数据库能够接受连接。
5. 选择 **Open Connection**（打开连接）显示保存的连接，再展开它浏览数据库和集合。

示例数据默认启用。若保持启用，展开已保存的连接以浏览示例数据库和集合。

右键单击 DocumentDB Local 条目，可以选择 **Start**（启动）、**Stop**（停止）、**Restart**（重启）、**Delete Container**（删除容器），以及 **Copy Connection String**（复制连接字符串）、**Copy Password**（复制密码）或 **View Logs**（查看日志）。停止再启动会保留数据；删除操作则会永久移除数据卷和生成的凭据。

## 可选：自行启动容器 {#alternative-start-the-container-yourself}

如果你希望自行管理容器，请使用此方法。如果 DocumentDB 已在运行，请跳过此步骤，[连接你的现有实例](#connect-an-existing-instance)。

使用 Docker 启动容器：

```bash
docker run -dt --pull always --name documentdb \
  -p 127.0.0.1:10260:10260 \
  -e USERNAME='<YOUR_USERNAME>' \
  -e PASSWORD='<YOUR_PASSWORD>' \
  ghcr.io/documentdb/documentdb/documentdb-local:latest
```

> [!NOTE]
> DocumentDB Local 镜像默认发送使用情况遥测数据。若要关闭，请在镜像名称前添加 `-e DOCUMENTDB_USAGE_TELEMETRY=false`。参见[使用情况遥测](/documentdb/documentdb-local/#usage-telemetry)和[隐私声明](https://github.com/documentdb/documentdb/blob/v1.0-0/documentdb-local/PRIVACY.md)。

若要直接安装到主机，而不使用 Docker，请在当前版本支持的发行版上按 [Linux 软件包快速入门](/documentdb/getting-started/packages/)操作。

## 连接现有实例 {#connect-an-existing-instance}

已有运行中的 DocumentDB 实例时，使用此方式。只需添加连接，无需运行配置向导，也无需再创建容器。请准备好实例的端口、用户名和密码。

1. 在 VS Code 活动栏中打开 **DocumentDB** 视图。
2. 在本地连接区域选择 **DocumentDB Local**，启动 **New Local Connection**（新建本地连接）流程。
3. 输入实例的端口（上述命令使用 `10260`）、用户名和密码。
4. 出现 TLS/SSL 提示时：
   - **仅限本地开发**：若使用默认自签名本地配置，且尚未配置证书信任，选择 **Disable TLS/SSL (Not recommended)**（禁用 TLS/SSL，不推荐）。
   - 若已配置受信任的本地证书，保留 **Enable TLS/SSL (Default)**（启用 TLS/SSL，默认）。
5. 完成向导，确认新连接已出现在连接树中。

## 在扩展中验证连接 {#verify-the-connection-in-the-extension}

引导式设置默认加载示例数据，除非你关闭此选项。上述手动 Docker 命令启动时不包含示例数据；[Docker 快速入门](/documentdb/getting-started/docker/) 说明了如何启用它。

1. 展开已保存的连接。若已加载示例数据，请打开示例数据库和集合以浏览文档。
2. 从上下文菜单创建你自己的数据库和集合。若未启用示例数据，空实例为预期状态。
3. 在你自己的集合中，添加一个测试文档，例如：

```json
{
  "name": "VS Code Quick Start",
  "source": "vscode",
  "status": "connected"
}
```

在 **Table**（表格）、**Tree**（树形）和 **JSON** 视图之间切换，确认扩展能读取文档。

如果你更倾向于先在扩展外部验证，请使用 [Mongo Shell 快速入门](/documentdb/getting-started/mongo-shell-quickstart/)。

## 导入、导出与查询 {#import-export-and-querying}

连接成功后，扩展可帮助你在不离开 VS Code 的情况下继续操作：

- 将 JSON 文档导入集合
- 导出查询结果或完整集合
- 以分页方式在多种视图中浏览文档
- 打开查询编辑器，继续使用 [API 参考](/documentdb/reference/) 中的命令

## 故障排除与调试 {#troubleshooting-and-debugging}

如果首次尝试设置或连接失败：

- 如果浏览器链接没有反应，确认已安装 VS Code，并允许浏览器打开它。如果 VS Code 已打开但配置流程没有启动，请安装或更新扩展，重新加载 VS Code，再次打开链接；也可以改为从命令面板运行 **DocumentDB: Set up DocumentDB Local**（配置 DocumentDB Local）
- 如果 VS Code 提示 **a DocumentDB deep-link was opened without a connection string**（打开了 DocumentDB 深层链接，但未提供连接字符串），说明扩展早于 0.10.1。运行 `code --install-extension ms-azuretools.vscode-documentdb --force`，重新加载 VS Code，再次打开链接
- 如果 VS Code 提示 **No extension gallery service configured**（未配置扩展市场服务），或缺少扩展时没有任何反应，说明该链接无法自动安装扩展。这常见于使用私有扩展市场的受管设备。请通过 `code --install-extension ms-azuretools.vscode-documentdb` 自行安装扩展，再次打开链接
- 如果配置流程提示无法连接 Docker，请修复提示的问题（Docker 未运行，或使用了 Windows 容器而非 Linux 容器），然后选择 **Continue setup**（继续配置）；此时尚未创建任何内容
- 如果没有出现 DocumentDB 视图，请确认已安装扩展，并重新加载 VS Code
- 连接前确认本地 DocumentDB 实例确实正在运行
- 使用 Docker 时，检查 `docker ps` 和 `docker logs documentdb`
- 使用 Linux 软件包时，检查 `sudo documentdb-setup --status`；若网关由手动构建，确认其进程正在监听所输入的端口
- 如果本地连接向导在安全设置环节失败，请重试，并选择与证书配置相符的 TLS/SSL 选项
- 使用 `mongosh` 单独验证端点是否正常，排除 VS Code 的影响

扩展特定帮助或问题：

- [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb)
- [GitHub 仓库](https://github.com/microsoft/vscode-documentdb)
- [GitHub 讨论](https://github.com/microsoft/vscode-documentdb/discussions)
- [GitHub 问题](https://github.com/microsoft/vscode-documentdb/issues)
- [DocumentDB Discord](https://discord.gg/vH7bYu524D)

## 下一步 {#next-steps}

- [Visual Studio Code 的 DocumentDB 扩展文档](https://github.com/microsoft/vscode-documentdb/tree/main/docs)
- [Docker 快速入门](/documentdb/getting-started/docker/)
- [Linux 软件包快速入门](/documentdb/getting-started/packages/)
- [Mongo Shell 快速入门](/documentdb/getting-started/mongo-shell-quickstart/)
- [Node.js 快速入门](/documentdb/getting-started/nodejs-setup/)
- [Python 快速入门](/documentdb/getting-started/python-setup/)
- [API 参考](/documentdb/reference/)
