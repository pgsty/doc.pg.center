---
title: 库和工具
weight: 1300
description: etcd 工具和客户端库列表
icon: fa-solid fa-puzzle-piece
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/integrations.md"
---

请注意，以下第三方库和工具未托管在 https://github.com/etcd-io 下，也未经 etcd 团队测试或维护。使用前应自行阅读相关资料并评估其可靠性。

## 工具 {#tools}

- [etcdctl](https://github.com/etcd-io/etcd/tree/main/etcdctl) - etcd 的命令行客户端
- [etcd-dump](https://npmjs.org/package/etcd-dump) - 用于导出/恢复 etcd 的命令行工具
- [etcd-fs](https://github.com/xetorthio/etcd-fs) - etcd 的 FUSE 文件系统
- [etcddir](https://github.com/rekby/etcddir) - 实时同步 etcd 与本地目录的工具，支持 Windows 和 Linux
- [etcd-browser](https://github.com/henszey/etcd-browser) - 基于 AngularJS 的 Web 端键值编辑器，用于 etcd
- [etcd-lock](https://github.com/datawisesystems/etcd-lock) - 基于 etcd 实现的领导者选举与分布式读写锁，支持 v2 版本
- [etcd-console](https://github.com/matishsiao/etcd-console) - 基于 PHP 的 Web 端键值编辑器，用于 etcd
- [etcd-viewer](https://github.com/nikfoundas/etcd-viewer) - 使用 Java 编写的 etcd 键值存储编辑器/查看器
- [etcdtool](https://github.com/mickep76/etcdtool) - 将 etcd 目录导出/导入/编辑为 JSON/YAML/TOML 格式，并使用 JSON Schema 验证目录
- [etcdloadtest](https://github.com/sinsharat/etcdloadtest) - 用于 etcd 3.0 及以上版本的命令行负载测试客户端
- [etcd-tui](https://github.com/olamilekan000/etcd-tui) - 用于与 etcd 数据库交互的现代终端用户界面（TUI），可在终端中导航键、查看值、过滤数据，并直接管理 etcd 集群
- [etcdfinder](https://etcdfinder.github.io) - 一款快速、现代的 Web UI，支持 etcd v2 和 v3，具备即时搜索功能
- [lucas](https://github.com/ringtail/lucas) - 用于 Kubernetes etcd 3.0+ 集群的 Web 端键值查看器
- [etcd-manager](https://etcdmanager.io) - 一款现代、高效、跨平台且免费的 etcd 3.x 图形界面与客户端工具，支持 Windows、Linux 和 Mac
- [etcd-backup-restore](https://github.com/gardener/etcd-backup-restore) - 用于定期且增量备份与恢复 etcd 的工具
- [etcd-druid](https://github.com/gardener/etcd-druid) - 用于部署 etcd 集群并管理日常运维操作的 Kubernetes Operator
- [etcdadm](https://github.com/kubernetes-sigs/etcdadm) - 用于操作 etcd 集群的命令行工具
- [etcd-defrag](https://github.com/ahrtr/etcd-defrag) - 更易用且智能的 etcd 碎片整理工具
- [etcdhelper](https://github.com/tsonglew/intellij-etcdhelper) - 适用于 IntelliJ 平台的 etcd 插件

## 库 {#libraries}

以下各节按语言列出了 etcd 客户端库。

### Golang {#go}

- [etcd/client/v3](https://github.com/etcd-io/etcd/tree/main/client/v3) - v3 版本的官方维护 Go 客户端
- [go-etcd](https://github.com/coreos/go-etcd) - 已弃用的官方客户端。对较旧版本（<2.0.0）的 etcd 可能仍有用处。
- [encWrapper](https://github.com/lumjjb/etcd/tree/enc_wrapper/clientwrap/encwrapper) - encWrapper 是 etcd 客户端 Keys API/KV 的加密封装。

### Java {#java}

- [coreos/jetcd](https://github.com/etcd-io/jetcd) - 支持 v3
- [justinsb/jetcd](https://github.com/justinsb/jetcd)
- [cdancy/etcd-rest](https://github.com/cdancy/etcd-rest) - 使用 jclouds 提供 v2 API 的完整实现。
- [IBM/etcd-java](https://github.com/IBM/etcd-java)

### Scala {#scala}

- [maciej/etcd-client](https://github.com/maciej/etcd-client) - 支持 v2。基于 Akka HTTP 的完全异步客户端
- [eiipii/etcdhttpclient](https://bitbucket.org/eiipii/etcdhttpclient) - 支持 v2。基于 Netty 和 Scala Futures 的异步 HTTP 客户端
- [mingchuno/etcd4s](https://github.com/mingchuno/etcd4s) - 支持 v3，使用 gRPC，可选支持 Akka Stream

### Perl {#perl}

- [hexfusion/perl-net-etcd](https://github.com/hexfusion/perl-net-etcd) - 支持 v3 gRPC 网关 HTTP API
- [robn/p5-etcd](https://github.com/robn/p5-etcd) - 支持 v2

### Python {#python}

- [kragniz/python-etcd3](https://github.com/kragniz/python-etcd3) - v3 版本客户端
- [jplana/python-etcd](https://github.com/jplana/python-etcd) - 支持 v2 版本
- [russellhaering/txetcd](https://github.com/russellhaering/txetcd) - 基于 Twisted 的 Python 库
- [cholcombe973/autodock](https://github.com/cholcombe973/autodock) - Docker 部署自动化工具
- [lisael/aioetcd](https://github.com/lisael/aioetcd) - (Python 3.4+) Asyncio 协程客户端（支持 v2）
- [txaio-etcd](https://github.com/crossbario/txaio-etcd) - 面向 Twisted（当前）和 asyncio（未来）的异步 etcd v3 专用客户端库
- [dims/etcd3-gateway](https://github.com/dims/etcd3-gateway) - 使用 HTTP gRPC 网关的 etcd v3 API 库
- [aioetcd3](https://github.com/gaopeiliang/aioetcd3) - (Python 3.6+) asyncio 专用的 etcd v3 API
- [Revolution1/etcd3-py](https://github.com/Revolution1/etcd3-py) - (Python 2.7 和 Python 3.5+) 使用 gRPC-JSON-Gateway 的 etcd v3 Python 客户端

### 节点 {#node}

- [mixer/etcd3](https://github.com/mixer/etcd3) - 支持 v3
- [stianeikeland/node-etcd](https://github.com/stianeikeland/node-etcd) - 支持 v2（使用 CoffeeScript）
- [lavagetto/nodejs-etcd](https://github.com/lavagetto/nodejs-etcd) - 支持 v2
- [deedubs/node-etcd-config](https://github.com/deedubs/node-etcd-config) - 支持 v2

### Ruby {#ruby}

- [iconara/etcd-rb](https://github.com/iconara/etcd-rb)
- [jpfuentes2/etcd-ruby](https://github.com/jpfuentes2/etcd-ruby)
- [ranjib/etcd-ruby](https://github.com/ranjib/etcd-ruby) - 支持 v2
- [davissp14/etcdv3-ruby](https://github.com/davissp14/etcdv3-ruby) - 支持 v3

### C {#c}

- [apache/celix/etcdlib](https://github.com/apache/celix/tree/master/libs/etcdlib) - 支持 v2
- [jdarcy/etcd-api](https://github.com/jdarcy/etcd-api) - 支持 v2
- [shafreeck/cetcd](https://github.com/shafreeck/cetcd) - 支持 v2

### C++ {#c-1}

- [edwardcapriolo/etcdcpp](https://github.com/edwardcapriolo/etcdcpp) - 支持 v2
- [suryanathan/etcdcpp](https://github.com/suryanathan/etcdcpp) - 支持 v2（带等待）
- [nokia/etcd-cpp-api](https://github.com/nokia/etcd-cpp-api) - 支持 v2
- [etcd-cpp-apiv3/etcd-cpp-apiv3](https://github.com/etcd-cpp-apiv3/etcd-cpp-apiv3) - 支持 v3

### Clojure {#clojure}

- [aterreno/etcd-clojure](https://github.com/aterreno/etcd-clojure)
- [dwwoelfel/cetcd](https://github.com/dwwoelfel/cetcd) - 支持 v2
- [rthomas/clj-etcd](https://github.com/rthomas/clj-etcd) - 支持 v2

### Erlang {#erlang}

- [marshall-lee/etcd.erl](https://github.com/marshall-lee/etcd.erl) - 支持 v2
- [zhongwencool/eetcd](https://github.com/zhongwencool/eetcd) - 支持 v3+（仅 GRPC）

### Elixir {#elixir}

- [team-telnyx/etcdex](https://github.com/team-telnyx/etcdex) - 支持 v3+（仅限 GRPC）

### .NET {#net}

- [wangjia184/etcdnet](https://github.com/wangjia184/etcdnet) - 支持 v2
- [drusellers/etcetera](https://github.com/drusellers/etcetera)
- [shubhamranjan/dotnet-etcd](https://github.com/shubhamranjan/dotnet-etcd) - 支持 v3+（仅 GRPC）
- [SimplifyNet/etcd.Microsoft.Extensions.Configuration](https://github.com/SimplifyNet/Etcd.Microsoft.Extensions.Configuration)

### PHP {#php}

- [linkorb/etcd-php](https://github.com/linkorb/etcd-php)
- [activecollab/etcd](https://github.com/activecollab/etcd)
- [ouqiang/etcd-php](https://github.com/ouqiang/etcd-php) - v3 gRPC 网关的客户端

### Haskell {#haskell}

- [wereHamster/etcd-hs](https://github.com/wereHamster/etcd-hs)

### R {#r}

- [ropensci/etseed](https://github.com/ropensci/etseed)

### Nim {#nim}

- [etcd_client](https://github.com/FedericoCeratto/nim-etcd-client)

### Tcl {#tcl}

- [efrecon/etcd-tcl](https://github.com/efrecon/etcd-tcl) - 支持 v2，但不支持 wait。

### Rust {#rust}

- [jimmycuadra/rust-etcd](https://github.com/jimmycuadra/rust-etcd) - 支持 v2

### Gradle {#gradle}

- [gradle-etcd-rest-plugin](https://github.com/cdancy/gradle-etcd-rest-plugin) - 支持 v2

### Lua {#lua}

- [api7/lua-resty-etcd](https://github.com/api7/lua-resty-etcd) - 支持 v2 和 v3（gRPC 网关 HTTP API）

## 部署工具 {#deployment-tools}

### Chef 集成 {#chef-integrations}

- [coderanger/etcd-chef](https://github.com/coderanger/etcd-chef)

### Chef 转译包 {#chef-cookbooks}

- [spheromak/etcd-cookbook](https://github.com/spheromak/etcd-cookbook)

### BOSH 发行版 {#bosh-releases}

- [cloudfoundry-community/etcd-boshrelease](https://github.com/cloudfoundry-community/etcd-boshrelease)
- [cloudfoundry/cf-release](https://github.com/cloudfoundry/cf-release/tree/master/jobs/etcd)

## 使用 etcd 的项目 {#projects-using-etcd}

- [etcd Raft 用户](https://github.com/etcd-io/raft/blob/main/README.md#notable-users) - 使用 etcd 的 Raft 库实现的项目。
- [Apache APISIX](https://github.com/apache/apisix) - 将 etcd 用作配置存储的 API 网关。
- [apache/celix](https://github.com/apache/celix) - 适用于 C 和 C++ 的 OSGi 规范实现。
- [binocarlos/yoda](https://github.com/binocarlos/yoda) - etcd + ZeroMQ。
- [blox/blox](https://github.com/blox/blox) - 一组用于容器管理与编排的开源项目，支持 AWS ECS。
- [calavera/active-proxy](https://github.com/calavera/active-proxy) - 使用 etcd 配置的 HTTP 代理。
- [chain/chain](https://github.com/chain/chain) - 用于运行并连接高度可扩展的许可区块链网络的软件。
- [derekchiang/etcdplus](https://github.com/derekchiang/etcdplus) - 基于 etcd 构建的一组分布式同步原语。
- [go-discover](https://github.com/flynn/go-discover) - Go 语言中的服务发现。
- [gleicon/goreman](https://github.com/gleicon/goreman/tree/etcd) - 支持 etcd 的 Go Foreman 克隆分支。
- [garethr/hiera-etcd](https://github.com/garethr/hiera-etcd) - 使用 etcd 作为后端的 Puppet hiera 后端。
- [mattn/etcd-vim](https://github.com/mattn/etcd-vim) - 在 vim 内部进行键的 SET 和 GET 操作。
- [mattn/etcdenv](https://github.com/mattn/etcdenv) - 集成 etcd 的 "env" shebang。
- [kelseyhightower/confd](https://github.com/kelseyhightower/confd) - 使用模板和来自 etcd 的数据管理本地应用配置文件。
- [configdb](https://git.autistici.org/ai/configdb/tree/master) - 基于任意数据库后端的 REST 关系型抽象，旨在存储配置和清单。
- [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) - 由 Google 推出的容器集群管理器。
- [mailgun/vulcand](https://github.com/mailgun/vulcand) - 使用 etcd 作为配置后端的 HTTP 代理。
- [duedil-ltd/discodns](https://github.com/duedil-ltd/discodns) - 使用 etcd 作为名称和记录数据库的简单 DNS 名称服务器。
- [skynetservices/skydns](https://github.com/skynetservices/skydns) - 符合 RFC 的 DNS 服务器。
- [xordataexchange/crypt](https://github.com/xordataexchange/crypt) - 使用 GPG 加密在 etcd 中安全存储值。
- [spf13/viper](https://github.com/spf13/viper) - Go 配置库，支持从 ENV、pflags、文件和 etcd 读取值，可选加密。
- [lytics/metafora](https://github.com/lytics/metafora) - Go 语言分布式任务库。
- [ryandoyle/nss-etcd](https://github.com/ryandoyle/nss-etcd) - 用于从 etcd 解析名称的 GNU libc NSS 模块。
- [Gru](https://github.com/dnaeon/gru) - 使用 Go 实现的简易编排。
- [Vitess](http://vitess.io/) - 用于 MySQL 水平扩展的数据库集群系统。
- [lclarkmichalek/etcdhcp](https://github.com/lclarkmichalek/etcdhcp) - 使用 etcd 实现持久化和协调的 DHCP 服务器。
- [openstack/networking-vpp](https://github.com/openstack/networking-vpp) - 一个网络驱动程序，用于编程 [FD.io VPP 数据平面](https://wiki.fd.io/view/VPP)，以提供 [OpenStack](https://www.openstack.org/) 云虚拟网络。
- [OpenStack](https://github.com/openstack/governance/blob/master/reference/base-services.rst) - OpenStack 服务可依赖 etcd 作为基础服务。
- [CoreDNS](https://github.com/coredns/coredns/tree/master/plugin/etcd) - CoreDNS 是一个可插件链式组合的 DNS 服务器，属于 CNCF 和 Kubernetes 项目。
- [Uber M3](https://github.com/m3db/m3) - M3：Uber 开源的大规模指标平台，兼容 Prometheus。
- [Rook](https://github.com/rook/rook) - Kubernetes 的存储编排。
- [Patroni](https://github.com/zalando/patroni) - 基于 ZooKeeper、etcd 或 Consul 的 PostgreSQL 高可用性模板。
- [Trillian](https://github.com/google/trillian) - Trillian 实现了一种默克尔树，其内容由数据存储层提供，以支持极大规模树的可扩展性。
- [purpleidea/mgmt](https://github.com/purpleidea/mgmt) - 新一代分布式、事件驱动、并行配置管理工具。
- [Portworx/kvdb](https://docs.portworx.com/concepts/internal-kvdb/) - 用于存储 Portworx 集群配置的内部 kvdb。
- [Apache Pulsar](https://pulsar.apache.org/) - Apache Pulsar 是一个面向云的开源分布式消息与流平台。
