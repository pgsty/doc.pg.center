# etcd 与 HAProxy 中文翻译规范

本文是 `content/docs/etcd/` 与 `content/docs/haproxy/` 中文译文的术语和风格基线。下述字面量保护、pgBadger 说明块例外、读者正文与验收规则也适用于 `content/docs/pgbadger/` 中文译文。译文与英文原文同目录存放，文件名采用 `<name>.zh.md`；目录页使用 `_index.zh.md`。

## 翻译范围

- 完整翻译页面标题、摘要、导航标题、正文、说明性列表、表头、表格中的说明文字和交叉引用文字。
- 产品名、协议名、命令、配置关键字、API/RPC/消息/字段名、环境变量、文件名、路径、URL、指标名、日志字段名和占位符保持原样，并用原文已有的 Markdown 代码样式标示。
- 除下述 pgBadger 与 HAProxy 已登记的说明块外，围栏与缩进代码块逐字保护，包括可复制的命令、配置、源码、协议报文、程序输出、日志、诊断、错误消息和代码注释。
- 仅对 `content/docs/pgbadger/` 中已独立复核并登记的说明类 `text` 围栏，翻译参数帮助、返回码说明、算法伪代码中的自然语言步骤、目录说明及其中的说明性示例注释。真实 CLI 签名、选项、允许值、默认值、命令、SQL、配置、正则表达式、诊断、法律原文、人名、数字和公式保持原样；此例外不允许翻译真实代码的注释。
- 每个例外围栏必须在 `data/translation-fences/pgbadger.zh/` 登记精确的源文与译文 SHA-256（`source_sha256`、`target_sha256`）、受保护字面量（`protected_literals`）及真实命令或输出行（`protected_lines`），并由独立审校者复核语义和字面量。未登记或哈希变化的围栏仍按逐字保护处理；`text` 标签本身不构成例外。
- HAProxy 围栏或缩进块中的参数说明、表格标签和自然语言解释可以翻译，但须在 `data/translation-fences/haproxy.zh/` 登记精确哈希、说明类别、复核结论及受保护字面量和命令行。真实配置、命令、源码、报文、输出、诊断和代码注释仍逐字保护；说明块混有这些内容时，只翻译解释文字。未登记或哈希变化的块不得作为例外。
- HAProxy 样本签名及旧别名声明中的返回类型标识 `integer`、`boolean`、`bool`、`string`、`binary`、`ip` 保持原样；自然语言正文中的类型说明正常翻译。
- 读者正文只写与产品使用有关的信息，不加入翻译政策、译者说明、“本页保留原文”等提示或编辑勘误过程叙述。来源归属数据与法律原文保留。
- 许可证正文不翻译。上游来源、版本、提交、别名、权重、图标、模块等元数据保持不变。
- 显式英文锚点必须逐字保留。原文没有显式锚点时，中文标题补充原英文标题对应的锚点，保证原有片段链接继续有效。
- 组件页面链接改为中文路由（如 `/zh/docs/etcd/...`）；图片、GIF、SVG、JSON 等中英文共享资产仍使用无语言前缀的原路径（如 `/docs/etcd/...`）。

## 通用风格

- 使用简体中文，面向熟悉 Linux、网络、分布式系统和数据库运维的技术读者。
- 以准确为首要目标，在不改变技术含义和约束强度的前提下使用自然、紧凑的中文句式；避免逐词硬译、冗余主语和口语化表达。
- `must` 译为“必须”或“务必”，`should` 译为“应”或“建议”，`may/can` 译为“可以”，不得削弱或加强原文语气。
- 操作步骤优先使用祈使句；客观说明使用无主句。除必要的提示语外，不使用“您”。
- `This document/guide/section` 按上下文译为“本文/本指南/本节”，不译为“本文件”；`administration skills` 译为“系统管理能力”。
- `troubleshoot X` 使用动宾语序“排查 X 故障”或“对 X 进行故障排查”，不得写成“故障排查 X”。
- 目录页只描述软件版本、功能与文档导航。删除 `English-only`、`complete English text/edition` 等与软件使用无关的语言版本自述，不另加双语、译文政策或保留原文的声明。
- 中文正文使用全角标点；中文与英文缩写、数字、行内代码之间留一个半角空格。代码和字面量内部不加空格。
- 首次出现且可能歧义的专有概念可写为“中文（English）”，后续只用中文。已有固定缩写（ACL、API、CA、CLI、DDoS、DNS、gRPC、HTTP、MVCC、QUIC、Raft、RPC、SNI、SPOE、TCP、TLS、TTL、WAL）直接保留。
- 标题中的章节编号、API 名、配置项和命令保持原样；其余标题翻译为中文。链接文字应翻译，目标地址和引用标签不得改变。
- 品牌拼写固定为 `etcd`、`etcdctl`、`HAProxy`、`PostgreSQL`、`PgBouncer`、`Prometheus`、`Grafana`、`Kubernetes` 和 `OpenSSL`。
- `etcd` 即使位于中文句首也保持小写。Raft 算法名固定写作 `Raft`。

## etcd 术语表

| 英文 | 统一译法 | 说明 |
| --- | --- | --- |
| alarm | 告警 | 指需要操作员介入的 etcd 告警 |
| authentication | 身份认证 | 与 authorization“授权”区分 |
| authorization | 授权 | |
| backend / backend database | 后端 / 后端数据库 | 不与 HAProxy 的“后端”混淆，按上下文使用 |
| backup | 备份 | |
| bootstrap | 引导 | 如“引导集群”“引导新成员” |
| client | 客户端 | |
| cluster | 集群 | |
| cluster ID / member ID | 集群 ID / 成员 ID | |
| cluster membership | 集群成员关系 | |
| compaction / compact | 压缩 / 执行压缩 | 指丢弃旧事件历史，不是数据编码压缩 |
| consensus | 共识 | |
| corruption / data corruption | 损坏 / 数据损坏 | |
| defragment / defragmentation | 整理碎片 / 碎片整理 | 与 compaction 区分 |
| discovery | 发现 | `discovery service` 译为“发现服务” |
| distributed key-value store | 分布式键值存储 | |
| election | 选举 | |
| endpoint | 端点 | |
| event | 事件 | |
| failure tolerance | 故障容忍度 | 描述数量时也可写“可容忍故障数” |
| feature gate | 功能门控 | |
| follower | 跟随者 | Raft 角色 |
| gateway | 网关 | |
| heartbeat | 心跳 | |
| keepalive / keep alive | 保活 | API 名和参数保持原样 |
| key | 键 | |
| key range | 键范围 | |
| keyspace | 键空间 | |
| key-value pair | 键值对 | |
| learner | 学习者成员 | 首次出现可注明“不投票” |
| leader | 领导者 | 不译为“主节点” |
| leadership | 领导权 | |
| lease | 租约 | |
| linearizable / linearizability | 线性一致 / 线性一致性 | |
| lock | 锁 | |
| member | 成员 | 指逻辑 etcd 服务器 |
| mixed-version cluster | 混合版本集群 | |
| modification revision | 修改修订版本 | 字段 `mod_revision` 保持原样 |
| MVCC | MVCC | 首次解释为“多版本并发控制” |
| peer | 对等成员 | `peer URL` 可译为“对等成员 URL” |
| proposal | 提案 | Raft 中需要达成共识的请求 |
| proxy | 代理 | |
| quorum | 法定人数 | 不译为“多数派”；需要强调计算时可写“多数成员（法定人数）” |
| range | 范围 | API、RPC 和类型名保持原样 |
| recovery | 恢复 | |
| revision | 修订版本 | 强调计数值时可写“修订版本号” |
| role | 角色 | |
| rolling upgrade | 滚动升级 | |
| runtime reconfiguration | 运行时重配置 | |
| serializable read | 可串行化读取 | |
| snapshot | 快照 | |
| stale read | 陈旧读取 | |
| store / storage | 存储 / 存储系统 | 依据上下文选择，不译为“商店” |
| strongly consistent | 强一致 | |
| term | 任期 | Raft 术语 |
| time to live (TTL) | 生存时间（TTL） | |
| transaction | 事务 | |
| watch | 监听 | 名词可译“监听”；命令和 API 名保持原样 |
| watcher | 监听器 | |
| write-ahead log | 预写日志 | 缩写 `WAL` 保持原样 |

## HAProxy 术语表

| 英文 | 统一译法 | 说明 |
| --- | --- | --- |
| access control list (ACL) | 访问控制列表（ACL） | 后续直接使用 ACL |
| action | 动作 | 指 HAProxy 规则动作 |
| active server | 活跃服务器 | |
| backend | 后端 | 配置关键字 `backend` 保持原样 |
| backend server | 后端服务器 | |
| backup server | 备用服务器 | |
| bandwidth limit | 带宽限制 | |
| bind | 绑定 | 配置关键字 `bind` 保持原样 |
| buffer | 缓冲区 | |
| cache | 缓存 | |
| capture | 捕获 | |
| chroot | chroot | 可写“chroot 环境” |
| client | 客户端 | |
| compression | 压缩 | |
| connection | 连接 | |
| consistency | 一致性 | |
| connection mode | 连接模式 | |
| consistent hash | 一致性哈希 | |
| content switching | 内容切换 | |
| converter | 转换器 | 特指样本转换器 |
| CPU affinity | CPU 亲和性 | |
| directive | 指令 | |
| event loop | 事件循环 | |
| file descriptor | 文件描述符 | |
| filter | 过滤器 | |
| flat | 扁平 | 如“扁平目录结构”“扁平阅读顺序” |
| formatted string | 格式化字符串 | |
| frontend | 前端 | 配置关键字 `frontend` 保持原样 |
| graceful shutdown | 优雅关闭 | |
| health check | 健康检查 | |
| header | 头 | 组合为“请求头”“响应头”“Host 头”“Vary 头”，不译为“头部” |
| HTTP header | HTTP 头 | request/response 分别译“请求头/响应头” |
| keep-alive | 持久连接 | 字面配置值和选项保持原样 |
| latency | 延迟 | |
| Layer 4 / Layer 7 | 第 4 层 / 第 7 层 | 可并列写作 L4/L7 |
| listener | 监听器 | |
| listening socket | 监听套接字 | |
| load balancer | 负载均衡器 | |
| load balancing | 负载均衡 | |
| log format | 日志格式 | |
| log forwarding | 日志转发 | |
| manual | 手册 | `Starter Guide`、`Configuration Manual`、`Management Guide` 分别译“入门指南”“配置手册”“管理指南” |
| map | 映射 | 配置对象或关键字保持 `map` |
| master-worker mode | 主进程/工作进程模式 | |
| matching method | 匹配方法 | |
| option family | 各类选项 | 不译为“选项家族” |
| pattern | 模式 | 正则语境可按需写“匹配模式” |
| pager stop | 翻页节点 | |
| peer | 对等节点 | 配置关键字 `peer` 与段名 `peers` 保持原样 |
| pinned input | 固定版本的源文件 | |
| process | 进程 | |
| PROXY protocol | PROXY 协议 | `PROXY` 必须大写 |
| proxy | 代理 | |
| proxy section | 代理段 | 配置文件中的 section 统一译“段” |
| queue | 队列 | |
| rate limit | 速率限制 | |
| redispatch | 重分派 | |
| regular expression | 正则表达式 | |
| reload | 重载 | `graceful reload` 译“平滑重载” |
| request | 请求 | |
| request rate / connection rate | 请求速率 / 连接速率 | 不译为“请求数率/连接数率” |
| response | 响应 | |
| reverse proxy | 反向代理 | |
| ring | 环形缓冲区 | 配置关键字 `ring` 保持原样 |
| round-robin | 轮询 | |
| rule | 规则 | |
| runtime API | 运行时 API | |
| runtime CLI | 运行时 CLI | |
| sample | 样本 | |
| sample fetch / sample fetching | 样本提取 | |
| sample fetch method | 样本提取方法 | |
| section | 段 | 指 HAProxy 配置段；普通文档章节仍译“章节” |
| secondary entry | 二级条目 | |
| secondary key | 二级键 | |
| server | 服务器 | |
| server close | 服务端关闭 | 指 HTTP 连接模式 |
| session | 会话 | |
| soft stop | 软停止 | |
| source address | 源地址 | |
| statistics / stats | 统计信息 | 命令、字段和配置名保持原样 |
| stick table | 粘性表 | 配置关键字 `stick-table` 保持原样 |
| stickiness | 会话粘性 | |
| stream | 流 | |
| tarpit | 连接陷阱（tarpit） | 首次出现保留英文，后续可写“连接陷阱” |
| thread | 线程 | |
| throughput | 吞吐量 | |
| timeout | 超时 | |
| TLS termination | TLS 终止 | |
| troubleshooting | 故障排查 | 不译为“故障排除” |
| typed output | 类型化输出 | |
| Unix socket | Unix 套接字 | |
| weight | 权重 | |
| zero downtime | 零停机 | |

## 一致性与验收规则

- 每个英文 Markdown 页面必须有且仅有一个同目录中文页面；非 Markdown 数据和图片不复制。
- 中英文页面的 `upstream_link`、显式锚点、代码围栏数量及类型、短代码、图片目标、引用定义、内部链接目标和 HTML 标签必须保持结构一致。
- 代码块默认逐字一致；pgBadger 说明类 `text` 围栏仅接受上述已独立复核的精确哈希与字面量登记，真实代码及注释继续逐字保护。读者正文不得出现翻译政策、译者说明或编辑过程叙述。
- 中文页面不得残留未说明的英文正文。允许保留的英文仅限本规范列出的字面量、专名、代码、程序输出、日志、错误消息与上游法律文本。
- 对 must/should/may、否定词、数值、单位、版本号、默认值、弃用状态、安全警告和操作顺序执行专项核对。
- 完成源文件校验后必须执行 Hugo 生产构建，并检查中英文路由、片段链接、导航顺序和窄屏页面可读性。
