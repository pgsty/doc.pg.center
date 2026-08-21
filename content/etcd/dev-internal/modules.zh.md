---
title: Go 模块
weight: 1650
description: etcd 项目的 Go 模块组织
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/dev-internal/modules.md"
---

etcd 项目（自版本 3.5 起）采用多个 [golang 模块](https://golang.org/ref/mod)，托管于 [单个仓库](https://golang.org/ref/mod#vcs-dir) 中。

![模块图](/etcd/dev-internal/img/modules.svg)

以下是各个模块：

  - **go.etcd.io/etcd/api/v3** - 包含 API 定义
  （如 protos 与 proto 生成的库），定义了 etcd 客户端与服务器之间的通信协议。

  - **go.etcd.io/etcd/pkg/v3** - etcd 使用的通用工具包集合，不针对 etcd 本身。仅当某个包未来可能被移出至独立仓库时，才应归入此处。请避免在此处添加依赖关系复杂的代码，因为这些依赖会自动成为客户端库的依赖（我们希望客户端库保持轻量）。

  - **go.etcd.io/etcd/client/v3** - 通过网络（gRPC）与 etcd 通信所使用的客户端库。建议所有新的 etcd 使用场景均采用此库。

  - **go.etcd.io/etcd/client/v2** - 用于通过 HTTP 协议与 etcd 通信的旧版客户端库。已弃用。所有新用法应依赖 /v3 库。

  - **go.etcd.io/etcd/raft/v3** - 分布式共识协议的实现。不应包含与 etcd 相关的特定代码。

  - **go.etcd.io/etcd/server/v3** - etcd 实现。
  该包中的代码为 etcd 内部实现，外部项目不应使用。包的结构和 API 可能在小版本内发生变更。

  - **go.etcd.io/etcd/etcdctl/v3** - 用于访问和管理 etcd 的命令行工具。

  - **go.etcd.io/etcd/tests/v3** - 包含 etcd 所有集成测试的模块。
    请注意：所有单元测试（快速且不依赖跨模块依赖）应保留在被测试代码所在的本地模块中。

  - **go.etcd.io/bbolt** - 持久化 b 树的实现。
    托管于独立的仓库中：https://github.com/etcd-io/bbolt.


### 运维 {#operations}

1. 所有 etcd 模块应以相同版本发布，例如：`go.etcd.io/etcd/client/v3@v3.5.10` 必须依赖 `go.etcd.io/etcd/api/v3@v3.5.10`。

   版本的持续更新可通过以下方式执行：
   ```shell script
   % DRY_RUN=false TARGET_VERSION="v3.5.10" ./scripts/release_mod.sh update_versions
   ```
2. 发布的模块应根据 https://golang.org/ref/mod#vcs-version 规则进行标记，即每个模块应拥有独立的标签。可通过以下方式执行标记：
   ```shell script
   % DRY_RUN=false REMOTE_REPO="origin" ./scripts/release_mod.sh push_mod_tags
   ```

3. 所有 etcd 模块应依赖相同版本的底层依赖项。
   可通过以下方式验证：
   ```shell script
   % PASSES="dep" ./test.sh
   ```

4. go.mod 文件中不得包含未使用的依赖项，且必须符合 `go mod tidy` 格式要求。
   验证方式如下：
   ```
   % PASSES="mod_tidy" ./test.sh
   ```

5. 若要在所有模块中触发操作（例如自动格式化所有文件），请使用或扩展以下脚本：
   ```shell script
   % ./scripts/fix.sh
   ```

### 未来 {#future}

作为指引方向的北极星，我们希望基于以下模型评估 etcd 模块：

![模块图](/etcd/dev-internal/img/modules-future.svg)

本文假设：
  - 将 etcdmigrate/etcdadm 从 etcdctl 二进制文件中分离。
    由此 etcdctl 将明确成为网络客户端 API 的命令行封装，
    而 etcdmigrate/etcdadm 则支持对 etcd 存储文件的直接物理操作。
  - 将 etcd-proxy 从 ./etcd 二进制文件中分离，因其包含更多实验性代码，
    故带来额外风险与依赖。
  - 废弃对 v2 协议的支持。
