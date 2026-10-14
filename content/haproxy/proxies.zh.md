---
title: "4. 代理"
linkTitle: "4. 代理"
weight: 150
description: "默认设置、前端、后端、监听器、代理关键字及动作引用"
icon: fa-solid fa-right-left
module: [HAPROXY]
categories: [参考]
aliases:
  - /haproxy/configuration/proxies/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 4"
---

代理配置可位于一组段中：

- defaults [`<name>`] [ from `<defaults_name>` ]
- frontend `<name>` [ from `<defaults_name>` ]
- backend `<name>` [ from `<defaults_name>` ]
- listen `<name>` [ from `<defaults_name>` ]

前端段描述了一组用于接收客户端连接的监听套接字。

后端段描述了一组代理将连接以转发传入连接的服务器。

段 “listen” 定义了一个完整的代理，其前端和后端部分合并于同一段中。该配置通常适用于仅 TCP 流量的场景。

“defaults” 段将所有设置重置为文档中定义的默认值，并为后续段落预设新的默认值。所有“frontend”、“backend”和“listen”段始终从一个“defaults”段获取初始设置，默认情况下使用在新创建段之前出现的最新一个“defaults”段。可以通过在段行中使用可选关键字“from”后指定名称，显式指定某个特定的“defaults”段作为初始设置来源。尽管“defaults”段不强制命名，但建议命名以提高可读性。这也是唯一一种指定使用特定段而非默认前一个段的方式。由于“defaults”段名称为可选，因此默认对名称采用非常宽松的校验，甚至允许名称重叠。然而，若某个“defaults”段被其他段引用，则其名称必须符合所有代理名称的语法要求，且在所有“defaults”段中必须唯一。请注意，尽管当前允许重复段名称，但建议一般情况下避免重复，并遵循与代理名称相同的命名语法。此规则未来版本中可能被强制执行。此外，若某个“defaults”段被某个代理显式引用，同时又因是最后一个定义的段而被另一个代理隐式引用，将发出警告。强烈建议避免混合使用显式引用和隐式引用，应始终使用显式引用，或添加一个专用于所有隐式引用的最后通用“defaults”段。

请注意，defaults 段甚至可以从另一个 defaults 段获取初始设置，从而跨多个层级的 defaults 段继承设置。这种方式可以方便地建立特定的配置模板，以承载一组默认设置（例如 TCP 与 HTTP 或短超时与长超时），但可能很快变得难以追踪。

默认情况下，命名的 defaults 段会在配置解析后保留，以便创建动态后端时复用。可通过全局关键字 `tune.defaults.purge` 改变此行为。

所有代理名称必须由大写字母、小写字母、数字、"-"（连字符）、'\_'（下划线）、'.'（点号）和 ":"（冒号）组成。ACL 名称区分大小写，这意味着 "www" 和 "WWW" 是两个不同的代理。

历史上，当满足某些条件时（例如，当代理不具备相同的前端/后端能力时），所有代理名称之间可以重叠，但这曾导致日志中出现过多问题，以及在 CLI 操作、stick-table 名称和统计信息检索方面造成混淆。现在，无论代理的具体能力如何，两个代理的名称必须不同。

目前，HAProxy 支持两种主要代理模式：“tcp”（也称为第 4 层）和 “http”（也称为第 7 层）。在第 4 层模式下，HAProxy 仅在两端之间转发双向流量。在第 7 层模式下，HAProxy 会分析协议，并可根据任意条件，对请求或响应中的任意内容执行允许、阻止、切换、添加、修改或移除操作。

在 HTTP 模式下，通过连接传输的请求和响应所应用的处理方式，取决于前端的 HTTP 选项与后端选项的组合。HAProxy 支持三种连接模式：

- KAL：持久连接（"option http-keep-alive"）为默认模式：所有请求和响应均被处理，连接在响应与新请求之间保持打开状态但处于空闲状态。

- SCL：服务端关闭（"option http-server-close"）：在收到响应结束后，关闭面向服务器的连接，但保持面向客户端的连接打开。

- CLO：关闭（“option httpclose”）：在响应结束之后关闭连接，并在两个方向上附加 "Connection: close"。

通过前端和后端的连接所采用的有效模式，可根据两个代理模式按以下矩阵确定，但简而言之，模式具有对称性，持久连接为最弱选项，关闭为最强选项。

                   Backend mode

```text
                | KAL | SCL | CLO
            ----+-----+-----+----
            KAL | KAL | SCL | CLO
            ----+-----+-----+----
   模式     SCL | SCL | SCL | CLO
            ----+-----+-----+----
            CLO | CLO | CLO | CLO
```

可以将 TCP 前端与 HTTP 后端串联使用。若仅处理 HTTP 流量，则此举毫无意义。但可用于在同一个前端中处理多种协议。在此情况下，客户端连接首先作为原始 TCP 连接处理，随后升级为 HTTP。升级前，内容处理基于原始数据进行。升级后，数据将使用一种称为 HTX 的内部表示形式进行解析和存储，此时不再可能依赖原始表示形式。无法回退。

有两种升级方式：就地升级和破坏性升级。第一种涉及从 TCP 升级至 HTTP/1。在 HTTP/1 中，请求处理是串行的，因此应用层流可以被保留。第二种涉及从 TCP 升级至 HTTP/2。由于 HTTP/2 是多路复用协议，应用层流无法与任何 HTTP/2 流关联，因而被破坏。当 HAProxy 在底层 H2 多路复用器中接收到新的 HTTP/2 流时，会创建新的应用层流。理解这一差异至关重要，因为它会显著改变数据处理方式。执行 HTTP/1 升级时，对原始数据已执行的应用层处理既不会丢失也不会重新执行；而执行 HTTP/2 升级时，应用层流彼此独立，每个流都会系统性地重新评估所有前端规则。如前所述，第一个流（即 TCP 流）会被破坏，但仅在前端规则评估完成后。

当在 TCP 代理中执行 HTTP 处理时，还有一个重要点需要理解。
虽然 HAProxy 能够在 tcp-request 内容规则中实时解析 HTTP/1，但无法解析 HTTP/2。
仅能解析 HTTP/2 的前导信息（preface）。这在 TCP 环境下的 HTTP 内容分析中是一个重大限制。
具体而言，仅能判断接收到的数据是否为 HTTP。例如，无法根据 Host 头的值选择后端，而这一操作在 HTTP/1 中极为简单。
值得庆幸的是，存在一种解决方案可缓解此缺陷。

有两种方式执行 HTTP 升级。第一种是传统方法，即选择一个 HTTP 后端。当后端被设置时，升级即发生。因此，在就地升级场景下，仅考虑后端配置对 HTTP 数据处理的影响。在破坏性升级场景下，应用流被销毁，其处理过程也随之停止。采用此方法时，选择支持 HTTP/2 连接的后端的可能性极为有限，如上所述，且基本无实际意义，因为流已被销毁。第二种方法是在 tcp-request content 规则评估期间，通过 "switch-mode http" 动作执行升级。在此情况下，升级在前端上下文中进行，可以在该前端中定义 HTTP 指令。对于就地升级，可尽早获得 HTTP 分析的全部功能。其行为与 HTTP 前端非常接近。对于破坏性升级，除无法基于有限信息选择后端外，其余无实质影响。此方法为推荐方案。因此，仅需在 tcp-request content 规则中检测请求协议以执行 HTTP 升级即可。其余所有 HTTP 操作可移至前端 http-request 规则集。请注意，tcp-request content 规则始终在每个流上评估，此行为不可更改。

## 4.1. 代理关键字矩阵 {#section-4-1}

以下关键词列表受支持。大多数关键词仅可在有限的段类型中使用。部分关键词标有“已弃用”，因其继承自旧语法，可能造成混淆或功能受限，现已推荐使用新关键词替代。标有“(\*)”的关键词可选择性地通过“no”前缀进行反转，例如“no option contstats”。当某选项默认已启用，而需在特定实例中禁用时，此用法有意义。此类选项还可使用“default”前缀，以恢复默认设置，无论此前“defaults”段中如何配置。标有“(!)”的关键词仅在命名的“defaults”段中受支持，不适用于匿名段。

请注意：部分危险且不推荐使用的指令故意未列在下表中。此举出于刻意。这些指令已有文档说明，但不在下方列出，也是为了进一步劝阻用户使用。

```text
 关键字                              defaults   frontend   listen    backend
------------------------------------+----------+----------+---------+---------
acl                                       X (!)      X         X         X
backlog                                   X          X         X         -
balance                                   X          -         X         X
be-unpublished                            -          -         X         X
bind                                      -          X         X         -
capture cookie                            -          X         X         -
capture request header                    -          X         X         -
capture response header                   -          X         X         -
clitcpka-cnt                              X          X         X         -
clitcpka-idle                             X          X         X         -
clitcpka-intvl                            X          X         X         -
compression                               X          X         X         X
cookie                                    X          -         X         X
crt                                       -          X         X         -
declare capture                           -          X         X         -
default-server                            X          -         X         X
default_backend                           X          X         X         -
description                               -          X         X         X
disabled                                  X          X         X         X
dispatch                    (deprecated)  -          -         X         X
email-alert from                          X          X         X         X
email-alert level                         X          X         X         X
email-alert mailers                       X          X         X         X
email-alert myhostname                    X          X         X         X
email-alert to                            X          X         X         X
enabled                                   X          X         X         X
errorfile                                 X          X         X         X
errorfiles                                X          X         X         X
errorloc                                  X          X         X         X
errorloc302                               X          X         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
errorloc303                               X          X         X         X
error-log-format                          X          X         X         -
external-check command                    X          -         X         X
external-check path                       X          -         X         X
force-persist                             -          -         X         X
force-be-switch                           -          X         X         -
filter                                    -          X         X         X
fullconn                                  X          -         X         X
guid                                      -          X         X         X
hash-balance-factor                       X          -         X         X
hash-preserve-affinity                    X          -         X         X
hash-type                                 X          -         X         X
http-after-response                       X (!)      X         X         X
http-check comment                        X          -         X         X
http-check connect                        X          -         X         X
http-check disable-on-404                 X          -         X         X
http-check expect                         X          -         X         X
http-check send                           X          -         X         X
http-check send-state                     X          -         X         X
http-check set-var                        X          -         X         X
http-check unset-var                      X          -         X         X
http-error                                X          X         X         X
http-request                              X (!)      X         X         X
http-response                             X (!)      X         X         X
http-reuse                                X          -         X         X
http-send-name-header                     X          -         X         X
id                                        -          X         X         X
ignore-persist                            -          -         X         X
load-server-state-from-file               X          -         X         X
log                                  (*)  X          X         X         X
log-format                                X          X         X         -
log-format-sd                             X          X         X         -
log-tag                                   X          X         X         X
log-steps                                 X          X         X         -
max-keep-alive-queue                      X          -         X         X
max-session-srv-conns                     X          X         X         -
maxconn                                   X          X         X         -
mode                                      X          X         X         X
monitor fail                              -          X         X         -
monitor-uri                               X          X         X         -
option abortonclose                  (*)  X          X         X         X
option allbackups                    (*)  X          -         X         X
option checkcache                    (*)  X          -         X         X
option clitcpka                      (*)  X          X         X         -
option contstats                     (*)  X          X         X         -
option disable-h2-upgrade            (*)  X          X         X         -
option dontlog-normal                (*)  X          X         X         -
option dontlognull                   (*)  X          X         X         -
-- keyword -------------------------- defaults - frontend - listen -- backend -
option external-check                     X          -         X         X
option forwardfor                         X          X         X         X
option forwarded                     (*)  X          -         X         X
option h1-case-adjust-bogus-client   (*)  X          X         X         -
option h1-case-adjust-bogus-server   (*)  X          -         X         X
option http-buffer-request           (*)  X          X         X         X
option http-drop-request-trailers    (*)  X          -         -         X
option http-drop-response-trailers   (*)  X          -         X         -
option http-ignore-probes            (*)  X          X         X         -
option http-keep-alive               (*)  X          X         X         X
option http-no-delay                 (*)  X          X         X         X
option http-pretend-keepalive        (*)  X          -         X         X
option http-restrict-req-hdr-names        X          X         X         X
option http-server-close             (*)  X          X         X         X
option http-use-proxy-header         (*)  X          X         X         -
option httpchk                            X          -         X         X
option httpclose                     (*)  X          X         X         X
option httplog                            X          X         X         -
option httpslog                           X          X         X         -
option idle-close-on-response        (*)  X          X         X         -
option independent-streams           (*)  X          X         X         X
option ldap-check                         X          -         X         X
option log-health-checks             (*)  X          -         X         X
option log-separate-errors           (*)  X          X         X         -
option logasap                       (*)  X          X         X         -
option mysql-check                        X          -         X         X
option nolinger                      (*)  X          X         X         X
option originalto                         X          X         X         X
option persist                       (*)  X          -         X         X
option pgsql-check                        X          -         X         X
option prefer-last-server            (*)  X          -         X         X
option redispatch                    (*)  X          -         X         X
option redis-check                        X          -         X         X
option smtpchk                            X          -         X         X
option socket-stats                  (*)  X          X         X         -
option splice-auto                   (*)  X          X         X         X
option splice-request                (*)  X          X         X         X
option splice-response               (*)  X          X         X         X
option spop-check                         X          -         X         X
option srvtcpka                      (*)  X          -         X         X
option ssl-hello-chk                      X          -         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
option tcp-check                          X          -         X         X
option tcp-smart-accept              (*)  X          X         X         -
option tcp-smart-connect             (*)  X          -         X         X
option tcpka                              X          X         X         X
option tcplog                             X          X         X         -
option transparent      (deprecated) (*)  X          -         X         X
option use-small-buffers             (*)  X          -         X         X
persist rdp-cookie                        X          -         X         X
quic-initial                              X (!)      X         X         -
rate-limit sessions                       X          X         X         -
redirect                                  -          X         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
retries                                   X          -         X         X
retry-on                                  X          -         X         X
server                                    -          -         X         X
server-state-file-name                    X          -         X         X
server-template                           -          -         X         X
source                                    X          -         X         X
srvtcpka-cnt                              X          -         X         X
srvtcpka-idle                             X          -         X         X
srvtcpka-intvl                            X          -         X         X
stats admin                               -          X         X         X
stats auth                                X          X         X         X
stats enable                              X          X         X         X
stats hide-version                        X          X         X         X
stats http-request                        -          X         X         X
stats realm                               X          X         X         X
stats refresh                             X          X         X         X
stats scope                               X          X         X         X
stats show-desc                           X          X         X         X
stats show-legends                        X          X         X         X
stats show-node                           X          X         X         X
stats show-version                        X          X         X         X
stats uri                                 X          X         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
stick match                               -          -         X         X
stick on                                  -          -         X         X
stick store-request                       -          -         X         X
stick store-response                      -          -         X         X
stick-table                               -          X         X         X
tcp-check comment                         X          -         X         X
tcp-check connect                         X          -         X         X
tcp-check expect                          X          -         X         X
tcp-check send                            X          -         X         X
tcp-check send-lf                         X          -         X         X
tcp-check send-binary                     X          -         X         X
tcp-check send-binary-lf                  X          -         X         X
tcp-check set-var                         X          -         X         X
tcp-check unset-var                       X          -         X         X
tcp-request connection                    X (!)      X         X         -
tcp-request content                       X (!)      X         X         X
tcp-request inspect-delay                 X (!)      X         X         X
tcp-request session                       X (!)      X         X         -
tcp-response content                      X (!)      -         X         X
tcp-response inspect-delay                X (!)      -         X         X
timeout check                             X          -         X         X
timeout client                            X          X         X         -
timeout client-fin                        X          X         X         -
timeout client-hs                         X          X         X         -
timeout connect                           X          -         X         X
timeout http-keep-alive                   X          X         X         X
timeout http-request                      X          X         X         X
timeout queue                             X          -         X         X
timeout server                            X          -         X         X
timeout server-fin                        X          -         X         X
timeout tarpit                            X          X         X         X
timeout tunnel                            X          -         X         X
transparent                 (deprecated)  X          -         X         X
unique-id-format                          X          X         X         X
unique-id-header                          X          X         X         -
use_backend                               -          X         X         -
use-fcgi-app                              -          -         X         X
use-server                                -          -         X         X
------------------------------------+----------+----------+---------+---------
 keyword                              defaults   frontend   listen    backend
```

## 4.2. 按字母顺序排序的关键字参考 {#section-4-2}

本段描述了每个关键字及其用法。

<a id="entry-4-2-acl"></a>

**`acl <aclname> <criterion> [flags] [operator] <value> ...`**

```haproxy
acl <aclname> <criterion> [flags] [operator] <value> ...
```

声明或完成访问控制列表。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes(!) \| yes \| yes \| yes

该指令仅可在命名的 defaults 段中使用，不可在匿名段中使用。在 defaults 段中定义的 ACL 不可被使用该段的其他段访问。

示例：

```text
acl invalid_src  src          0.0.0.0/7 224.0.0.0/3
acl invalid_src  src_port     0:1023
acl local_dst    hdr(host) -i localhost
```

请参阅 [第 7 节](/zh/haproxy/acls-and-samples/) 了解 ACL 的使用方法。

<a id="entry-4-2-backlog"></a>

**`backlog <conns>`**

```haproxy
backlog <conns>
```

向系统提供关于期望监听队列大小的近似提示

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
<conns>   是待处理的连接数。根据操作系统，它可表示已确认的连接数、未确认的连接数，或两者之和。
```

此选项仅对流监听器（包括 QUIC 监听器）有意义。然而，其行为与 QUIC 实例并不完全相同。

对于除 QUIC 以外的所有监听器，为防范 SYN 洪水攻击，一种解决方案是增大系统的 SYN 队列长度。根据系统不同，该参数有时可通过系统参数调整，有时则完全不可调，有时系统会依赖应用程序在调用 listen() 系统调用时提供的提示。默认情况下，HAProxy 会将前端的 maxconn 值传递给 listen() 系统调用。在能够利用该值的系统上，有时指定不同的值会更有用，因此引入了 backlog 参数。

在 Linux 2.4 上，该参数会被系统忽略。在 Linux 2.6 上，它作为提示使用，系统最多接受小于等于最小大于该值的 2 的幂次，且永远不会超过某些限制（通常为 32768）。

对于 QUIC 监听器，backlog 为活跃握手的最大数量和待接受连接的数量设定了共享上限。握手阶段主要依赖于与远端对等节点的网络延迟，而第二阶段则完全取决于 HAProxy 的负载。当任一限制达到时，HAProxy 将开始丢弃 INITIAL 数据包的接收，阻止任何新连接的分配，直至连接数量超出部分开始下降。此情况可能导致浏览器静默降级 HTTP 版本并切换至 TCP。

另请参阅：“maxconn”以及目标操作系统的调优指南。

<a id="entry-4-2-balance"></a>

**`balance <algorithm> [ <arguments> ]`**

```haproxy
balance <algorithm> [ <arguments> ]
balance url_param <param> [check_post]
```

定义后端所使用的负载均衡算法。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<algorithm> 是负载均衡时选择服务器的算法，仅在没有可用的会话保持信息，
            或连接被重分派到另一服务器时应用。<algorithm> 可为以下值之一：

  roundrobin  按权重轮流使用各服务器。服务器处理时间分布均衡时，这是最平滑、公平的算法。
              此算法为动态算法，可在运行时调整服务器权重，例如用于慢启动。
              按设计，每个后端最多支持 4095 个活跃服务器。在某些大型服务器群中，
              服务器短暂离线后重新上线，偶尔可能需要数百个请求才重新加入并开始接收流量。
              这是正常但十分罕见的情况，在此说明以免遇到时产生疑虑。
              注意：LOG 模式后端忽略权重。

  static-rr   按权重轮流使用各服务器。与 roundrobin 类似，但为静态算法，
              因而运行时更改服务器权重无效。其服务器数量没有设计上限，
              服务器上线后，一旦完整映射重新计算完毕，便立即重新加入服务器群。
              运行时 CPU 消耗也略低（约 -1%）。此算法不可用于 LOG 模式。

  leastconn   连接数最少的服务器接收连接。负载相同的服务器组内采用轮询，以确保各服务器均被使用。
              推荐用于预期会话很长的场景，如 LDAP、SQL、TSE 等，但不太适合 HTTP 等短会话协议。
              此算法为动态算法，可在运行时调整权重，例如用于慢启动。
              除已建立连接外，还考虑排队连接数，以尽量减少排队。此算法不可用于 LOG 模式。

  first       第一个具有可用连接槽位的服务器接收连接。按数值标识符从低到高选择服务器
              （参见服务器参数 "id"），默认标识符为服务器在群组中的位置。
              服务器达到 maxconn 后使用下一服务器，未设置 maxconn 时使用此算法没有意义。
              目的是始终使用最少的服务器，以便在非繁忙时段关闭多余服务器。
              此算法忽略权重，更适合 RDP 或 IMAP 等长会话，但 HTTP 场景也可能受益。
              为高效使用，建议云控制器定期检查服务器使用情况，关闭未使用的服务器，
              并定期检查后端队列，在队列膨胀时启动新服务器。
              也可使用 "http-check send-state" 向服务器通告负载。此算法不可用于 LOG 模式。

  hash        接受普通样本表达式作为参数。每个请求均对表达式求值，并按配置的 hash-type 计算哈希。
              将哈希结果按运行中服务器的总权重取模，以确定接收请求的服务器。
              可代替 "source"、"uri"、"hdr()"、"url_param()"、"rdp-cookie"，
              以使用转换器、细化求值，或从本地变量提取数据。数据不可用时采用轮询。
              默认是静态算法，运行时更改权重无效，但可通过 "hash-type" 改变这一行为。
              不可用于 LOG 模式后端，此时请改用 "log-hash"。

  source      对源 IP 地址计算哈希，再按运行中服务器的总权重取模，以确定接收请求的服务器。
              只要没有服务器上线或离线，同一客户端 IP 地址就始终到达同一服务器。
              若运行中服务器数量变化导致哈希结果改变，许多客户端将被导向不同服务器。
              通常用于无法插入 Cookie 的 TCP 模式，也可在互联网上为拒绝会话 Cookie 的客户端
              尽力提供粘性。默认是静态算法，运行时更改权重无效，但可通过 "hash-type" 改变。
              另见上方 "hash" 选项。此算法不可用于 LOG 模式后端。

  uri         对 URI 左侧部分（问号之前）或完整 URI（使用 "whole" 参数时）计算哈希，
              再按运行中服务器的总权重取模，以确定接收请求的服务器。
              只要没有服务器上线或离线，同一 URI 就始终导向同一服务器。
              用于代理缓存和防病毒代理，以提高缓存命中率。仅可用于 HTTP 后端。
              默认是静态算法，运行时更改权重无效，但可通过 "hash-type" 改变。

              支持两个可选参数 "len" 和 "depth"，均后接正整数。
              仅需根据 URI 开头部分进行负载均衡时，这些选项可能有用。
              "len" 指定仅使用 URI 开头的相应字符数计算哈希。
              由于大多数 URI 以 "/" 开头，将 "len" 设为 1 通常没有意义。

              "depth" 指定计算哈希时使用的最大目录深度，每个斜杠计为一级。
              同时指定两个参数时，达到其中任意一个限制便停止求值。

              "path-only" 指定哈希键从路径的第一个 '/' 开始，
              可忽略绝对 URI 的 authority 部分，并确保 HTTP/1 和 HTTP/2 URI 生成相同哈希。
              另见上方 "hash" 选项。

  url_param   在每个 HTTP GET 请求的查询字符串中查找参数指定的 URL 参数。

              使用 "check_post" 修饰符时，若未在 URL 问号（'?'）之后的查询字符串中找到参数，
              则在 HTTP POST 请求实体中查找。只有收到声明的数据量或请求缓冲区已满时，
              才开始分析消息体。若少见地使用分块编码，则仅扫描首个块。
              参数值跨越块边界时，可能被随机均衡，甚至可能无法处理。
              此关键字曾支持可选的 <max_wait> 参数，目前会忽略该参数。

              找到参数，且其后有等号（'='）和值时，对该值计算哈希，
              再按运行中服务器的总权重取模，以确定接收请求的服务器。

              用于跟踪请求中的用户标识符，确保只要没有服务器上线或离线，
              同一用户 ID 始终发送到同一服务器。未找到值或参数时，应用轮询算法。
              仅可用于 HTTP 后端。默认是静态算法，运行时更改权重无效，
              但可通过 "hash-type" 改变。另见上方 "hash" 选项。

  hdr(<name>) 在每个 HTTP 请求中查找 HTTP 头 <name>。与等效的 ACL 'hdr()' 函数一样，
              括号中的头名称不区分大小写。头不存在或不包含值时，改用 roundrobin 算法。

              可选参数 'use_domain_only' 可针对 'Host' 等特定头，只用主域名部分计算哈希。
              例如，Host 值为 "haproxy.1wt.eu" 时，仅考虑 "1wt"。

              默认是静态算法，运行时更改权重无效，但可通过 "hash-type" 改变。
              另见上方 "hash" 选项。

  random
  random(<draws>)
              将随机数作为一致性哈希函数的键，因而遵守服务器权重，
              动态权重变更和新增服务器均立即生效。随机负载均衡适用于大型服务器群，
              或服务器频繁增删的情况，可避免此时 roundrobin 或 leastconn 可能导致的集中冲击。
              hash-balance-factor 指令可进一步改善公平性，尤其在服务器响应时间差异很大时。
              提供 <draws> 参数时，其值必须为大于或等于一的整数，表示抽取多少个服务器后，
              从中选择负载最小的服务器。已证明，只从两个服务器中选择负载较小者，
              就足以显著改善公平性，避免选择群组中负载最高的服务器，
              并消除一致性列表分布不均造成的偏差。更高的 N 会排除 N-1 个负载较高的候选服务器，
              但以性能为代价。值极高时，结果趋近 leastconn，但速度慢得多。
              对于负载很低或完全均衡的大型服务器群，比较负载时常出现并列。
              若所有采样服务器负载相等，则比较它们在上一秒的请求速率，
              以类似 roundrobin 的方式平衡长期使用率，并缓解一致性哈希的不公平性。
              默认值为 2，通常兼顾分布和性能。大型服务器群负载较低时
              （每台服务器每秒少于几个请求），提高到 3 或 4 可能有帮助。
              此算法又称 Power of Two Random Choices，说明见：
              http://www.eecs.harvard.edu/~michaelm/postscripts/handbook2001.pdf

              对于 LOG 模式后端，由于没有服务器负载的概念，忽略抽取次数，只抽取一个随机数。
              随机日志均衡适用于大型服务器群，或可用服务器池频繁增删的情况，
              可避免此时 roundrobin 可能导致的集中冲击。

  rdp-cookie
  rdp-cookie(<name>)
              对每个传入 TCP 请求查找 RDP Cookie <name>（省略时为 "mstshash"），并计算哈希。
              与等效的 ACL 'req.rdp_cookie()' 函数一样，名称不区分大小写。
              此机制可作为退化的会话保持模式，让同一用户或同一会话 ID 始终发送到同一服务器。
              未找到 Cookie 时，改用普通 roundrobin 算法。

              为使此机制正常工作，前端必须确保请求缓冲区中已有 RDP Cookie。
              必须使用 'tcp-request content accept' 规则与 'req.rdp_cookie_cnt' ACL 组合。

              默认是静态算法，运行时更改权重无效，但可通过 "hash-type" 改变。
              另见上方 "hash" 选项。

  log-hash    接受以逗号分隔的转换器列表作为参数。转换器依次应用于输入的日志消息，
              将结果转换为字符串，再按配置的 hash-type 计算哈希。
              使用最终哈希从日志后端声明的服务器中选择目标。
              目的是通过字符串转换器从最终日志消息中提取键，再利用哈希保持使用同一服务器。
              目前仅支持 "map-based" 哈希。仅可用于 LOG 模式后端，其他后端请改用 "hash"。

  sticky      尽可能保持使用同一服务器。可用服务器列表中的第一个服务器接收所有日志消息。
              服务器变为 DOWN 时，列表中的下一服务器接替。
              此前 DOWN 的服务器恢复 UP 时，添加到列表末尾，
              因而当前粘性目标在变为 DOWN 之前不会改变。

<arguments> 是可选的参数列表，部分算法可能需要。目前仅 "url_param"、"uri" 和 "log-hash" 支持可选参数。
```

当后端未设置其他算法、模式或选项时，其负载均衡算法默认为“random”。每个后端的算法只能设置一次。

对于需要同一连接的认证方案（如 NTLM），不得使用基于 URI 的算法，否则后续请求可能被路由至不同的后端服务器，从而破坏 NTLM 所依赖的无效假设。

TCP/HTTP 示例：

```text
balance roundrobin
balance url_param userid
balance url_param session_id check_post 64
balance hdr(User-Agent)
balance hdr(host)
balance hdr(Host) use_domain_only
balance hash req.cookie(clientid)
balance hash var(req.client_id)
balance hash req.hdr_ip(x-forwarded-for,-1),ipmask(24)
```

日志后端示例：

```text
global
  log backend@mylog-rrb local0 # send all logs to mylog-rrb backend
  log backend@mylog-hash local0 # send all logs to mylog-hash backend

backend mylog-rrb
  mode log
  balance roundrobin

  server s1 udp@127.0.0.1:514 # will receive 50% of log messages
  server s2 udp@127.0.0.1:514

backend mylog-hash
  mode log

  # extract "METHOD URL PROTO" at the end of the log message,
  # and let haproxy hash it so that log messages generated from
  # similar requests get sent to the same syslog server:
  balance log-hash 'field(-2,\")'

  # server list here
  server s1 127.0.0.1:514
  #...
```

请注意：在使用 "check_post" 扩展与 "url_param" 时，必须考虑以下注意事项和限制：

    - 所有 POST 请求都会纳入考虑，因为无法判断参数是否位于可能包含二进制
      数据的正文或实体中。因此，可能需要另一种方法来排除正文中没有 URL
      参数的 POST 请求。（参见 acl http_end）

    - 使用大于请求缓冲区大小的 `<max_wait>` 值没有意义，也没有用处。缓冲
      区大小在构建时设定，默认为 16 kB。

    - 不支持 Content-Encoding，参数搜索很可能失败；负载均衡将回退为
      轮询（Round Robin）。

    - 不支持 Expect: 100-continue，负载均衡将回退为轮询（Round Robin）。

    - Transfer-Encoding（RFC7230 3.3.1）仅在第一个块中受支持。如果完整
      的参数值未出现在第一个块中，服务器的选择将是未定义的（实际上，
      取决于第一个块中实际出现了多少内容）。

    - 此功能不支持生成 100、411 或 501 响应。

    - 在某些情况下，请求 "check_post" 可能会尝试扫描报文正文的全部内容。
      扫描通常在遇到线性空白字符或控制字符时终止，这表明可能的 URL 参数
      列表已经结束。对于 SGML 类型的报文正文，这大概不是问题。

另请参阅："dispatch"、"cookie"、"transparent"、"hash-type"。

<a id="entry-4-2-be-unpublished"></a>

**`be-unpublished`**

```haproxy
be-unpublished
```

指示后端以未发布状态启动。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

使用此指令后，其他代理中引用当前代理的 `use_backend` 和 `default_backend` 规则会被忽略，并继续评估后续的内容切换规则。不过，`force-be-switch` 规则可以绕过这一限制。

该状态与禁用状态类似，但有几点不同。首先，未发布的后端仍会完整初始化，包括继续运行服务器健康检查。其次，可通过 CLI 的 `publish backend` 命令将后端公开发布。详见管理手册。

另请参阅：`force-be-switch`

<a id="entry-4-2-bind"></a>

**`bind [<address>]:<port_range> [, ...] [param*]`**

```haproxy
bind [<address>]:<port_range> [, ...] [param*]
bind /<path> [, ...] [param*]
```

在前端中定义一个或多个监听地址和/或端口。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| no

参数：

```text
<address>     是可选参数，可为主机名、IPv4 地址、IPv6 地址或 '*'，指定前端监听的地址。
              未设置时，监听系统的所有 IPv4 地址；'*' 或系统特殊地址 "0.0.0.0" 也有相同效果。
              IPv6 对应地址为 '::'。注意，UDP 绑定多个地址时，需要特定的操作系统（OS）功能，
              才能确保响应使用正确的网络接口和源地址。因此，QUIC 监听器仅应在足够新的系统上绑定多个地址。

              可在地址前添加地址族前缀，忽略地址格式并强制使用指定地址族，
              例如指定不包含斜杠（'/'）的 unix 套接字路径时可能有用。目前支持的前缀包括：
                - 'ipv4@'  -> 地址始终为 IPv4
                - 'ipv6@'  -> 地址始终为 IPv6
                - 'udp@'   -> 地址解析为 IPv4 或 IPv6，使用 UDP 协议；目前仅在 log-forward 段支持此类监听器。
                - 'udp4@'  -> 地址始终为 IPv4，使用 UDP 协议；目前仅在 log-forward 段支持此类监听器。
                - 'udp6@'  -> 地址始终为 IPv6，使用 UDP 协议；目前仅在 log-forward 段支持此类监听器。
                - 'unix@'  -> 地址是本地 unix 套接字路径
                - 'abns@'  -> 地址位于抽象命名空间（仅 Linux）
                - 'abnsz@'  -> 地址位于抽象命名空间（仅 Linux），但显式以零终止，
                   不使用 \0 填充 sun_path；适合连接未实现 haproxy 默认 abns 命名逻辑的程序。
                - 'fd@<n>' -> 使用从父进程继承的文件描述符 <n>。fd 必须已绑定，可以已经监听，也可以尚未监听。
                - 'sockpair@<n>'-> 类似 fd@，但必须使用已连接的 unix 套接字或 socketpair 的 fd。
                  bind 等待通过 unix 套接字收到 FD，并将其当作 accept() 返回的 FD 使用。应谨慎使用。
                - 'quic4@' -> 地址解析为 IPv4，使用 UDP 协议。大流量下为获得最佳性能，
                  应保持 "tune.quic.fe.sock-per-conn
                  default-on"。否则 QUIC 连接会在监听套接字上复用。
                  另一种方法是在多个线程上复制 QUIC 监听器实例，例如通过 "shards" 关键字至少减少线程竞争。
                - 'quic6@' -> 地址解析为 IPv6，使用 UDP 协议；QUIC over IPv4 的性能说明同样适用。
                - 'rhttp@' [ EXPERIMENTAL ] -> 用于反向 HTTP。地址必须是格式为 '<backend>/<server>' 的服务器。
                  使用此服务器实例化到远程地址的连接。监听器尝试保持 "nbconn" 个连接。
                  这是实验性功能，要求在此 bind 之前的一行中启用 "expose-experimental-directives"。

              地址参数可能需要引用环境变量，参见第 2.3 节的环境变量说明。

<port_range>  是单个 TCP 端口或端口范围，代理将在上述 IP 地址上接受这些端口的连接。
              TCP 监听器必须指定端口。IPv6 地址的端口始终是最后一个冒号（':'）之后的数值。
              范围可以是：
               - 数值端口（例如 '80'）
               - 用连字符分隔，显式指定上下限且包含两端的端口范围（例如 '2000-2100'）。

              使用端口范围时须格外谨慎：每个 <address:port> 组合占用一个套接字（即一个文件描述符），
              简单的范围就可能消耗大量描述符并耗尽套接字。
              同一系统运行的所有实例之间，每个 <address:port> 组合只能使用一次。
              绑定低于 1024 的端口通常需要程序启动时具有特殊权限，与 'uid' 参数无关。

<path>        是以斜杠（'/'）开头的 UNIX 套接字路径，可替代 TCP 监听端口。
              HAProxy 在此位置的套接字上接收 UNIX 连接。路径必须以斜杠开头，默认是绝对路径，
              也可相对于 global 段中 "unix-bind" 定义的前缀。
              前缀与套接字路径的总长度不能超过 UNIX 套接字的系统限制，通常为 107 个字符。

<param*>      是同一行声明的所有套接字共用的参数列表。
              参数众多，取决于操作系统（OS）和构建选项，有专门的一节完整介绍。详情见第 5 节。
```

可以指定以逗号分隔的地址：端口组合列表。前端将在此列出的所有地址上监听。前端可监听的地址和端口数量没有固定限制，同时前端中“bind”语句的数量也没有限制。

示例：

```text
listen http_proxy
    bind :80,:443
    bind 10.0.0.1:10080,10.0.0.1:10443
    bind /var/run/ssl-frontend.sock user root mode 600 accept-proxy

listen http_https_proxy
    bind :80
    bind :443 ssl crt /etc/haproxy/site.pem

listen http_https_proxy_explicit
    bind ipv6@:80
    bind ipv4@public_ssl:443 ssl crt /etc/haproxy/site.pem
    bind unix@ssl-frontend.sock user root mode 600 accept-proxy

listen external_bind_app1
    bind "fd@${FD_APP1}"

listen h3_quic_proxy
    bind quic4@10.0.0.1:8888 ssl crt /etc/mycrt
```

请注意：关于 Linux 的抽象命名空间套接字，“abns” HAProxy 套接字使用 sun_path 的完整长度作为地址长度。其他一些程序（如 socat）默认仅使用字符串长度。如需使 socat 的抽象套接字定义与 HAProxy 兼容，请向 socat 的任意抽象套接字定义传递选项 ",unix-tightsocklen=0"，或改用 "abnsz" HAProxy 套接字族。

另请参阅：“source”、“option forwardfor”、“unix-bind”以及 PROXY 协议文档，以及关于绑定选项的[第 5 节](/zh/haproxy/bind-and-server-options/)。

<a id="entry-4-2-capture-cookie"></a>

**`capture cookie <name> len <length>`**

```haproxy
capture cookie <name> len <length>
```

捕获并记录请求和响应中的 Cookie。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| no

参数：

```text
<name>    是要捕获的 Cookie 名称的起始部分。要精确匹配名称，只需在末尾添加等号（'='）。
          日志中显示完整名称，适合会同时调整 Cookie 名称和值的应用服务器（例如 ASPSESSIONXXX）。

<length>  是在日志中报告的最大字符数，包含 Cookie 名称、等号和值，采用标准的 "name=value" 形式。
          字符串长度超过 <length> 时，从右侧截断。
```

仅捕获第一个 Cookie。同时监控“cookie”请求头和“set-cookie”响应头。此功能特别适用于检查应用程序缺陷导致的用户间会话交叉或会话窃取问题，因为通常情况下用户的 Cookie 仅在登录页面发生变更。

当客户端未提供 Cookie 时，相关日志列将报告“-”。当请求未导致服务器分配 Cookie 时，响应列将报告“-”。

捕获操作仅在前端执行，因为必须确保某个前端的日志格式不随后端变化而改变。此行为未来可能会调整。请注意，一个前端中只能存在一条“capture cookie”语句。捕获的最大长度由全局 "tune.http.cookielen" 设置决定，默认值为 63 个字符。无法在“defaults”段中指定捕获。

示例：

```text
capture cookie ASPSESSION len 32
```

另请参阅：“capture request header”、“capture response header”，以及关于日志记录的 [第 8 节](/zh/haproxy/configuration-logging/)。

<a id="entry-4-2-capture-request-header"></a>

**`capture request header <name> len <length>`**

```haproxy
capture request header <name> len <length>
```

捕获并记录指定请求头的最后一次出现。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| no

参数：

```text
<name>    是要捕获的头名称。头名称不区分大小写，但通常按其在请求中出现的形式书写，
          每个单词的首字母大写。日志中不显示头名称，仅报告其值，但保留其在日志中的位置。

<length>  是从值中提取并在日志中报告的最大字符数。字符串长度超过 <length> 时，从右侧截断。
```

捕获最后一个出现的头的完整值。该值将被添加到日志中，用大括号（'{}'）括起。若捕获多个头，它们将按配置中声明的顺序以竖线（'\|'）分隔，并依次出现。不存在的头将被记录为空字符串。请求头捕获的常见用途包括：在虚拟主机环境中捕获“Host”字段，在支持上传时捕获“Content-length”，通过“User-agent”快速区分真实用户与机器人，以及在代理环境中捕获“X-Forwarded-For”以确定请求来源。

请注意，捕获如 "User-agent" 等头时，日志中可能包含空格，这会使日志分析更加困难。因此，如果已知日志解析器不够智能，无法依赖大括号解析，请谨慎选择记录的内容。

对捕获的请求头数量和长度均无限制，但建议保持较低数量以降低每流的内存使用量。为确保同一前端的日志格式一致，头捕获只能在前端段中声明。无法在“defaults”段中指定捕获。

示例：

```text
capture request header Host len 15
capture request header X-Forwarded-For len 15
capture request header Referer len 15
```

另请参阅：“capture cookie”、“capture response header”，以及关于日志记录的 [第 8 节](/zh/haproxy/configuration-logging/)。

<a id="entry-4-2-capture-response-header"></a>

**`capture response header <name> len <length>`**

```haproxy
capture response header <name> len <length>
```

捕获并记录指定响应头的最后一次出现。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| no

参数：

```text
<name>    是要捕获的头名称。头名称不区分大小写，但通常按其在响应中出现的形式书写，
          每个单词的首字母大写。日志中不显示头名称，仅报告其值，但保留其在日志中的位置。

<length>  是从值中提取并在日志中报告的最大字符数。字符串长度超过 <length> 时，从右侧截断。
```

最后一次出现的头字段的完整值将被捕获。捕获结果将被添加到日志中，位于捕获的请求头之后，用大括号（'{}'）括起。若捕获了多个头字段，它们将以竖线（'\|'）分隔，并按配置中声明的顺序出现。不存在的头字段将被记录为空字符串。响应头捕获的常见用途包括“Content-length”头，用于指示预期返回的字节数，以及“Location”头，用于追踪重定向。

对响应头的捕获数量和长度均无限制，但建议保持较低数量以控制每流的内存使用量。为确保同一前端的日志格式一致，头捕获只能在前端中声明。无法在“defaults”段中指定捕获。

示例：

```text
capture response header Content-length len 9
capture response header Location len 15
```

另请参阅：“capture cookie”、“capture request header”，以及关于日志记录的 [第 8 节](/zh/haproxy/configuration-logging/)。

<a id="entry-4-2-clitcpka-cnt"></a>

**`clitcpka-cnt <count>`**

```haproxy
clitcpka-cnt <count>
```

设置 TCP 在客户端侧丢弃连接前应发送的最大保活探测次数。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
<count>   是保活探测的最大次数。
```

此关键字对应套接字选项 TCP_KEEPCNT。若未指定此关键字，则使用系统级 TCP 参数（tcp_keepalive_probes）。该设置的可用性取决于操作系统。已知其在 Linux 上可用。

另请参阅：“option clitcpka”、“clitcpka-idle”、“clitcpka-intvl”。

<a id="entry-4-2-clitcpka-idle"></a>

**`clitcpka-idle <timeout>`**

```haproxy
clitcpka-idle <timeout>
```

设置连接在 TCP 开始发送保活探测前需保持空闲的时间，若启用，则在客户端侧发送 TCP 保活数据包。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
<timeout> 是连接保持空闲多久后 TCP 开始发送保活探测的时间。默认单位为秒，
          也可在数值后添加单位后缀，使用其他单位，详见本文开头的说明。
```

此关键字对应套接字选项 TCP_KEEPIDLE。若未指定此关键字，则使用系统级 TCP 参数（tcp_keepalive_time）。该设置的可用性取决于操作系统。已知其在 Linux 上可用。

另请参阅：“option clitcpka”、“clitcpka-cnt”、“clitcpka-intvl”。

<a id="entry-4-2-clitcpka-intvl"></a>

**`clitcpka-intvl <timeout>`**

```haproxy
clitcpka-intvl <timeout>
```

设置客户端侧单个 keepalive 探测之间的时间间隔。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
<timeout> 是两次保活探测之间的时间。默认单位为秒，也可在数值后添加单位后缀，
          使用其他单位，详见本文开头的说明。
```

此关键字对应套接字选项 TCP_KEEPINTVL。若未指定此关键字，则使用系统级 TCP 参数（tcp_keepalive_intvl）。该设置的可用性取决于操作系统。已知其在 Linux 上可用。

另请参阅：“option clitcpka”、“clitcpka-cnt”、“clitcpka-idle”。

<a id="entry-4-2-compression-algo"></a>

**`compression algo <algorithm> ...`**

```haproxy
compression algo <algorithm> ...
compression algo-req <algorithm>
compression algo-res <algorithm>
compression type <mime type> ...
```

启用 HTTP 压缩。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
algo     后接受支持的响应压缩算法列表（旧版关键字）。
algo-req 后接请求压缩算法（仅提供一种）。
algo-res 后接受支持的响应压缩算法列表。
type     后接要压缩的响应 MIME 类型列表（旧版关键字）。
type-req 后接要压缩的请求 MIME 类型列表。
type-res 后接要压缩的响应 MIME 类型列表。
```

当前支持的算法如下：

```text
identity     主要用于调试，曾用于开发压缩功能。Identity 不对数据作任何修改。

gzip         应用 gzip 压缩，仅在编译时启用了 zlib 或 libslz 支持时可用。

deflate      与 "gzip" 相同，但使用 deflate 算法和 zlib 格式。
             许多浏览器对此算法的支持含糊不清，近期浏览器甚至完全不支持。
             强烈建议仅用于实验。仅在编译时启用了 zlib 或 libslz 支持时可用。

raw-deflate  与 "deflate" 相同，但不使用 zlib 封装，在浏览器要求 "deflate" 时用作替代方案。
             所有主流浏览器均能理解它；尽管违反标准，已知它至少在 MSIE 和某些 Safari 版本中
             比 "deflate" 工作得更好。不要与 "deflate" 同时使用，二者只能择一，
             因为都会响应同一个 Accept-Encoding 词元。仅在编译时启用了 zlib 或 libslz 支持时可用。
```

压缩功能将根据请求头中的 Accept-Encoding 决定是否启用。若设置为 identity，则忽略该请求头。若后端服务器支持 HTTP 压缩，这些指令将无操作：HAProxy 会识别已压缩的响应，不再进行二次压缩。若后端服务器不支持 HTTP 压缩，且请求中包含 Accept-Encoding 头，则 HAProxy 将对匹配的响应进行压缩。

当满足以下任一条件时，压缩功能将被禁用：   - 请求未在 "Accept-Encoding" 头中声明支持的压缩算法   - 响应消息的协议版本低于 HTTP/1.1   - HTTP 状态码不是 200、201、202 或 203 之一   - 响应既不包含 "Content-Length" 头，也不包含 "Transfer-Encoding" 头且其最后一个值不是 "chunked"   - 响应包含 "Content-Type" 头，且其首个值以 "multipart" 开头   - 响应包含 "Cache-control" 头且其值包含 "no-transform"   - User-Agent 匹配 "Mozilla/4"，除非其为 MSIE 6 且运行于 XP SP2，或 MSIE 7 及更高版本   - 响应包含 "Content-Encoding" 头，表明响应已压缩（参见压缩卸载）   - 响应包含无效的 "ETag" 头或多个 ETag 头   - 负载大小小于最小大小（参见 compression minsize-res）

请注意：压缩功能不会发出 Warning 头。

示例：

```text
compression algo gzip
compression type text/html text/plain
```

另请参阅：“compression offload”、“compression direction”、“compression minsize-req”和“compression minsize-res”

<a id="entry-4-2-compression-minsize-req"></a>

**`compression minsize-req <size>`**

```haproxy
compression minsize-req <size>
compression minsize-res <size>
```

设置应用压缩功能的最小负载大小（以字节为单位）。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

小于该大小的负载将不会被压缩，以避免对无法显著受益于压缩的数据造成不必要的 CPU 开销。“minsize-req” 适用于请求，“minsize-res” 适用于响应。默认值为 0。

<a id="entry-4-2-compression-offload"></a>

**`compression offload`**

```haproxy
compression offload
```

使 HAProxy 仅作为压缩卸载器工作。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| yes

offload 设置会使 HAProxy 移除 Accept-Encoding 头，以防止后端服务器对响应进行压缩。强烈建议不要执行此操作，因为这意味着所有压缩工作都将集中于 HAProxy 所在的单一节点上。然而在某些部署场景中，HAProxy 可能位于存在缺陷的网关前端，而该网关的 HTTP 压缩实现存在缺陷且无法关闭。在此情况下，HAProxy 可用于防止该网关发出无效负载。在这种场景下，仅在配置中移除头信息无效，因为该操作在头信息被解析前执行，从而阻止了 HAProxy 自身进行压缩。此时应使用 offload 设置。

如果在 defaults 段中使用此设置，将发出警告并忽略该选项。

另请参阅：“压缩类型”、“压缩算法”、“压缩方向”

<a id="entry-4-2-compression-direction"></a>

**`compression direction <direction> (deprecated)`**

```haproxy
compression direction <direction> (deprecated)
```

使 HAProxy 能够压缩请求和响应。有效值为 "request"，仅压缩请求；"response"，仅压缩响应；或 "both"，当需要同时压缩请求和响应时使用。默认值为 "response"。

该指令仅在启用旧版“过滤器压缩”时才相关，因为当显式使用 comp-req 和 comp-res 过滤器时，压缩方向已冗余。

可用于以下上下文：http

另请参阅："compression type"、"compression algo"、"compression offload"

<a id="entry-4-2-cookie"></a>

**`cookie <name> [ rewrite | insert | prefix ] [ indirect ] [ nocache ]`**

```haproxy
cookie <name> [ rewrite | insert | prefix ] [ indirect ] [ nocache ]
              [ postonly ] [ preserve ] [ httponly ] [ secure ]
              [ domain <domain> ]* [ maxidle <idle> ] [ maxlife <life> ]
              [ dynamic ] [ attr <value> ]*
```

在后端中启用基于 Cookie 的持久性。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<name>    是为实现会话保持而监控、修改或插入的 Cookie 名称。
          通过响应中的 "Set-Cookie" 头发送给客户端，再由客户端在所有请求的 "Cookie" 头中带回。
          应谨慎选择名称，避免与应用可能使用的 Cookie 冲突。
          同一客户端可能使用相同后端（例如 HTTP/HTTPS）时，
          若不希望在后端之间保持会话，应为各后端使用不同的 Cookie 名称。

rewrite   表示由服务器提供 Cookie，HAProxy 修改其值，将服务器标识符写入其中。
          将复杂的 "Set-cookie" 与 "Cache-control" 头组合交给应用管理时，此模式十分方便。
          应用可自行决定是否适合发送会话保持 Cookie。
          由于必须监控所有响应，此模式不适用于 HTTP 隧道模式。
          除非应用行为十分复杂或存在缺陷，否则不建议新部署从此模式开始。
          此关键字与 "insert"、"prefix" 不兼容。

insert    若客户端尚未具有能让其访问此服务器的 Cookie，则由 HAProxy 在服务器响应中插入会话保持 Cookie。
          未使用 "preserve" 选项时，服务器发送的同名 Cookie 会在处理前移除，
          因此可用此模式升级原先采用 "rewrite" 模式的配置。
          插入的 Cookie 仅为会话 Cookie，不存储到客户端磁盘。
          默认情况下，除非添加 "indirect" 选项，否则服务器会看到客户端发送的 Cookie。
          考虑缓存影响，通常应添加 "nocache" 或 "postonly"（见下文）。
          "insert" 与 "rewrite"、"prefix" 不兼容。

prefix    表示不依赖专用的会话保持 Cookie，而是补充现有 Cookie。
          某些特殊环境中，客户端仅支持单个 Cookie，且应用已需要该 Cookie，此模式可能有用。
          服务器设置名为 <name> 的 Cookie 时，在其值前添加服务器标识符和分隔符。
          所有客户端请求中的该前缀会被移除，使服务器仍能读到原先发送的 Cookie。
          由于所有请求和响应均可能被修改，此模式不适用于隧道模式。
          "prefix" 与 "rewrite"、"insert" 不兼容。
          注意：强烈建议不要将 "indirect" 与 "prefix" 组合，否则服务器更新的 Cookie 不会发送给客户端。

indirect  已有对应处理请求的服务器的有效 Cookie 时，不再向客户端发送 Cookie。
          服务器自行设置此类 Cookie 时，会将其移除，除非同时设置 "preserve"。
          在 "insert" 模式下，还会从发往服务器的请求中移除 Cookie，
          从应用的角度使会话保持机制完全透明。
          注意：强烈建议不要将 "indirect" 与 "prefix" 组合，否则服务器更新的 Cookie 不会发送给客户端。

nocache   客户端与 HAProxy 之间存在缓存时，推荐与插入模式组合。
          需要插入 Cookie 时，确保将本可缓存的响应标记为不可缓存。
          例如，若所有会话保持 Cookie 都在可缓存的主页中插入，所有用户会从外部缓存获取页面，
          并共享同一会话保持 Cookie，导致一台服务器接收远多于其他服务器的流量。
          另见 "insert" 和 "postonly"。

postonly  确保仅在 POST 请求的响应中插入 Cookie，可替代 "nocache"。
          POST 响应不可缓存，因而会话保持 Cookie 不会被缓存。
          大多数站点在首次 POST（通常为登录请求）之前不需要会话保持，
          因此此方法可高效优化缓存，而不必担心缓存中出现会话保持 Cookie。
          另见 "insert" 和 "nocache"。

preserve  仅可与 "insert" 和/或 "indirect" 组合，允许服务器自行发送会话保持 Cookie。
          响应中存在该 Cookie 时，HAProxy 不修改它，例如可用于在登出请求后结束会话保持。
          服务器只需发送值无效（如空值）或日期已过期的 Cookie。
          与 "disable-on-404" 检查选项组合，可实现完全优雅关闭，
          因为用户登出后会确定离开该服务器。

httponly  告诉 HAProxy 在插入 Cookie 时添加 "HttpOnly" 属性，
          防止用户代理与非 HTTP 组件共享 Cookie。此属性详情见 RFC6265。

secure    告诉 HAProxy 在插入 Cookie 时添加 "Secure" 属性，
          防止用户代理通过不安全通道发送该 Cookie；带此标志的 Cookie 仅通过 SSL/TLS 连接发送。
          此属性详情见 RFC6265。

domain    指定插入 Cookie 的域，必须且只能接受一个参数：有效域名。
          域名以点号开头时，浏览器可将 Cookie 用于所有以此名称结尾的主机。
          可重复使用此选项指定多个域名。某些浏览器可能限制域名数量，应谨慎使用。
          作为参考，向 MSIE 6 或 Firefox 2 发送 10 个域名可以正常工作。

maxidle   允许在空闲一段时间后忽略插入的 Cookie，仅适用于插入模式。
          向客户端发送 Cookie 时，同时发送其发出日期。
          客户端再次提供 Cookie 时，若日期超过参数指定的时长（秒），则忽略该 Cookie；
          否则，在响应发送给客户端时按需刷新。
          适合防止永不关闭浏览器的用户在同一服务器上停留过久，例如服务器群规模变更后。
          设置此选项且 Cookie 没有日期时，始终接受，但在响应中刷新，以保留管理员访问站点的能力。
          日期超过当前时间向后 24 小时的 Cookie 会被忽略，
          以便管理员修复时区问题，而不冒着将用户踢出站点的风险。

maxlife   允许在存活一段时间后忽略插入的 Cookie，无论其是否正在使用，仅适用于插入模式。
          首次向客户端发送 Cookie 时，同时发送其发出日期。
          客户端再次提供 Cookie 时，若日期超过参数指定的时长（秒），则忽略该 Cookie。
          请求的 Cookie 没有日期时，接受该 Cookie 并设置日期。
          日期超过当前时间向后 24 小时的 Cookie 会被忽略，
          以便管理员修复时区问题，而不冒着将用户踢出站点的风险。
          与 maxidle 不同，此值不会刷新，仅首次访问日期有效。maxidle 和 maxlife 可同时使用。
          适合防止永不关闭浏览器的用户在同一服务器上停留过久，例如服务器群规模变更后。
          比 maxidle 更强，因为经过固定时长后强制重分派。

dynamic   启用动态 Cookie。根据服务器 IP、端口及 "dynamic-cookie-key" 后端指令指定的密钥，
          为每台服务器动态创建会话 Cookie。IP 地址每次变化时重新生成，仅针对 IPv4/IPv6 生成。

attr      告诉 HAProxy 在插入 Cookie 时添加额外属性。
          属性值可包含除控制字符和 ";" 以外的任何字符。此选项可重复使用。
```

每个 HTTP 后端只能有一个持久性 cookie，该 cookie 可在 defaults 段中声明。cookie 的值将为服务器语句中 "cookie" 关键字后指定的值。若未为某个服务器声明 cookie，则不会设置 cookie。

示例：

```text
cookie JSESSIONID prefix
cookie SRV insert indirect nocache
cookie SRV insert postonly indirect
cookie SRV insert indirect nocache maxidle 30m maxlife 8h
```

另请参阅：“balance source”、“capture cookie”、“server”和“ignore-persist”。

<a id="entry-4-2-declare-capture"></a>

**`declare capture [ request | response ] len <length>`**

```haproxy
declare capture [ request | response ] len <length>
```

声明一个捕获槽。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| no

参数：

```text
<length> 是允许捕获的长度。
```

此声明仅可在前端或 listen 段中使用，但预留的槽位可在后端中使用。“request”关键字用于为请求分配一个捕获槽位，“response”关键字用于为响应分配一个捕获槽位。

另请参阅：“capture-req”、“capture-res”（样本转换器）、"capture.req.hdr"、"capture.res.hdr"（样本提取）、“http-request capture”和“http-response capture”。

<a id="entry-4-2-default-server"></a>

**`default-server [param*]`**

```haproxy
default-server [param*]
```

更改后端中服务器的默认选项

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<param*>  是此服务器的参数列表。"default-server" 关键字支持大量选项，有专门的一节完整介绍。
          更多详情见第 5 节。
```

示例：

```text
default-server inter 1000 weight 13
```

另请参阅：“server”以及 [第 5 节](/zh/haproxy/bind-and-server-options/) 中关于服务器选项的内容

<a id="entry-4-2-default-backend"></a>

**`default_backend <backend>`**

```haproxy
default_backend <backend>
```

当未匹配任何 "use_backend" 规则时，指定要使用的后端。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
<backend> 是要使用的后端名称。
```

使用 "use_backend" 关键字在前端与后端之间进行内容切换时，通常需要明确指定当无规则匹配时将使用的后端。这通常是动态后端，用于捕获所有未确定的请求。

如果后端被禁用或未发布，针对该后端的 default_backend 规则将被忽略，流处理将继续在原始代理上进行。

示例：

```text
use_backend     dynamic  if  url_dyn
use_backend     static   if  url_css url_img extension_img
default_backend dynamic
```

另请参阅："use_backend"

<a id="entry-4-2-description"></a>

**`description <string>`**

```haproxy
description <string>
```

描述一个 listen、frontend 或 backend。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| yes

参数：string

允许在 HAProxy HTML 统计信息页面中为相关对象添加描述语句。描述内容将显示在所描述对象名称的右侧。`<string>` 参数中无需转义空格。

<a id="entry-4-2-disabled"></a>

**`disabled`**

```haproxy
disabled
```

禁用代理、前端或后端。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

“disabled” 关键字用于禁用实例，主要用于释放监听端口或临时停用服务。实例仍将被创建并进行配置检查，但将以“已停止”状态创建，并在统计信息中显示为已停止状态。该实例不会接收任何流量，也不会发送健康检查或日志。可以通过在“defaults”段中添加“disabled”关键字，一次性禁用多个实例。

默认情况下，无法选择已禁用的后端进行内容切换。然而，当使用 "force-be-switch" 时，部分流量可忽略此限制。

另请参阅："enabled"，"force-be-switch"

<a id="entry-4-2-dispatch"></a>

**`dispatch <address>:<port>   (deprecated)`**

```haproxy
dispatch <address>:<port>   (deprecated)
```

设置默认服务器地址

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

参数：

```text
<address> 是默认服务器的 IPv4 地址。也支持可解析的主机名，但该名称在启动期间解析。

<ports>   是必需的端口参数。所有连接均发送到此端口，不允许像普通服务器那样使用端口偏移。
```

dispatch 指令

"dispatch" 指令用于指定在无法连接到其他服务器时使用的默认服务器。过去，该指令曾用于将非持久连接转发至辅助负载均衡器。由于其语法简单，也曾被用于实现简单的 TCP 中继。为提高配置清晰度，建议不再使用该指令，而应改用 "server" 指令。

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除，原因在于存在一些内部限制（例如不支持 SSL 或空闲连接等）。使用该关键字将发出警告，可通过在全局段启用指令 "expose-deprecated-directives" 来静默此警告。

正确做法是，不使用该指令时，只需声明一个地址和端口相同的服务器。如果“dispatch”指令与其他服务器混合使用，则应将这些服务器的权重配置为零，以确保负载均衡算法永远不会选择它们。

示例：

```text
backend deprecated_setup
    dispatch 192.168.100.100:80 # external load balancer's address
    server s1 192.168.100.1:80 cookie S1 check
    server s2 192.168.100.2:80 cookie S2 check

backend modern_setup
    server external_lb 192.168.100.100:80
    server s1 192.168.100.1:80 cookie S1 check weight 0
    server s2 192.168.100.2:80 cookie S2 check weight 0
```

另请参阅："server"

<a id="entry-4-2-dynamic-cookie-key"></a>

**`dynamic-cookie-key <string>`**

```haproxy
dynamic-cookie-key <string>
```

为后端设置动态 Cookie 密钥。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：用于的密钥。

当启用动态 cookie（参见 cookie 指令中的 "dynamic" 选项）时，将为每个服务器创建一个动态 cookie（除非在 "server" 指令中显式指定），该 cookie 通过服务器的 IP 地址、TCP 端口和密钥的哈希值生成。这样可确保在多个负载均衡器之间实现会话持久性，即使服务器动态添加或移除也能保持会话连续。

<a id="entry-4-2-enabled"></a>

**`enabled`**

```haproxy
enabled
```

启用代理、前端或后端。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

"enabled" 关键字用于显式启用实例，当默认值已设为 "disabled" 时使用。此用法极为罕见。

另请参阅："be-unpublished"、"disabled"

<a id="entry-4-2-errorfile"></a>

**`errorfile <code> <file>`**

```haproxy
errorfile <code> <file>
```

返回文件内容，而非 HAProxy 生成的错误信息

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<code>    是 HTTP 状态码。目前 HAProxy 可生成的状态码为
          200、400、401、403、404、405、407、408、410、413、414、425、429、431、500、501、502、503 和 504。

<file>    指定包含完整 HTTP 响应的文件。建议遵循常见做法，在文件名末尾添加 ".http"，
          避免将响应与 HTML 错误页面混淆；还应使用绝对路径，因为文件在执行 chroot 之前读取。
```

必须理解，该关键字并非用于重写服务器返回的错误，而是用于重写 HAProxy 检测并返回的错误。这也是为何支持的错误列表被限制在较小的集合中。

状态码 200 在响应匹配 "monitor-uri" 规则的请求时发出。

HAProxy 启动时会解析这些文件，且必须符合 HTTP 规范。文件大小不得超过配置的缓冲区大小（BUFSIZE），通常为 16 kB，否则将返回内部错误。建议不要引用本地内容（例如图片），以避免在所有服务器均不可用时，客户端与 HAProxy 之间产生循环，导致返回错误而非图片。最后，响应大小不得超过（tune.bufsize - tune.maxrewrite），以确保“http-after-response”规则仍有操作空间（参见 "tune.maxrewrite"）。

文件在读取配置的同时被加载并保留在内存中。因此，即使进程已执行 chroot，错误仍会持续返回，且在进程运行期间不会考虑文件的任何变更。开发这些文件的一种简单方法是将其与 403 状态码关联，并查询一个被阻止的 URL。

另请参阅："http-error", "errorloc", "errorloc302", "errorloc303"

示例：

```text
errorfile 400 /etc/haproxy/errorfiles/400badreq.http
errorfile 408 /dev/null  # work around Chrome pre-connect bug
errorfile 403 /etc/haproxy/errorfiles/403forbid.http
errorfile 503 /etc/haproxy/errorfiles/503sorry.http

```

<a id="entry-4-2-errorfiles"></a>

**`errorfiles <name> [<code> ...]`**

```haproxy
errorfiles <name> [<code> ...]
```

导入在 `<name>` http-errors 段中定义的错误文件，可全部或部分导入。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<name>  是已存在的 http-errors 段的名称。

<code>  是 HTTP 状态码，可列出多个。目前 HAProxy 可生成的状态码为
        200、400、401、403、404、405、407、408、410、413、414、425、429、431、500、501、502、503 和 504。
```

在 http-errors 段中定义的名称为 `<name>` 的错误会被导入当前代理。

若未指定状态码，则导入 http-errors 段中的所有错误文件。否则，仅导入与所列状态码关联的错误文件。这些错误文件将覆盖代理中已定义的自定义错误，且可能被后续导入的错误文件覆盖。

在功能上，这与手动使用 "errorfile" 指令声明所有错误文件完全相同。

有关 HTTP 错误的更多信息，请参阅 "http-error"、"errorfile"、"errorloc"、"errorloc302"、"errorloc303" 以及 [第 12.4 节](/zh/haproxy/other-sections/#section-12-4)。

示例：

```text
errorfiles generic
errorfiles site-1 403 404

```

<a id="entry-4-2-errorloc"></a>

**`errorloc <code> <url>`**

```haproxy
errorloc <code> <url>
errorloc302 <code> <url>
```

返回 HTTP 重定向至指定 URL，而非 HAProxy 生成的错误

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<code>    是 HTTP 状态码。目前 HAProxy 可生成的状态码为
          200、400、401、403、404、405、407、408、410、413、414、425、429、431、500、501、502、503 和 504。

<url>     是 "Location" 头的确切内容，可以是同一站点错误页面的相对 URI，
          或另一站点错误页面的绝对 URI。使用相对 URI 时应格外谨慎，
          避免 URI 本身产生同样的错误（例如 500）而导致重定向循环。
```

必须理解，该关键字并非用于重写服务器返回的错误，而是用于重写 HAProxy 检测并返回的错误。这也是为何支持的错误列表被限制在较小的集合中。

状态码 200 在响应匹配 "monitor-uri" 规则的请求时发出。

请注意，这两个关键字均返回 HTTP 302 状态码，指示客户端使用相同的 HTTP 方法获取指定的 URL。在使用非 GET 方法（如 POST）时，这可能会造成问题，因为发送给客户端的 URL 可能不允许用于除 GET 以外的其他方法。为规避此问题，请使用 "errorloc303"，该关键字发送 HTTP 303 状态码，指示客户端必须使用 GET 请求获取该 URL。

另请参阅："http-error"、"errorfile"、"errorloc303"

<a id="entry-4-2-errorloc303"></a>

**`errorloc303 <code> <url>`**

```haproxy
errorloc303 <code> <url>
```

返回 HTTP 重定向至指定 URL，而非 HAProxy 生成的错误

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<code>    是 HTTP 状态码。目前 HAProxy 可生成的状态码为
          200、400、401、403、404、405、407、408、410、413、414、425、429、431、500、501、502、503 和 504。

<url>     是 "Location" 头的确切内容，可以是同一站点错误页面的相对 URI，
          或另一站点错误页面的绝对 URI。使用相对 URI 时应格外谨慎，
          避免 URI 本身产生同样的错误（例如 500）而导致重定向循环。
```

必须理解，该关键字并非用于重写服务器返回的错误，而是用于重写 HAProxy 检测并返回的错误。这也是为何支持的错误列表被限制在较小的集合中。

状态码 200 在响应匹配 "monitor-uri" 规则的请求时发出。

请注意，这两个关键字均返回 HTTP 303 状态码，该码指示客户端使用相同的 HTTP GET 方法获取指定的 URL。这解决了与“errorloc”和 302 状态码相关联的常见问题。尽管可能存在一些在 HTTP/1.1 之前设计的老旧浏览器不支持此行为，但截至目前尚未报告此类问题。

另请参阅："http-error"、"errorfile"、"errorloc"、"errorloc302"

<a id="entry-4-2-email-alert-from"></a>

**`email-alert from <emailaddr>`**

```haproxy
email-alert from <emailaddr>
```

声明用于邮件警报信封和头中的发件人地址。此地址即为邮件警报的发送来源。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<emailaddr> 是发送邮件告警时使用的发件人邮箱地址。
```

还要求设置 "email-alert mailers" 和 "email-alert to"，若已设置，则为该代理启用邮件告警功能。

另请参阅：“email-alert level”、“email-alert mailers”、“email-alert myhostname”、“email-alert to”，以及关于邮件发送器的[第 12.3 节](/zh/haproxy/other-sections/#section-12-3)。

<a id="entry-4-2-email-alert-level"></a>

**`email-alert level <level>`**

```haproxy
email-alert level <level>
```

声明将发送邮件告警的消息最大日志级别。这将作为邮件告警发送的过滤器。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<level> 为 8 个 syslog 级别之一：
          emerg alert crit err warning notice info  debug
        上述 syslog 级别按从低到高的顺序排列。
```

默认级别为 alert

还要求设置 "email-alert from"、"email-alert mailers" 和 "email-alert to"，若已设置，则为该代理启用邮件告警功能。

当满足以下条件时发送告警：

- 未暂停的服务器被标记为不可用，且 `<level>` 的日志级别为 alert 或更低
- 暂停的服务器被标记为不可用，且 `<level>` 的日志级别为 notice 或更低
- 服务器被标记为可用或进入 drain 状态，且 `<level>` 的日志级别为 notice 或更低
- 启用了 "option log-health-checks"，`<level>` 的日志级别为 info 或更低，且发生健康检查状态更新

另请参阅：“email-alert from”、“email-alert mailers”、“email-alert myhostname”、“email-alert to”，以及关于邮件发送器的[第 12.3 节](/zh/haproxy/other-sections/#section-12-3)。

<a id="entry-4-2-email-alert-mailers"></a>

**`email-alert mailers <mailersect>`**

```haproxy
email-alert mailers <mailersect>
```

声明用于发送邮件告警的邮件发送器

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<mailersect> 是用于发送邮件告警的 mailers 段的名称。
```

还要求设置 "email-alert from" 和 "email-alert to"，若已设置，则为该代理启用邮件告警功能。

另请参阅："email-alert from"、"email-alert level"、"email-alert myhostname"、"email-alert to"，以及关于邮件发送器的[第 12.3 节](/zh/haproxy/other-sections/#section-12-3)。

<a id="entry-4-2-email-alert-myhostname"></a>

**`email-alert myhostname <hostname>`**

```haproxy
email-alert myhostname <hostname>
```

声明用于与邮件发送器通信时的主机名地址。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<hostname> 是与 mailers 通信时使用的主机名。
```

默认情况下，使用系统的主机名。

还要求设置 "email-alert from"、"email-alert mailers" 和 "email-alert to"，若已设置，则为该代理启用邮件告警功能。

另请参阅：“email-alert from”、“email-alert level”、“email-alert mailers”、“email-alert to”，以及关于邮件发送器的[第 12.3 节](/zh/haproxy/other-sections/#section-12-3)。

<a id="entry-4-2-email-alert-to"></a>

**`email-alert to <emailaddr>`**

```haproxy
email-alert to <emailaddr>
```

声明邮件警报信封中的收件人地址以及邮件头中的收件人地址。
此地址为邮件警报的发送目标。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<emailaddr> 是发送邮件告警时使用的收件人邮箱地址。
```

还要求设置 "email-alert mailers" 和 "email-alert to"，若已设置，则为该代理启用邮件告警功能。

另请参阅："email-alert from"、"email-alert level"、"email-alert mailers"、"email-alert myhostname"，以及关于邮件发送器的 [第 12.3 节](/zh/haproxy/other-sections/#section-12-3)。

<a id="entry-4-2-error-log-format"></a>

**`error-log-format <fmt>`**

```haproxy
error-log-format <fmt>
```

指定在前端发生连接错误时所使用的日志格式字符串。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

该指令指定用于记录与错误、超时、重试、重分派或 HTTP 状态码 5xx 相关信息的日志格式字符串。该格式将简要用于所有受“log-separate-errors”选项影响的日志行，包括 [第 8.2.5 节](/zh/haproxy/configuration-logging/#section-8-2-5)中描述的连接错误。

若该指令在 defaults 段中使用，则后续所有前端均将采用相同的日志格式。请参见 [第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6)，其中详细介绍了自定义日志格式字符串。

"error-log-format" 指令会覆盖之前的 "error-log-format" 指令。

<a id="entry-4-2-force-persist"></a>

**`force-persist { if | unless } <condition>`**

```haproxy
force-persist { if | unless } <condition>
```

声明一个条件，以强制对已关闭的服务器保持持久性

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

默认情况下，请求不会被分派至处于关闭状态的服务器。可以使用“option persist”强制分派，但该选项无条件生效，若设置了“option redispatch”，则会在有可用服务器时进行重分派。这使得强制某些请求到达因维护操作而被人为标记为关闭的服务器变得几乎不可能。

"force-persist" 语句允许声明多种基于 ACL 的条件，当这些条件满足时，请求将忽略服务器的宕机状态，仍尝试与其建立连接。这使得可以在服务器启动后，仍对健康检查返回错误，同时使用经过特殊配置的浏览器来测试服务。其中一种便捷的方法是使用特定的源 IP 地址，或特定的 Cookie。Cookie 的优势在于，可通过测试页面轻松地在浏览器中添加或移除。服务验证完成后，即可通过向健康检查返回有效响应，将服务对公众开放。

当满足 "if" 条件时，强制持久化功能被启用，或在满足 "unless" 条件时被禁用。使用此功能时，最终的重分派始终被禁用。

另请参阅：“option redispatch”、“ignore-persist”、“persist”以及[第 7 节](/zh/haproxy/acls-and-samples/)中关于 ACL 使用的说明。

<a id="entry-4-2-external-check-command"></a>

**`external-check command <command>`**

```haproxy
external-check command <command>
```

执行外部检查时运行的可执行文件

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<command> 是要运行的外部命令。
```

传递给命令的参数如下：

`<proxy_address>` `<proxy_port>` `<server_address>` `<server_port>`

`<proxy_address>` 和 `<proxy_port>` 由首个 IPv4、IPv6 或 Unix 套接字类型的监听器推导得出。若监听器为 Unix 套接字，则代理地址（proxy_address）为套接字路径，`<proxy_port>` 的值为字符串 "NOT_USED"。在后端段中，无法确定监听器，因此 `<proxy_address>` 和 `<proxy_port>` 的值均为字符串 "NOT_USED"。

部分值也可通过环境变量提供。

环境变量：

```text
HAPROXY_PROXY_ADDR      第一个 bind 地址（若可用）；不适用时为空，例如在 "backend" 段中。

HAPROXY_PROXY_ID        后端 ID。

HAPROXY_PROXY_NAME      后端名称。

HAPROXY_PROXY_PORT      第一个 bind 端口（若可用）；不适用时为空，例如在 "backend" 段中或使用 UNIX 套接字时。

HAPROXY_SERVER_ADDR     服务器地址。

HAPROXY_SERVER_CURCONN  服务器当前连接数。

HAPROXY_SERVER_ID       服务器 ID。

HAPROXY_SERVER_MAXCONN  服务器最大连接数。

HAPROXY_SERVER_NAME     服务器名称。

HAPROXY_SERVER_PORT     服务器端口（若可用）；UNIX 套接字时为空。

HAPROXY_SERVER_SSL      未使用 SSL 时为 "0"，使用时为 "1"。

HAPROXY_SERVER_PROTO    服务器使用的协议，可为 "cli"（haproxy CLI）、"syslog"（syslog TCP 服务器）、
                        "peers"（peers TCP 服务器）、"h1"（HTTP/1.x 服务器）、"h2"（HTTP/2 服务器）
                        或 "tcp"（任何其他 TCP 服务器）。

PATH                    执行命令时使用的 PATH 环境变量，可通过 "external-check path" 设置。
```

如果执行的命令退出状态为零，则认为检查通过；否则认为检查失败。

示例：

```text
external-check command /bin/true
```

另请参阅："external-check"、"option external-check"、"external-check path"

<a id="entry-4-2-external-check-path"></a>

**`external-check path <path>`**

```haproxy
external-check path <path>
```

运行外部检查时所使用的 PATH 环境变量的值

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<path> 是执行外部命令时使用的路径。
```

默认路径为空字符串。

示例：

```text
external-check path "/usr/bin:/bin"
```

另请参阅："external-check"、"option external-check"、"external-check command"

<a id="entry-4-2-force-be-switch"></a>

**`force-be-switch { if | unless } <condition>`**

```haproxy
force-be-switch { if | unless } <condition>
```

允许内容切换选择已禁用或未发布的后端实例。此规则可供管理员在将服务对外暴露前，用于测试流量。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| no

另请参阅："disabled"

<a id="entry-4-2-filter"></a>

**`filter <name> [param*]`**

```haproxy
filter <name> [param*]
```

在附加到代理的过滤器列表中添加过滤器 `<name>`。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| yes

参数：

```text
<name>     是过滤器名称。官方支持的过滤器见第 9 节。

<param*>   是过滤器 <name> 接受的参数列表，其解析由过滤器负责。
           所有支持的参数详情见相应过滤器的文档（第 9 节）。
```

同一代理可多次使用过滤器行。如需，同一过滤器可被多次引用。

示例：

```text
listen
  bind *:80

  filter trace name BEFORE-HTTP-COMP
  filter compression
  filter trace name AFTER-HTTP-COMP

  compression algo gzip
  compression offload

  server srv1 192.168.0.1:80
```

另请参阅：[第 9 节](/zh/haproxy/filters/)。

<a id="entry-4-2-fullconn"></a>

**`fullconn <conns>`**

```haproxy
fullconn <conns>
```

指定后端负载达到多少时，服务器将达到最大连接数

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<conns>   是让服务器使用最大连接数时所需的后端连接数。
```

当服务器配置了 "maxconn" 参数时，表示其并发连接数将不会超过该值。此外，若同时配置了 "minconn" 参数，则表示该限制为动态值，随后端负载变化而调整。此时，服务器将始终至少接受 `<minconn>` 个连接，且不会超过 `<maxconn>` 个连接，当后端并发连接数低于 `<conns>` 时，该限制将在两个数值之间动态调整。这使得在正常负载下可限制服务器负载，而在重要负载时可适度提升负载能力，同时在异常负载情况下避免服务器过载。

由于很难准确设置该值，HAProxy 会自动将其设为所有可能转向此后端的前端（基于 "use_backend" 和 "default_backend" 规则）的 maxconns 之和的 10%。因此，可以安全地不显式设置该值。然而，涉及动态名称的 "use_backend" 不会被计入，因为无法判断其是否可能匹配。

示例：

```shell
# The servers will accept between 100 and 1000 concurrent connections each
# and the maximum of 1000 will be reached when the backend reaches 10000
# connections.
backend dynamic
   fullconn   10000
   server     srv1   dyn1:80 minconn 100 maxconn 1000
   server     srv2   dyn2:80 minconn 100 maxconn 1000
```

另请参阅：“maxconn”、“server”

<a id="entry-4-2-guid"></a>

**`guid <string>`**

```haproxy
guid <string>
```

为该代理指定一个区分大小写的全局唯一 ID。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| yes

`<string>` 必须在所有 HAProxy 配置中针对每种对象类型保持唯一。格式未作限定，以允许用户自行选择命名策略。唯一限制是其长度不得超过 127 个字符。所有字母数字字符以及 '.'、':'、'-' 和 '\_' 均为有效字符。参见“shm-stats-file”。

<a id="entry-4-2-hash-balance-factor"></a>

**`hash-balance-factor <factor>`**

```haproxy
hash-balance-factor <factor>
```

指定有界负载一致性哈希的均衡因子

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| no \| yes

参数：

```text
<factor> 控制发送到服务器的最大并发请求数，表示为所有活跃服务器平均并发请求数的百分比。
```

为使用 "hash-type consistent" 的服务器指定 "hash-balance-factor" 可启用一种算法，该算法可防止任一服务器在短时间内接收过多请求，即使某些哈希桶接收的请求远多于其他桶。将 `<factor>` 设置为 0（默认值）可禁用此功能。否则，`<factor>` 必须为大于 100 的百分比。例如，若 `<factor>` 为 150，则任一服务器的负载不得超过平均负载的 1.5 倍。若使用服务器权重，将予以尊重。

如果首选服务器被排除，算法将根据请求哈希选择另一台服务器，直至找到具有额外容量的服务器。较高的 `<factor>` 会导致服务器间负载不平衡程度增加，而较低的 `<factor>` 意味着平均需检查的服务器数量更多，从而影响性能。合理的取值范围为 125 至 200。

此设置也由“balance random”使用，后者内部依赖一致性哈希机制。

另请参阅：“balance” 和 “hash-type”。

<a id="entry-4-2-hash-preserve-affinity"></a>

**`hash-preserve-affinity { always | maxconn | maxqueue }`**

```haproxy
hash-preserve-affinity { always | maxconn | maxqueue }
```

指定在服务器已饱和或队列已满时，使用哈希负载均衡将流分配至服务器的方法。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

以下值可以指定：

    - "always"：这是默认策略。无论服务器当前是否饱和，都基于哈希将流
                   分配给服务器。

    - "maxconn"：选用时，已设置 "maxconn" 且当前已饱和的服务器将被跳过，
                   并沿哈希环选取另一台服务器。这对未设置 "maxconn" 的服务
                   器没有影响。若所有服务器均已饱和，请求将被排入哈希环中
                   位于初始选定服务器之前的最后一台服务器的队列。

    - "maxqueue"：选用时，已设置 "maxconn"、"maxqueue" 为非零值（受限队列
                   大小）且当前队列已满的服务器将被跳过。并沿哈希环选取另一
                   台服务器。这对未同时设置 "maxconn" 和 "maxqueue" 的服务
                   器没有影响。

另请参阅："maxconn"、"maxqueue"、"hash-balance-factor"

<a id="entry-4-2-hash-type"></a>

**`hash-type <method> <function> <modifier>`**

```haproxy
hash-type <method> <function> <modifier>
```

指定用于将哈希映射到服务器的方法

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<method> 是从 <function> 计算的哈希中选择服务器的方法：

  map-based   哈希表是包含所有存活服务器的静态数组。哈希分布十分平滑，且考虑权重，
              但服务器上线期间的权重变更会被忽略，因此不支持慢启动。
              由于按数组位置选择服务器，服务器数量变化时大多数映射会改变。
              服务器上线、离线或新增时，大多数连接被重新分配到不同服务器，这对缓存等场景可能不便。

  consistent  哈希表是树，每台服务器在树中出现多次。在树中查找哈希键，选择最接近的服务器。
              此哈希是动态的，支持服务器上线期间更改权重，因而兼容慢启动。
              服务器上线或离线时，仅移动其关联关系；新增服务器时，仅重新分配少量映射，十分适合缓存。
              但其原理决定了分布不会十分平滑，有时需调整服务器权重或 ID 以改善均衡。
              要在多个负载均衡器上得到相同分布，所有服务器必须具有完全相同的 ID。
              注意：未指定哈希函数时，一致性哈希使用 sdbm 和 avalanche。

<function> 是要使用的哈希函数：

   sdbm   最初为 sdbm 数据库库设计，该库是 ndbm 的公有领域重新实现。
          此函数擅长打散位，改善键的分布并减少分裂，也是一种分布良好的通用哈希函数。
          但服务器总权重为 64 的倍数时，使用 avalanche 修饰符可能有帮助。

   djb2   多年前由 Dan Bernstein 在 comp.lang.c 首次提出。
          研究表明，某些工作负载下分布优于 sdbm。通常适合文本输入，
          但仅包含数值的输入或服务器总权重为 33 的倍数时，性能可能极差，除非同时使用 avalanche。

   wt6    过去测试其他函数时为 HAProxy 设计。分布不如其他函数平滑，
          但对输入数据集或服务器数量远不那么敏感。
          一致性哈希或对源 IP 地址、URL 参数中的访客标识符等数值数据计算哈希时，
          可作为 sdbm+avalanche 或 djb2+avalanche 的替代方案。

   crc32  Ethernet、gzip、PNG 等使用的常见 CRC32 实现。
          比其他函数慢，但可能提供更好的分布或更难预测的结果，尤其用于字符串时。

   none   不对键计算哈希，直接将键作为哈希值。
          适合先用转换器自行计算哈希，再让 haproxy 直接使用结果。
          若键尚未为字符串，先将其转换为字符串，再解析为整数，以该值作为键。
          某些输入键类型可能不适用，例如 IP 地址。

<modifier> 指定对键计算哈希后应用的可选方法：

   avalanche   表示不直接使用上述函数的原始结果，而先应用 4 字节的完整雪崩哈希。
               目的是混合前一个哈希得到的位，避免输入仅包含有限数值，
               或服务器数量为哈希某个组成部分的倍数时产生不良影响（SDBM 为 64，DJB2 为 33）。
               启用后，结果通常更难预测，但不如原始函数平滑。某些工作负载可能需要测试。
               此哈希是 Bob Jenkins 提出的众多算法之一。
```

默认哈希类型为“基于映射”（map-based），适用于大多数使用场景。默认函数为“sdbm”，函数的选择应基于被哈希值的取值范围。

另请参阅：“balance”、“hash-balance-factor”、“hash-preserve-affinity”、“server”

<a id="entry-4-2-http-after-response"></a>

**`http-after-response <action> <options...> [ { if | unless } <condition> ]`**

```haproxy
http-after-response <action> <options...> [ { if | unless } <condition> ]
```

对所有第 7 层响应（服务器、应用程序/服务及内部响应）的访问控制。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes(!) \| yes \| yes \| yes

第 7 层处理中，`http-after-response` 语句定义了一组规则。这些规则在前端、监听或后端段中按声明顺序进行评估。由于这些规则作用于响应，因此先应用后端规则，再应用前端规则。任何规则均可选择性地跟随一个基于 ACL 的条件，此时仅当该条件为真时才进行评估。

与 http-response 规则不同，此类规则适用于所有响应，包括服务器响应以及 HAProxy 生成的所有响应。这些规则在响应分析结束时进行评估，位于数据转发阶段之前。

条件在动作执行前进行评估，且该动作仅执行一次。因此，即使某个动作改变了作为条件一部分的元素，也不会造成问题。这也意味着多个动作可以依赖同一条件，只要首个改变条件评估结果的动作执行后，其余动作便会自动隐式禁用。例如，当变量为空时，从多个来源为其赋值，即采用此机制。每个实例中对“http-after-response”语句的数量无限制。

在语法中，“http-after-response”之后的第一个关键字是规则的动作，可选地后接该动作所需的若干参数。支持的动作及其相应语法详见 [第 4.3 节](/zh/haproxy/proxies/#section-4-3) “动作”（请查找标记为“HTTP Aft”的动作）。

该指令仅在命名的 defaults 段中可用，不可用于匿名段。在关联的代理段之前，将先评估 defaults 段中定义的规则。为避免歧义，在此情况下，同一 defaults 段不可同时被具备前端能力的代理和具备后端能力的代理使用。这意味着，listen 段不可使用定义了此类规则的 defaults 段。

请注意：在请求解析早期阶段产生的错误由多路复用器在较低层级处理，早于任何 HTTP 分析阶段。因此，这些错误不会触发 http-after-response 规则集的评估。

示例：

```text
http-after-response set-header Strict-Transport-Security "max-age=31536000"
http-after-response set-header Cache-Control "no-store,no-cache,private"
http-after-response set-header Pragma "no-cache"

```

<a id="entry-4-2-http-check-comment"></a>

**`http-check comment <string>`**

```haproxy
http-check comment <string>
```

为后续的 http-check 规则定义注释，若该规则执行失败，将在日志中报告。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<string>  是后续 http-check 规则失败时添加到日志中的注释消息。
```

仅适用于 connect、send 和 expect 规则。可用于生成用户友好的错误报告。

另请参阅：“option httpchk”、“http-check connect”、“http-check send”和“http-check expect”。

<a id="entry-4-2-http-check-connect"></a>

**`http-check connect [default] [port <expr>] [addr <ip>] [send-proxy]`**

```haproxy
http-check connect [default] [port <expr>] [addr <ip>] [send-proxy]
                   [via-socks4] [ssl] [sni <sni>] [alpn <alpn>] [linger]
                   [proto <name>] [comment <msg>]
```

打开一个新连接以执行 HTTP 健康检查

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
comment <msg>  定义规则求值失败时报告的消息。

default      使用 server 行的默认选项进行健康检查，仅使用未被重新定义的服务器选项。

port <expr>  未设置时，使用检查端口或服务器端口，指定 HAProxy 连接的位置。
             <port> 必须为 1 到 65535 的有效 TCP 端口整数，或样本提取表达式。

addr <ip>    定义健康检查使用的 IP 地址。

send-proxy   发送 PROXY 协议字符串。

via-socks4   通过上游 socks4 代理执行出站健康检查。

ssl          打开加密连接。

sni <sni>    指定通过 SSL 执行健康检查时使用的 SNI。

alpn <alpn>  定义通过 ALPN 通告的协议。协议列表由逗号分隔的协议名称组成，
             例如 "h2,http/1.1"。未设置时使用服务器的 ALPN。

proto <name> 强制此连接使用指定的多路复用器协议，必须为可在后端侧使用的 HTTP 复用协议。
             可用协议列表通过 haproxy -vv 报告。

linger       干净地关闭连接，而非仅发送 RST。
```

与 tcp-check 健康检查类似，可配置用于执行 HTTP 健康检查的连接。该指令还应用于描述涉及多个请求/响应交互的场景，这些交互可能在不同端口上进行，或涉及不同的服务器。

当服务器行中未配置 TCP 端口，且未使用 server port 指令时，http-check 序列的第一步必须使用 "http-check connect" 指定端口。

在 http-check 规则集中，必须包含一个 'connect' 规则，且规则集必须以 'connect' 规则开头。此举旨在确保管理员清楚了解其操作意图。

当连接必须启动规则集时，仍可由 set-var、unset-var 或 comment 规则先行。

示例：

```shell
# check HTTP and HTTPs services on a server.
# first open port 80 thanks to server line port directive, then
# tcp-check opens port 443, ciphered and run a request on it:
option httpchk

http-check connect
http-check send meth GET uri / ver HTTP/1.1 hdr host haproxy.1wt.eu
http-check expect status 200-399
http-check connect port 443 ssl sni haproxy.1wt.eu
http-check send meth GET uri / ver HTTP/1.1 hdr host haproxy.1wt.eu
http-check expect status 200-399

server www 10.0.0.1 check port 80
```

另请参阅：“option httpchk”、“http-check send”、“http-check expect”

<a id="entry-4-2-http-check-disable-on-404"></a>

**`http-check disable-on-404`**

```haproxy
http-check disable-on-404
```

在健康检查返回 HTTP/404 响应时启用维护模式

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

当启用此选项时，返回 HTTP 状态码 404 的服务器将不再参与后续的负载均衡，但仍会接收持久连接。这为 Web 管理员提供了一种非常便捷的服务器优雅关闭方式。需要注意的是，处于此模式下检测到失败的服务器不会触发告警，仅生成通知。若服务器再次返回 2xx 或 3xx 响应，将立即被重新加入服务器池。统计信息页面中，该服务器的状态显示为“NOLB”。请注意，此选项仅在与“httpchk”选项配合使用时生效。若与“http-check expect”选项一同使用，则本选项具有更高优先级，即 404 响应仍被视为软停止。此外，已停止的服务器即使返回 404，仍将持续处于停止状态。此选项仅对运行中的服务器进行评估。

另请参阅：“option httpchk” 和 “http-check expect”。

<a id="entry-4-2-http-check-expect"></a>

**`http-check expect [min-recv <int>] [comment <msg>]`**

```haproxy
http-check expect [min-recv <int>] [comment <msg>]
                  [ok-status <st>] [error-status <st>] [tout-status <st>]
                  [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                  [!] <match> <pattern>
```

使 HTTP 健康检查考虑响应内容或特定状态码

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
comment <msg>  定义规则求值失败时报告的消息。

min-recv  是可选参数，定义对当前 expect 规则求值所需的最少数据量。
          接收字节数低于此限制时，检查等待更多数据。可用于消除匹配规则的歧义，
          或避免对已知尚不完整的内容执行昂贵的正则匹配。
          使用精确字符串时，取字符串长度与此参数的较小值。
          设为 -1 时忽略此参数；expect 规则不匹配时，检查等待更多数据。
          设为 0 时，求值结果始终是确定的。

ok-status <st>     是可选参数，在 expect 规则求值成功且为 tcp-check 规则集的最后一条规则时，
                   设置检查状态。支持 "L7OK"、"L7OKC"、"L6OK" 和 "L4OK"：
                     - L7OK : 第 7 层检查通过
                     - L7OKC: 第 7 层检查有条件通过，将服务器设为 NOLB 状态
                     - L6OK : 第 6 层检查通过
                     - L4OK : 第 4 层检查通过
                   默认使用 "L7OK"。

error-status <st>  是可选参数，在 expect 规则求值发生错误时设置检查状态。
                   支持 "L7OKC"、"L7RSP"、"L7STS"、"L6RSP" 和 "L4CON"：
                     - L7OKC: 第 7 层检查有条件通过，将服务器设为 NOLB 状态
                     - L7RSP: 第 7 层响应无效：协议错误
                     - L7STS: 第 7 层响应错误，例如 HTTP 5xx
                     - L6RSP: 第 6 层响应无效：协议错误
                     - L4CON: 第 1-4 层连接问题
                   默认使用 "L7RSP"。

tout-status <st>   是可选参数，在 expect 规则求值超时时设置检查状态。
                   支持 "L7TOUT"、"L6TOUT" 和 "L4TOUT"：
                     - L7TOUT: 第 7 层（HTTP/SMTP）超时
                     - L6TOUT: 第 6 层（SSL）超时
                     - L4TOUT: 第 1-4 层超时
                   默认使用 "L7TOUT"。

on-success <fmt>   是可选参数，在 expect 规则求值成功且为 tcp-check 规则集的最后一条规则时，
                   自定义日志中报告的信息消息。<fmt> 为自定义日志格式字符串（参见第 8.2.6 节）。

on-error <fmt>     是可选参数，在 expect 规则求值发生错误时，自定义日志中报告的信息消息。
                   <fmt> 为自定义日志格式字符串（参见第 8.2.6 节）。

status-code <expr> 是可选参数，设置成功或错误时在日志中报告的检查状态码。
                   <expr> 是标准 HAProxy 表达式，由样本提取后接若干转换器构成。

<match>   指定如何在响应中查找特定模式，可为 "status"、"rstatus"、"hdr"、"fhdr"、"string" 或 "rstring"。
          关键字前可加感叹号（"!"）来反转匹配。感叹号与关键字之间允许空格。
          所支持关键字的更多详情见下文。

<pattern> 是要查找的模式，可为字符串、正则表达式或包含多个参数的复杂模式。
          字符串模式包含空格时，必须使用通常的反斜杠（'\'）转义。
```

默认情况下，“option httpchk”认为响应状态码为 2xx 和 3xx 时有效，其余状态码为无效。当使用“http-check expect”时，它将定义何为有效或无效。一个后端中仅支持一条“http-check”语句。若服务器无响应或超时，检查显然会失败。可用的匹配项包括：

```text
status <codes>:  解析 <codes> 字符串，检查其中的状态码。
                  必须为逗号分隔的状态码或状态码范围列表。响应状态码匹配任一状态码，
                  或落入任一范围时，健康检查响应视为有效。
                  "status" 前加 "!" 时，状态码匹配则将响应视为无效。

rstatus <regex>: 对 HTTP 状态码进行正则表达式检查。响应状态码匹配表达式时，健康检查响应视为有效。
                  "rstatus" 前加 "!" 时，状态码匹配则将响应视为无效。主要用于检查多个状态码。

hdr  { name | name-lf } [ -m <meth> ] <name>
     [ { value | value-lf } [ -m <meth> ] <value>:
                  对 HTTP 响应头检查指定的头模式。名称模式为必需项，值模式为可选项。
                  未指定值模式时，仅检查头是否存在。<meth> 是应用于头名称或头值的匹配方法。
                  支持 "str"（精确匹配）、"beg"（前缀匹配）、"end"（后缀匹配）、
                  "sub"（子串匹配）或 "reg"（正则匹配），未指定时使用精确匹配。
                  使用 "name-lf" 时，将 <name> 作为自定义日志格式字符串求值（参见第 8.2.6 节）；
                  使用 "value-lf" 时，将 <value> 作为日志格式字符串求值。
                  这些参数不能与正则匹配方法组合。头值被视为逗号分隔的列表。
                  注意，头名称匹配不区分大小写。

fhdr { name | name-lf } [ -m <meth> ] <name>
     [ { value | value-lf } [ -m <meth> ] <value>:
                  对 HTTP 响应头检查指定的完整头模式，与 "hdr" 完全相同，
                  但检查完整的头值，不将逗号视为分隔符。

string <string>: 检查 HTTP 响应体中的精确字符串匹配。
                  响应体包含此字符串时，健康检查响应视为有效。
                  "string" 前加 "!" 时，响应体包含此字符串则将响应视为无效。
                  可用于检查动态页面末尾必须出现的词，或在检查页面出现特定错误（如堆栈跟踪）时检测故障。

rstring <regex>: 对 HTTP 响应体进行正则表达式检查。
                  响应体匹配表达式时，健康检查响应视为有效。
                  "rstring" 前加 "!" 时，响应体匹配则将响应视为无效。
                  可用于检查动态页面末尾必须出现的词，或在检查页面出现特定错误（如堆栈跟踪）时检测故障。

string-lf <fmt>: 在 HTTP 响应体中匹配自定义日志格式字符串（参见第 8.2.6 节）。
                  响应体包含对 <fmt> 按日志格式规则求值得到的字符串时，健康检查响应视为有效。
                  前加 "!" 时，响应体包含此字符串则将响应视为无效。
```

请注意，响应大小将受到全局 "tune.bufsize" 选项的限制，该选项默认值为 16384 字节。因此，使用 "string" 或 "rstring" 时，过大的响应可能不包含必需的模式。若确实需要处理大响应，可通过设置全局变量更改默认最大大小。但需注意，解析非常大的响应可能会浪费部分 CPU 周期，尤其是在使用正则表达式时，且始终建议将检查聚焦于较小的资源。

在 http-check 规则集中，最后一个 expect 规则可以是隐式的。如果在最后一个 "http-check send" 之后未指定 expect 规则，则会定义一个隐式的 expect 规则，用于匹配 2xx 或 3xx 状态码。这意味着，即使完全未设置 "http-check" 规则，仅设置了 "option httpchk" 时，该规则同样会被定义。

最后，如果将“http-check expect”与“http-check disable-on-404”结合使用，则当服务器响应 404 时，后者具有优先权。

示例：

```shell
# only accept status 200 as valid
http-check expect status 200,201,300-310

# be sure a sessid coookie is set
http-check expect hdr name "set-cookie" value -m beg "sessid="

# consider SQL errors as errors
http-check expect ! string SQL\ Error

# consider status 5xx only as errors
http-check expect ! rstatus ^5

# check that we have a correct hexadecimal tag before /html
http-check expect rstring <!--tag:[0-9a-f]*--></html>
```

另请参阅：“option httpchk”、“http-check connect”、“http-check disable-on-404”和“http-check send”。

<a id="entry-4-2-http-check-send"></a>

**`http-check send [meth <method>] [{ uri <uri> | uri-lf <fmt> }>] [ver <version>]`**

```haproxy
http-check send [meth <method>] [{ uri <uri> | uri-lf <fmt> }>] [ver <version>]
                [hdr <name> <fmt>]* [{ body <string> | body-lf <fmt> }]
                [comment <msg>]
```

在 HTTP 健康检查发送的请求中添加可能的头字段列表和/或请求体。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
comment <msg>  定义规则求值失败时报告的消息。

meth <method>  是请求使用的可选 HTTP 方法。未设置时使用 "OPTIONS"，因为该方法通常处理开销较低，
               且易于从日志中过滤掉。可使用任何方法，但不建议自行创建非标准方法。

uri <uri>      是可选参数，将 HTTP 请求引用的 URI 设为字符串 <uri>。
               默认值为 "/"，几乎任何服务器均默认可访问；也可改为任何其他 URI，允许查询字符串。

uri-lf <fmt>   是可选参数，使用自定义日志格式 <fmt>（参见第 8.2.6 节）设置 HTTP 请求引用的 URI。
               默认值为 "/"，几乎任何服务器均默认可访问；也可改为任何其他 URI，允许查询字符串。

ver <version>  是可选的 HTTP 版本字符串，默认值为 "HTTP/1.0"。
               某些服务器在 HTTP 1.0 下可能行为异常，改用 HTTP/1.1 有时会有帮助。
               注意，HTTP/1.1 要求必须提供 Host 字段，可使用 "hdr" 参数添加。

hdr <name> <fmt>  添加 HTTP 头，名称由 <name> 指定，值由 <fmt> 定义，
                  遵循第 8.2.6 节所述的自定义日志格式规则。

body <string>  将 <string> 定义的消息体添加到 HTTP 健康检查发送的请求中。
               定义此项时，自动添加 "Content-Length" 头。

body-lf <fmt>  将自定义日志格式 <fmt>（参见第 8.2.6 节）定义的消息体添加到 HTTP 健康检查发送的请求中。
               定义此项时，自动添加 "Content-Length" 头。
```

除了由 "option httpchk" 指令定义的请求行外，以下方式是向 HTTP 健康检查请求中添加头字段并可选地添加请求体的正确方法。若定义了请求体，则会自动添加相应的 "Content-Length" 头字段。因此，在 "http-check send" 提供的请求中，不应包含该头字段或 "Transfer-encoding" 头字段，否则将被忽略。在 "option httpchk" 行中版本字符串后添加头字段的旧方法现已弃用。

此外，“http-check send” 不支持 HTTP 持久连接。请注意，除非通过 hdr 条目已配置 Connection 头，否则它会自动附加一个 "Connection: close" 头。

请注意，当 Host 头和请求授权信息均被定义时，二者会自动同步。这意味着在发送 HTTP 请求时，若在请求中插入 Host 头，则请求授权信息会相应更新。因此，若发现 Host 头值覆盖了配置的请求授权信息，无需感到意外。

请注意，目前在 HTTP/1.1 及以上版本的请求中，不会自动添加 Host 头。应显式添加。

另请参阅：“option httpchk”、“http-check send-state”和“http-check expect”。

<a id="entry-4-2-http-check-send-state"></a>

**`http-check send-state`**

```haproxy
http-check send-state
```

启用 HTTP 健康检查时发送状态头

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

当启用此选项时，HAProxy 会始终向每个服务器发送一个特殊头字段 "X-Haproxy-Server-State"，其中包含一组参数，用于指示 HAProxy 对各服务器的当前状态判断。例如，当服务器在未访问 HAProxy 的情况下被操作时，管理员可借此确认 HAProxy 是否仍认为该服务器处于运行状态，或该服务器是否为某服务器组中的最后一个成员。

头由分号分隔的字段组成，第一个字段为一个单词（"UP"、"DOWN"、"NOLB"），后接状态转换前的有效检查数与总检查数（格式与统计信息界面中显示的一致，如 2/3）。后续字段格式为 "`<variable>`=`<value>`"，以任意顺序表示统计信息界面中可用的某些值：- 变量 "address"，包含后端服务器的地址。该值对应服务器声明中的 `<address>` 字段。对于 Unix 域套接字，其值为 "unix"。

    - 变量 "port"，包含后端服务器的端口。对应服务器声明中的 `<port>`
      字段。对于 Unix 域套接字，其值为 "unix"。

    - 变量 "name"，包含后端名称，后接斜杠（"/"）和服务器名称。当一台
      服务器在多个后端中接受检查时，可以使用该变量。

    - 变量 "node"，包含 HAProxy 节点的名称，即全局 "node" 变量中设置的
      值；未指定时使用系统主机名。

    - 变量 "weight"，指示服务器的权重，后接斜杠（"/"）和服务器组的总
      权重（仅统计可用的服务器）。这有助于了解当该服务器发生故障时，
      是否有其他服务器可用于承担负载。

    - 变量 "scur"，指示服务器上当前的并发连接数，后接斜杠（"/"）和同一
      后端中所有服务器的连接总数。

    - 变量 "qcur"，指示服务器队列中当前的请求数。

应用服务器接收到的头示例：

```shell
>>>  X-Haproxy-Server-State: UP 2/3; name=bck/srv2; node=lb1; weight=1/2; \
       scur=13/22; qcur=0
```

另请参阅：“option httpchk”、“http-check disable-on-404” 和 “http-check send”。

<a id="entry-4-2-http-check-set-var"></a>

**`http-check set-var(<var-name>[,<cond>...]) <expr>`**

```haproxy
http-check set-var(<var-name>[,<cond>...]) <expr>
http-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
```

此操作用于设置变量的内容。变量在行内声明。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<var-name>   是变量名称。仅可使用 "proc"、"sess" 和 "check" 作用域。详情见第 2.8 节的变量说明。

 <cond>      是一组条件，必须全部为真才会实际设置变量（例如 "ifnotempty"、"ifgt" 等）。
             所有可用条件见 set-var 转换器的说明。

 <expr>      是样本提取表达式，其后可接转换器。

 <fmt>       是以自定义日志格式表示的值（参见第 8.2.6 节的自定义日志格式）。
```

示例：

```text
http-check set-var(check.port) int(1234)
http-check set-var-fmt(check.port) "name=%H"

```

<a id="entry-4-2-http-check-unset-var"></a>

**`http-check unset-var(<var-name>)`**

```haproxy
http-check unset-var(<var-name>)
```

释放变量在其作用域内的引用。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<var-name>   是变量名称。仅可使用 "proc"、"sess" 和 "check" 作用域。详情见第 2.8 节的变量说明。
```

示例：

```text
http-check unset-var(check.port)

```

<a id="entry-4-2-http-error-status"></a>

**`http-error status <code> [content-type <type>]`**

```haproxy
http-error status <code> [content-type <type>]
           [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

               file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
           [ hdr `<name>` `<fmt>` ]*

定义自定义错误消息，用于替代 HAProxy 生成的错误信息。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
status <code>        是 HTTP 状态码，必须指定。HAProxy 目前可生成的状态码为
                     200、400、401、403、404、405、407、408、410、413、414、425、429、431、500、501、502、503 和 504。

content-type <type>  是响应内容类型，例如 "text/plain"。
                     配置了 errorfile 或负载为空时，忽略此参数，应省略；其他情况下必须定义。

default-errorfiles   重置当前代理此前为状态 <code> 定义的错误消息。
                     用于后端时，使用前端定义的错误消息（若有）；用于前端时，使用默认错误消息。

errorfile <file>     指定包含完整 HTTP 响应的文件。建议在文件名末尾添加 ".http"，
                     避免与 HTML 错误页面混淆；还应使用绝对路径，因为文件在执行 chroot 之前读取。

errorfiles <name>    指定从哪个 http-errors 段导入状态码 <code> 对应的错误消息。
                     未找到此类消息时，使用代理的错误消息。

file <file>          指定用作响应负载的文件。文件非空时，必须使用 "content-type" 参数设置其内容类型；
                     否则忽略任何 "content-type" 参数。<file> 视为原始字符串。

string <str>         指定用作响应负载的原始字符串，必须始终使用 "content-type" 参数设置内容类型。

lf-file <file>       指定用作响应负载的文件。文件非空时，必须使用 "content-type" 参数设置其内容类型；
                     否则忽略任何 "content-type" 参数。
                     <file> 按自定义日志格式求值（参见第 8.2.6 节）。

lf-string <str>      指定用作响应负载的日志格式字符串，必须始终使用 "content-type" 参数设置内容类型。

hdr <name> <fmt>     添加 HTTP 响应头，名称由 <name> 指定，值由 <fmt> 定义，
                     遵循自定义日志格式规则（参见第 8.2.6 节）。使用 errorfile 时忽略此参数。
```

此指令可用于替代 "errorfile"，以定义自定义错误消息。与 "errorfile" 指令相同，它用于处理 HAProxy 检测并返回的错误。若定义了 errorfile，则 HAProxy 启动时会对其进行解析，且必须符合 HTTP 标准。生成的响应不得超过配置的缓冲区大小（BUFFSIZE），否则将返回内部错误。最后，若考虑使用某些 http-after-response 规则来重写这些错误，应确保预留的缓冲区空间可用（参见 "tune.maxrewrite"）。

配置文件与之同时读取并保留在内存中。因此，即使进程已执行 chroot，错误仍会持续返回，且在进程运行期间不会考虑任何文件变更。

请注意：在请求解析早期阶段产生的 400/408/500 错误由多路复用器在较低层级处理。此层级不支持自定义格式化。因此，仅支持使用 "errorfile" 指令定义的静态错误消息。然而，此限制仅存在于请求头解析期间或两次事务之间。

另请参阅：“errorfile”、“errorfiles”、“errorloc”、“errorloc302”、“errorloc303”以及 [第 12.4 节](/zh/haproxy/other-sections/#section-12-4) 关于 http-errors 的内容。

<a id="entry-4-2-http-request"></a>

**`http-request <action> [options...] [ { if | unless } <condition> ]`**

```haproxy
http-request <action> [options...] [ { if | unless } <condition> ]
```

第 7 层请求的访问控制

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes(!) \| yes \| yes \| yes

第 7 层处理中，`http-request` 语句用于定义一组规则。这些规则在前端、监听或后端段中按声明顺序进行评估。每条规则可选择性地跟随一个基于 ACL 的条件，此时仅当该条件求值为真时，规则才会被评估。

条件在动作执行前进行评估，且该动作仅执行一次。因此，即使某个动作改变了作为条件一部分的元素，也不会造成问题。这也意味着多个动作可以依赖同一条件，只要首个改变条件评估结果的动作执行后，其余动作便会自动隐式禁用。例如，当变量为空时，从多个来源为其赋值，即采用此机制。每个实例中“http-request”语句的数量无限制。

在 "http-request" 语法中，首个关键字为规则的动作，可选地后接该动作所需的若干参数。支持的动作及其对应语法详见 [第 4.3 节](/zh/haproxy/proxies/#section-4-3) “动作”（请查找标记为“HTTP Req”的动作）。

该指令仅在命名的 defaults 段中可用，不可用于匿名段。在关联的代理段之前，将先评估 defaults 段中定义的规则。为避免歧义，在此情况下，同一 defaults 段不可同时被具备前端能力的代理和具备后端能力的代理使用。这意味着，listen 段不可使用定义了此类规则的 defaults 段。

示例：

```text
acl nagios src 192.168.129.3
acl local_net src 192.168.0.0/16
acl auth_ok http_auth(L1)

http-request allow if nagios
http-request allow if local_net auth_ok
http-request auth realm Gimme if local_net auth_ok
http-request deny
```

示例：

```text
acl key req.hdr(X-Add-Acl-Key) -m found
acl add path /addacl
acl del path /delacl

acl myhost hdr(Host) -f myhost.lst

http-request add-acl(myhost.lst) %[req.hdr(X-Add-Acl-Key)] if key add
http-request del-acl(myhost.lst) %[req.hdr(X-Add-Acl-Key)] if key del
```

示例：

```text
acl value  req.hdr(X-Value) -m found
acl setmap path /setmap
acl delmap path /delmap

use_backend bk_appli if { hdr(Host),map_str(map.lst) -m found }

http-request set-map(map.lst) %[src] %[req.hdr(X-Value)] if setmap value
http-request del-map(map.lst) %[src]                     if delmap
```

另请参阅：“stats http-request”，[第 12.2 节](/zh/haproxy/other-sections/#section-12-2) 关于 userlists 的说明，以及 [第 7 节](/zh/haproxy/acls-and-samples/) 关于 ACL 使用的说明。

<a id="entry-4-2-http-response"></a>

**`http-response <action> <options...> [ { if | unless } <condition> ]`**

```haproxy
http-response <action> <options...> [ { if | unless } <condition> ]
```

第 7 层响应的访问控制

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes(!) \| yes \| yes \| yes

第 7 层处理中，`http-response` 语句定义了一组规则。这些规则在前端、监听或后端段中按声明顺序进行评估。由于这些规则作用于响应，因此先应用后端规则，再应用前端规则。任何规则均可选择性地跟随一个基于 ACL 的条件，此时仅当该条件求值为真时才进行评估。

条件在动作执行前进行评估，且该动作仅执行一次。因此，即使某个动作改变了作为条件一部分的元素，也不会造成问题。这也意味着多个动作可以依赖同一条件，只要首个改变条件评估结果的动作执行后，其余动作便会自动隐式禁用。例如，当变量为空时，从多个来源为其赋值，即采用此机制。每个实例中“http-response”语句的数量无限制。

在语法中，“http-response”之后的第一个关键字是规则的动作，可选地后接该动作所需的若干参数。支持的动作及其各自语法详见 [第 4.3 节](/zh/haproxy/proxies/#section-4-3)“动作”（请查找标记为“HTTP Res”的动作）。

该指令仅在命名的 defaults 段中可用，不可用于匿名段。在关联的代理段之前，将先评估 defaults 段中定义的规则。为避免歧义，在此情况下，同一 defaults 段不可同时被具备前端能力的代理和具备后端能力的代理使用。这意味着，listen 段不可使用定义了此类规则的 defaults 段。

示例：

```text
acl key_acl res.hdr(X-Acl-Key) -m found

acl myhost hdr(Host) -f myhost.lst

http-response add-acl(myhost.lst) %[res.hdr(X-Acl-Key)] if key_acl
http-response del-acl(myhost.lst) %[res.hdr(X-Acl-Key)] if key_acl
```

示例：

```text
acl value  res.hdr(X-Value) -m found

use_backend bk_appli if { hdr(Host),map_str(map.lst) -m found }

http-response set-map(map.lst) %[src] %[res.hdr(X-Value)] if value
http-response del-map(map.lst) %[src]                     if ! value
```

另请参阅：“http-request”，[第 12.2 节](/zh/haproxy/other-sections/#section-12-2) 关于 userlists 的说明以及 [第 7 节](/zh/haproxy/acls-and-samples/) 关于 ACL 使用的说明。

<a id="entry-4-2-http-reuse"></a>

**`http-reuse { never | safe | aggressive | always }`**

```haproxy
http-reuse { never | safe | aggressive | always }
```

声明空闲 HTTP 连接在请求之间如何共享

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

为避免为每个 HTTP 请求建立与后端服务器的新连接所带来的开销，HAProxy 会在使用后尽量保持这些空闲连接处于打开状态。这些连接与特定服务器相关，并存储在一个称为连接池的列表中，且根据一组共同的关键属性进行分组。后续的 HTTP 请求将触发对关联连接池中具有相同属性的兼容连接的查找，从而复用该连接，而非建立新的连接。

可通过服务器关键字 "pool-max-conn" 指定服务器上保持的空闲连接数量上限。未使用的连接将根据 "pool-purge-delay" 间隔周期性地清除。

以下连接属性用于确定空闲连接在特定请求上是否可重用：

- 源地址和目标地址
- PROXY 协议
- TOS 和 mark 套接字选项
- 连接名称，由 "pool-conn-name" 表达式求值结果确定，若该表达式不存在，则由 "sni" 表达式确定，其默认值为 "req.hdr(host),field(1,:)"，即使用入站请求的 "Host" 头字段，不包含冒号和端口号。

在某些情况下，由于额外的限制，不会执行连接查找或复用。这由通过关键字参数指定的复用策略决定：

    - "never"：空闲连接从不在会话之间共享。可以强制使用此模式，以取消从
                 defaults 段继承的其他策略，或用于故障排查。例如，某个老旧
                 的有缺陷的应用程序认为同一连接上的多个请求来自同一客户端，
                 且无法修复该应用程序时，可能需要在单个后端中禁用连接共享。
                 此类应用程序的一个例子是使用 cookie 插入且处于隧道模式的
                 旧版 HAProxy，它不检查第一个之后的任何请求。

    - "safe"：这是默认且推荐的策略。会话的第一个请求始终通过其自身的
                 连接发送，只有后续请求才可能通过其他现有连接分派。这确保
                 了在服务器于请求发送期间关闭连接的情况下，浏览器可以决定
                 静默重试。由于这完全等同于常规持久连接，因此不应有任何
                 副作用。对于使用受队头阻塞（Head-of-line blocking）影响的
                 协议（后端为 h2 或 fcgi）的连接，还有特殊处理：此时，只要
                 至少有一个流正在处理，所使用的连接就会被保留用于处理同一
                 会话的流；当不再有流处理时，连接会被释放并可以复用。

    - "aggressive"：此模式可能适用于并非所有服务器都已知、且希望大多数
                 首个请求通过现有连接交付的 Web 服务环境。此时，首个请求
                 仅通过至少被复用过一次的现有连接交付，以证明服务器正确
                 支持连接复用。只有当确定客户端能够偶尔重试失败的请求，
                 且激进连接复用的收益显著大于偶发连接故障的缺点时，才应
                 使用此模式。

    - "always"：仅当已知通往服务器的路径绝不会在释放连接后很快断开现有
                 连接时，才推荐使用此模式。它允许会话的第一个请求通过现有
                 连接发送。当后端是缓存服务器集群时，相比 "safe" 策略，这
                 可以带来显著的性能提升，因为此类组件的行为往往一致，并能
                 从连接共享中受益。在此模式下，建议保持较低的
                 "http-keep-alive" 超时，以免失效连接仍可使用。在大多数
                 情况下，这会带来与 "aggressive" 相同的性能收益，但风险
                 更高。仅当其效果优于 "aggressive" 时才应使用。

请注意，使用某些依赖连接的伪造认证机制（如 NTLM）的连接，若可能将被标记为私有，且永不共享。然而，当使用具备多路复用能力的协议，并启用大于默认“安全”策略的重用模式级别时，情况将不同，此时无法阻止连接已被共享。

决定在处理完成后是否保持空闲连接打开或关闭的规则，同样由 "tune.pool-low-fd-ratio"（默认值：20%）和 "tune.pool-high-fd-ratio"（默认值：25%）控制。这两个参数分别对应于空闲连接所占用的总文件描述符比例阈值，当超过该阈值时，HAProxy 将分别停止在响应后保持连接打开，或主动终止空闲连接。某些配置中空闲连接比例极高，可能是由于全局 "maxconn" 值过低，或前端存在大量 HTTP/2 或 HTTP/3 流量（连接数少），而后端使用 HTTP/1 连接，可能导致连接复用率下降，因为保持打开的连接过少。在此情况下，调整这些阈值或简单地提高全局 "maxconn" 值可能是有益的。

在某些罕见情况下，当主机名用于区分出站 TLS 连接（例如正向代理）且大多数请求的目标主机不同时，连接复用率会非常低。此时，在连接有机会被复用之前，系统可能已触发对使用频率较低连接的自动淘汰机制。这是因为该机制会持续测量维持服务所需的平均连接数，以避免资源耗尽。在此类场景中，将“pool-low-conn”设置为接近预期空闲连接平均数的值，有助于通过鼓励线程建立自己的连接，而非尝试选取其他线程的连接，从而减少可用连接池的收缩，保留更多连接。

如果本地托管的服务器使用单个证书（包含多个主机名或通配符）并运行多个站点，建议在“server”行上使用“no-sni-auto”而非保留对单一主机名的连接，以提升连接复用率。部分服务器可能在主机名与 SNI 之间执行过多检查，导致拒绝后续请求，因此该选项需预先验证。默认行为（“sni-auto”）旨在确保与此类服务器的兼容性，更为安全。

当显式启用线程组时，需注意空闲连接仅可在同一组内的线程之间复用。因此，组间负载不均可能导致需要更多空闲连接，从而降低复用率。可采用相同解决方案（增加全局 "maxconn" 值或提高池比例）。

另请参阅："option http-keep-alive"、"pool-conn-name"、"pool-max-conn"、"pool-purge-delay"、"server maxconn"、"sni"、"thread-groups"、"tune.pool-high-fd-ratio"、"tune.pool-low-fd-ratio"

<a id="entry-4-2-http-send-name-header"></a>

**`http-send-name-header [<header>]`**

```haproxy
http-send-name-header [<header>]
```

将服务器名称添加到请求中。使用由 `<header>` 提供的头字符串

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<header>  是用于发送服务器名称的头字符串。
```

“http-send-name-header” 语句会导致名为 `<header>` 的头字段在请求即将通过网络发送时被设置为目标服务器的名称。该头字段中任何已存在的实例均会被移除。在重试和重分派过程中，该头字段会更新，始终反映当前尝试连接的服务器。由于该头字段在连接建立过程的后期才被修改，可能对已修改的其他头字段产生意外影响。例如，与传输层头（如 connection、content-length、transfer-encoding 等）一起使用时，很可能导致向服务器发送无效请求。因此，以下头字段被禁止使用：host、content-length、transfer-encoding 和 connection。

另请参阅："server"

<a id="entry-4-2-id"></a>

**`id <value>`**

```haproxy
id <value>
```

为代理设置持久化 ID。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| yes

参数：无

为代理设置一个持久化 ID。该 ID 必须唯一且为正数。若未设置，将自动分配一个未使用的 ID。由于历史行为，除非显式设置，否则值 1 不会被使用。因此，自动分配的最小值为 2。该 ID 当前仅在统计信息中返回。

<a id="entry-4-2-ignore-persist"></a>

**`ignore-persist { if | unless } <condition>`**

```haproxy
ignore-persist { if | unless } <condition>
```

声明一个条件以忽略持久性

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

默认情况下，启用 cookie 持久性后，所有包含该 cookie 的请求将无条件保持持久性（前提是目标服务器处于运行状态）。

本节中的 "ignore-persist" 语句允许声明多种基于 ACL 的条件，当这些条件满足时，将导致请求忽略持久性。这在对静态文件请求进行负载均衡时有时很有用，因为这类请求通常不需要持久性。该功能也可用于针对特定 User-Agent 完全禁用持久性（例如，某些网络爬虫机器人）。

当满足 "if" 条件时，持久性将被忽略，或除非满足 "unless" 条件。

示例：

```text
acl url_static  path_beg         /static /images /img /css
acl url_static  path_end         .gif .png .jpg .css .js
ignore-persist  if url_static
```

另请参阅：“force-persist”、“cookie”以及 [第 7 节](/zh/haproxy/acls-and-samples/) 中关于 ACL 使用的说明。

<a id="entry-4-2-load-server-state-from-file"></a>

**`load-server-state-from-file { global | local | none }`**

```haproxy
load-server-state-from-file { global | local | none }
```

允许 HAProxy 无缝重载

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

本指令用于指定 HAProxy 从何处加载前一次运行进程保存的服务器状态文件。这样，在启动过程中、处理流量之前，新进程可以将旧状态精确地应用到服务器上，如同未发生重载一般。`load-server-state-from-file` 指令的作用是告知 HAProxy 使用哪个文件。目前，该指令仅支持两个参数：一个用于禁止加载状态，另一个用于从包含所有后端和服务器状态的文件中加载状态。状态文件可通过在统计信息套接字上执行命令 `show servers state` 并重定向输出生成。

文件格式已版本化，且非常具体。如需理解，请阅读“show servers state”命令的文档（管理指南第 9.3 章）。

参数：

```text
global     加载全局指令 "server-state-file" 指向的文件的内容。

local      若设置了 "server-state-file-name" 指令，则加载它指向的文件；
           否则以后端名称作为文件名。

none       不加载此后端的任何状态。
```

注意：默认情况下，服务器的 IP 地址在重载过程中得以保留，但可通过服务器的 "init-addr" 设置更改其顺序。这意味着通过 CLI 在运行时执行的 IP 地址变更将被保留，且若启用了状态文件，对本地解析器（例如 /etc/hosts）的任何更改可能不会产生效果。

    - 除非服务器的权重在新旧配置文件之间发生了更改，否则将沿用之前运行
      进程中的服务器权重。

示例：最小配置

      global
       stats socket /tmp/socket
       server-state-file /tmp/server_state

      defaults
       load-server-state-from-file global

      backend bk
       server s1 127.0.0.1:22 check weight 11
       server s2 127.0.0.1:22 check weight 12

然后可以运行：

```text
socat /tmp/socket - <<< "show servers state" > /tmp/server_state
```

/tmp/server_state 文件的内容应如下所示：

```shell
1
# <field names skipped for the doc example>
1 bk 1 s1 127.0.0.1 2 0 11 11 4 6 3 4 6 0 0
1 bk 2 s2 127.0.0.1 2 0 12 12 4 6 3 4 6 0 0
```

示例：最小配置

    global
     stats socket /tmp/socket
     server-state-base /etc/haproxy/states

    defaults
     load-server-state-from-file local

    backend bk
     server s1 127.0.0.1:22 check weight 11
     server s2 127.0.0.1:22 check weight 12

然后可以运行：

```text
socat /tmp/socket - <<< "show servers state bk" > /etc/haproxy/states/bk
```

/etc/haproxy/states/bk 文件内容如下：

```shell
1
# <field names skipped for the doc example>
1 bk 1 s1 127.0.0.1 2 0 11 11 4 6 3 4 6 0 0
1 bk 2 s2 127.0.0.1 2 0 12 12 4 6 3 4 6 0 0
```

另请参阅：“server-state-file”、“server-state-file-name”和“show servers state”

<a id="entry-4-2-log-global"></a>

**`log global`**

```haproxy
log global
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    [profile <prof>] <facility> [<level> [<minlevel>]]
no log
```

启用每个实例的事件和流量日志记录。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

前缀：

```text
no         用于需要清空日志记录器列表的情况，例如不希望继承默认列表时。
           此前缀不接受参数。
```

参数：

```text
global     实例日志参数与全局参数相同时使用，这是最常见的用法。
           "global" 将所有日志参数替换为 "global" 段中日志条目的参数。
           每个实例仅能使用一条 "log global" 语句，且此形式不接受其他参数。

<target>   指定日志发送位置，格式与 "global" 段的日志相同，可为：

           - IPv4 地址，可选地后接冒号（':'）和 UDP 端口。未指定时默认使用 514（标准 syslog 端口）。

           - IPv6 地址，后接冒号（':'）及可选 UDP 端口。未指定时默认使用 514（标准 syslog 端口）。

           - UNIX 域套接字的文件系统路径。需考虑 chroot（确保路径在 chroot 内可访问）
             和 uid/gid（确保路径具有适当写权限）。

           - "fd@<number>" 形式的文件描述符，可指向管道、终端或套接字。
             此时使用无缓冲日志，每条日志调用一次 writev()，开销稍高，但大多数工作负载可接受。
             消息不会截断，但可能丢弃，此时 DroppedLogs 计数器递增。
             对不超过 PIPE_BUF 的消息，writev() 即使写入管道也具有原子性。
             POSIX 建议此大小至少为 512，大多数现代操作系统为 4096 字节。
             更大的消息可能与其他进程的消息交错。仅为调试，可将文件描述符指向文件，
             但非阻塞调用会被忽略，显著降低 HAProxy 速度；不重启进程也无法清理或轮转该文件。
             配置的 syslog 格式仍保留，输出适合 TCP syslog 服务器。另见下方 "short" 和 "raw" 格式。

           - "stdout" / "stderr"，分别是 "fd@1" 和 "fd@2" 的别名，见上文。

           - "ring@<name>" 形式的环形缓冲区，对应内存中的环形缓冲区，
             可通过 CLI 的 "show events" 命令访问；该命令也列出已有环及其大小。
             缓冲区在重载或重启时丢失，但作为补充手段，可立即获取日志，帮助故障排查。详情见第 12.5 节。

           - "backend@<name>" 形式的日志后端，将消息发送到对应日志后端，
             由其按负载均衡设置发送到适当服务器。日志后端是设置 "mode log" 的 backend 段
             （更多信息见 "mode"）。

           - "tcp@"、"tcp6@"、"tcp4@" 或 "uxst@" 等显式流地址前缀，
             会分配隐式环形缓冲区及指向该地址的流转发服务器。

           地址参数可能需要引用环境变量，参见第 2.3 节。

<length>   是可选的最大行长度。超过此值的日志行在发送前截断，因为 syslog 服务器对行长度处理不同。
           所有服务器支持默认值 1024，但某些服务器直接丢弃更长的行，其他服务器仍能记录。
           支持长行时，可设置此值避免截断；丢弃长行时，最好在发送前截断。
           接受 80 到 65535（含两端），默认 1024 通常适合标准用法。
           长捕获或 JSON 日志可能需要更大的值。请求 URI 被截断时，可能还需增大 "tune.http.logurilen"。

<ranges>   是逗号分隔的范围列表，确定采样哪些日志，以均衡发送到日志服务器的负载。
           范围边界不能为零，从 1 开始编号。采样大小或周期（日志条数）须通过 <sample_size> 设置。

<sample_size>
           是均衡日志负载时考虑的采样日志条数，用于均衡发送到 syslog 服务器的负载。
           必须大于或等于各范围上界的最大值（另见 <ranges>）。

<format> 是生成 syslog 消息时使用的日志格式，可为：

  local     类似 rfc3164 syslog 消息格式，但去除主机名字段。这是默认值。
            注意："log-send-hostname" 会将默认值切换为 rfc3164。

  rfc3164   RFC3164 syslog 消息格式。
            (https://tools.ietf.org/html/rfc3164)

  rfc5424   RFC5424 syslog 消息格式。
            (https://tools.ietf.org/html/rfc5424)

  priority  仅包含尖括号内的级别与 syslog facility 之和，如 '<63>'，以及其后的文本。
            省略 PID、日期、时间、进程名称和系统名称，适用于本地日志服务器。

  short     仅包含尖括号内的级别，如 '<3>'，以及其后的文本。
            省略 PID、日期、时间、进程名称和系统名称，适用于本地日志服务器，兼容 systemd 日志记录器。

  timed     仅包含尖括号内的级别，如 '<3>'，以及其后的 ISO 日期和文本。
            省略 PID、进程名称和系统名称，适用于本地日志服务器。

  iso       仅包含 ISO 日期及其后的文本，省略 PID、进程名称和系统名称，适用于本地日志服务器。

  raw       仅包含文本，省略级别、PID、日期、时间、进程名称和系统名称。
            适用于容器或开发环境，严重程度仅取决于使用的文件描述符（stdout/stderr）。

<prof>     是可选的 "log-profile" 段名称，在构建日志时覆盖部分选项。
           更多信息见 "8.3.5. Log profiles"。

<facility> 必须为 24 个标准 syslog facility 之一：

               kern   user   mail   daemon auth   syslog lpr    news
               uucp   cron   auth2  ftp    ntp    audit  alert  cron2
               local0 local1 local2 local3 local4 local5 local6 local7

           "short" 和 "raw" 格式忽略 facility，但仍要求提供此位置参数。
           此时推荐用 "daemon"，明确表示仅用于本地。

<level>    是可选参数，用于过滤出站消息，默认发送全部消息。
           指定级别后，仅发送严重程度至少达到该级别的消息。
           还可指定可选的最低级别；超过该严重程度的日志会被限制在该级别，
           避免某些默认 syslog 配置将 "emerg" 消息发送到所有终端。支持八个级别：

             emerg  alert  crit   err    warning notice info  debug
```

请注意，决定从连接中记录哪些内容的是前端，若发生内容切换，则后端生成的日志条目将被忽略。连接日志记录级别为 "info"。

然而，后端日志声明定义了服务器状态变更的记录方式和位置。状态变为“上线”时使用级别“notice”记录，收到终止信号或服务永久终止时使用级别“warning”记录，服务器宕机时使用级别“alert”记录。

请注意：根据 RFC3164，消息在发出前会被截断至 1024 字节。

示例：

```text
log global
log stdout format short daemon          # send log to systemd
log stdout format raw daemon            # send everything to stdout
log stderr format raw daemon notice     # send important events to stderr
log 127.0.0.1:514 local0 notice         # only send important events
log tcp@127.0.0.1:514 local0 notice notice  # same but limit output
                                            # level and send in tcp
log "${LOCAL_SYSLOG}:514" local0 notice   # send to local server
```

<a id="entry-4-2-log-format"></a>

**`log-format <fmt>`**

```haproxy
log-format <fmt>
```

指定用于流量日志的自定义日志格式字符串

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

该指令指定将用于通过此行配置的前端处理流量所产生的所有日志的日志格式字符串。若该指令在 defaults 段中使用，则后续所有前端将采用相同的日志格式。请参见 [第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6)，其中详细介绍了自定义日志格式字符串。

也可定义仅在连接错误情况下使用的特定日志格式，详见 "error-log-format" 选项。

"log-format" 指令会覆盖之前的 "option tcplog"、"log-format"、"option httplog" 和 "option httpslog" 指令。

<a id="entry-4-2-log-format-sd"></a>

**`log-format-sd <fmt>`**

```haproxy
log-format-sd <fmt>
```

指定用于生成 RFC5424 结构化数据的自定义日志格式字符串

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

该指令指定 RFC5424 结构化数据日志格式字符串，该字符串将用于通过此行配置的前端处理流量所产生的所有日志。若该指令在 defaults 段中使用，则后续所有前端均将采用相同的日志格式。请参见 [第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6)，其中深入介绍了日志格式字符串。

有关 RFC5424 结构化数据部分的更多信息，请参见 <https://tools.ietf.org/html/rfc5424#section-6.3>。

请注意：此日志格式字符串仅适用于将日志格式设置为 "rfc5424" 的记录器。

示例：

```text
log-format-sd [exampleSDID@1234\ bytes=\"%B\"\ status=\"%ST\"]
```

<a id="entry-4-2-log-steps"></a>

**`log-steps <steps>`**

```haproxy
log-steps <steps>
```

指定在事务处理过程中应在哪些步骤生成日志。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

在处理 TCP/HTTP 事务时，HAProxy 可能在处理过程的不同阶段生成日志（例如：接受连接、建立连接、接收请求、发送响应、关闭连接）。

默认情况下，HAProxy 每个事务仅生成一条日志，且仅在日志格式表达式中使用的所有项均满足后才发出日志，这意味着在实际应用中，日志通常在事务结束时发出（HTTP 为响应结束后，TCP 为连接结束后），除非使用了 "option logasap"。

指令 "log-steps" 允许精确控制日志的输出时机，甚至支持为同一事务输出多条日志。特殊值 "all" 可用于启用所有可用的日志来源，从而实现从连接接收至连接关闭的完整事务追踪。也可通过用逗号分隔的名称指定个别日志来源，以选择性地启用日志输出。

常见的日志来源包括：accept、connect、request、response、close。

示例：

```text
frontend myfront
    option httplog
    log-steps accept,close         #only log accept and close for the txn
```

可直接在日志配置文件中使用以“logging steps”（如 accept、close）指定的日志来源（在 'on' 指令之后）。将“log-steps”与日志配置文件结合使用，能够对 HAProxy 在事务处理过程中自动生成的日志实现细粒度控制，具有很高的实用价值。

此设置仅对前端有效，后端将忽略该设置。

另请参阅："log-profile"

<a id="entry-4-2-log-tag"></a>

**`log-tag <string>`**

```haproxy
log-tag <string>
```

指定用于所有出站日志的日志标签

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

设置 syslog 头中的标签字段为该字符串。默认值为全局段中设置的 log-tag，否则为从命令行启动时的程序名称，通常为 "HAProxy"。在同一个主机上运行多个进程时，或在同一个进程中运行多个客户实例时，有时需要加以区分。在后端中，关于服务器启停的日志将使用此标签。作为提示，可以在 defaults 段中设置与托管客户相关的 log-tag，然后将该客户的全部前端和后端配置放在此段中，再在新的 defaults 段中开始配置另一个客户。参见全局段中的 "log-tag" 指令。

<a id="entry-4-2-max-keep-alive-queue"></a>

**`max-keep-alive-queue <value>`**

```haproxy
max-keep-alive-queue <value>
```

设置用于维持持久连接的服务器队列最大大小

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

HTTP 持久连接会尽可能复用相同的服务器连接，但在某些情况下可能适得其反，例如当某些服务器连接数较多而其他服务器处于空闲状态时。这一点在静态服务器上尤为明显。

本设置的目的是设定一个队列中连接数量的阈值，当超过该阈值时，HAProxy 停止尝试复用同一台服务器，转而优先选择其他服务器。默认值 -1 表示无限制。值为 0 表示持久连接永远不会被排队。对于延迟较低、且对中断持久连接不敏感的近距离服务器，建议使用较低的值（例如，本地静态服务器可使用 10 或更小的值）。对于延迟较高的远程服务器，可能需要更高的值以弥补延迟和/或选择其他服务器的开销。

请注意，此设置对连续发送至同一服务器的响应无影响，即使这些响应需被排队。在收到 401 响应后，它们仍会发送至同一服务器。

另请参阅：“option http-server-close”、“option prefer-last-server”、服务器“maxconn”和 cookie 持久性。

<a id="entry-4-2-max-session-srv-conns"></a>

**`max-session-srv-conns <nb>`**

```haproxy
max-session-srv-conns <nb>
```

设置单个客户端会话可保持空闲的最大出站连接数。默认值为 5（精确等于在编译时定义的 MAX_SRV_LIST）。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

<a id="entry-4-2-maxconn"></a>

**`maxconn <conns>`**

```haproxy
maxconn <conns>
```

设定前端的最大并发连接数

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
<conns>   是前端接受并提供服务的最大并发连接数。超出的连接由系统排入套接字的监听队列，
          在已有连接关闭后再提供服务。
```

如果系统支持，对于大型站点而言，将此限制值设得非常高可能很有用，以便 HAProxy 管理连接队列，而非让客户端处于未响应的连接尝试状态。该值不应超过全局 maxconn。同时请注意，每个连接包含两个 tune.bufsize（默认为 16 kB）的缓冲区，以及一些其他数据，导致每个已建立的连接大约消耗 33 kB 的内存。这意味着，经过适当调优的中等规模系统，配备 1 GB 内存时，可承受约 20000 至 25000 个并发连接。

此外，当 `<conns>` 设置为较大值时，服务器可能无法承受如此高的负载，因此通常建议为其分配合理的连接限制。

当该值设置为零时（即默认值），将使用全局的 "maxconn" 值。

另请参阅："server"、global 段的 "maxconn"、"fullconn"

<a id="entry-4-2-mode"></a>

**`mode { tcp|http|log|spop }`**

```haproxy
mode { tcp|http|log|spop }
```

设置实例的运行模式或协议。
可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
tcp       实例以纯 TCP 模式工作，在客户端与服务器之间建立全双工连接，不进行第 7 层检查。
          这是默认模式，适用于 SSL、SSH、SMTP 等。

http      实例以 HTTP 模式工作，在连接任何服务器之前深入分析客户端请求。
          不符合 RFC 的请求将被拒绝，可进行第 7 层过滤、处理和切换。
          这是最能体现 HAProxy 价值的模式。

haterm    前端以 haterm HTTP 基准测试模式工作。后端不支持此模式。详情见 doc/haterm.txt。

log       在 backend 段中使用时，将其转换为日志后端。通过 "backend@<name>" 语法，
          此类后端可作为任意 "log" 指令的日志目标。日志消息按可通过 "balance" 关键字配置的
          负载均衡设置分发给后端服务器。在服务器地址前添加 "udp@" 前缀，可支持 UDP 服务器。
          支持通用的后端和服务器功能，但不支持 TCP 或 HTTP 专用功能。

spop      在 backend 段中使用时，将其转换为 spop 后端。后端包含 SPOA 服务器时必须使用此模式；
          但在 tcp 模式下检测到此类服务器时，会自动转换为 spop 模式。
```

进行内容切换时，前端和后端必须处于相同模式（通常为 HTTP），否则配置将被拒绝。

示例：

```text
defaults http_instances
    mode http

```

<a id="entry-4-2-monitor-fail"></a>

**`monitor fail { if | unless } <condition>`**

```haproxy
monitor fail { if | unless } <condition>
```

为监控 HTTP 请求添加一个失败报告条件。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| no

参数：

```text
if <cond>     条件满足时监控请求失败，否则成功。该条件应描述一个组合测试，
              在全部条件满足时触发失败，例如后端及其备用后端的服务器数量均较少。

unless <cond> 仅当条件满足时监控请求成功，否则失败。
              此条件可基于检查一组后端中是否有最低数量的活跃服务器。
```

此语句添加一个条件，可强制对监控请求的响应报告失败。默认情况下，当外部组件查询专用于监控的 URI 时，将返回 200 响应。当满足上述任一条件时，HAProxy 将返回 503 而非 200。此机制对于向外部组件报告站点故障非常有用，外部组件可能基于 HAProxy 报告的可用性状态在多个站点间进行路由通告。在此场景中，应依赖包含 "nbsrv" 条件的 ACL。请注意，"monitor fail" 仅在 HTTP 模式下有效。如需调整，可使用 "errorfile" 或 "errorloc" 自定义状态消息。

示例：

```text
frontend www
   mode http
   acl site_dead nbsrv(dynamic) lt 2
   acl site_dead nbsrv(static)  lt 2
   monitor-uri   /site_alive
   monitor fail  if site_dead
```

另请参阅："monitor-uri"、"errorfile"、"errorloc"

<a id="entry-4-2-monitor-uri"></a>

**`monitor-uri <uri>`**

```haproxy
monitor-uri <uri>
```

拦截外部组件监控请求所使用的 URI

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
<uri>     是要拦截的确切 URI，用于返回 HAProxy 的健康状态，而非转发请求。
```

当在前端接收到引用 `<uri>` 的 HTTP 请求时，HAProxy 不会转发该请求，也不会记录日志，而是返回“HTTP/1.0 200 OK”或“HTTP/1.0 503 Service unavailable”，具体取决于通过“monitor fail”定义的故障条件。通常情况下，任何前端 HTTP 探针均可据此判断服务处于正常运行状态，而无需将请求转发至后端服务器。请注意，HTTP 方法、版本及所有头字段均被忽略，但请求在 HTTP 层面必须至少有效。该关键字仅可与 HTTP 模式前端一同使用。

监控请求在解析后立即处理，甚至早于任何 "http-request" 规则。在此之前仅应用了 tcp-request 规则集。这些请求无法被记录，这是设计目的。监控仅可配置一个 URI；当存在多个 "monitor-uri" 语句时，最后一个将决定所使用的 URI。它们仅用于向高层组件报告 HAProxy 的健康状态，除此之外无其他用途。然而，可以使用 "monitor fail" 和 ACLs 添加任意数量的条件，从而根据任何可设想的检查结果进行调整（最常见的场景是后端中可用服务器的数量）。

请注意：如果 `<uri>` 以斜杠（'/'）开头，则匹配将基于请求路径而非请求 URI 执行。此做法为一种变通方案，用于使 HTTP/2 请求能够匹配 monitor-uri。在 HTTP/2 中，客户端被建议仅发送绝对 URI。

示例：

```shell
# Use /haproxy_test to report HAProxy's status
frontend www
    mode http
    monitor-uri /haproxy_test
```

另请参阅：“monitor fail”

<a id="entry-4-2-option-abortonclose"></a>

**`option abortonclose`**

```haproxy
option abortonclose
no option abortonclose
```

启用或禁用客户端关闭时对未开始处理的早期中止

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

TCP 连接支持在每个方向上独立关闭，仅单向关闭的连接通常被称为“半关闭”。最初，在 HTTP 生态系统主要采用“关闭模式”时，每个连接仅传输一次请求和一次响应后即关闭，此时脚本化客户端发送请求后关闭发送方向，等待响应，接收关闭指示后即完成操作的情况十分常见。然而，随着持久连接及更高级协议的出现，这种做法已基本消失。目前，客户端在未收到响应前关闭连接的情况，本质上仅出现在用户希望中止传输，或超时触发导致连接被关闭的场景中。

这两种情况（半关闭与中止）从服务器端（此处为 HAProxy 监听器）无法区分。这是一个问题，因为当客户端中止连接后仍保持连接并继续处理请求，会消耗大量资源，尤其是当连接关闭是由于用户点击“重载”按钮所致时，意味着新请求被排队，而先前的请求并未被中止。反之，若在遇到此类半关闭情况时一律中止连接，将导致大量 TCP 应用程序以及部分内部网络中与旧版代理交互的 HTTP 应用程序无法正常工作。

"abortonclose" 选项允许选择期望的行为：当该选项存在于前端时，将避免处理处于半关闭连接上的待处理 TLS 握手。这可能是由于用户在高负载下执行 HTTPS 请求时触发“重载”操作，例如在主 HAProxy 节点与备用节点之间发生 VRRP 故障转移时：所有客户端同时重新连接至新节点，且所有客户端均需执行开销较高的完整 TLS 握手。若该过程耗时超过数秒，很可能导致部分用户放弃连接，此时继续为其执行握手将毫无意义。鉴于 TLS 握手的 CPU 开销较高，建议在面向互联网的前端上保持该选项启用。对于入站 TLS 连接，此为默认行为。

    - 当该选项存在于后端时，将使半关闭连接尝试中止尚未发送至服务器的
      请求（即该请求仍在队列中等待或正在尝试建立连接时）。如果请求已由
      某台服务器处理，则与该服务器的连接也会相应切换为半关闭状态，以向
      服务器表明同样的情况，由服务器决定后续如何处理。对于 HTTP 模式的
      后端，此为默认行为。

建议在面向互联网的 TLS 终端节点和 HTTP 服务上启用此选项，并在纯 TCP 服务以及未暴露的旧环境里禁用。HTTP 后端中默认启用此选项，可通过在后端段或其继承的“defaults”段中前置“no”关键字强制禁用。TLS 监听器也默认启用此选项，同样可通过在前端段或其继承的“defaults”段中指定“no option abortonclose”强制禁用。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：“timeout queue” 以及服务器的 “maxconn” 和 “maxqueue” 参数

<a id="entry-4-2-option-accept-invalid-http-request"></a>

**`option accept-invalid-http-request     (deprecated)`**

```haproxy
option accept-invalid-http-request     (deprecated)
no option accept-invalid-http-request  (deprecated)
```

启用或禁用对 HTTP 请求解析的宽松处理

“accept-invalid-http-request” 关键字已弃用，请改用 “option accept-unsafe-violations-in-http-request”。

<a id="entry-4-2-option-accept-invalid-http-response"></a>

**`option accept-invalid-http-response     (deprecated)`**

```haproxy
option accept-invalid-http-response     (deprecated)
no option accept-invalid-http-response  (deprecated)
```

启用或禁用对 HTTP 响应解析的宽松处理

"accept-invalid-http-response" 关键字已弃用，请改用 "option accept-unsafe-violations-in-http-response"。

<a id="entry-4-2-option-accept-unsafe-violations-in-http-request"></a>

**`option accept-unsafe-violations-in-http-request`**

```haproxy
option accept-unsafe-violations-in-http-request
no option accept-unsafe-violations-in-http-request
```

启用或禁用对 HTTP 请求解析的宽松处理

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

默认情况下，HAProxy 会遵循不同的 HTTP RFC 规范进行消息解析。这意味着消息解析非常严格，对于格式错误的消息会向客户端返回错误。这种行为是期望的，因为格式错误的消息本质上常被用于利用服务器弱点的攻击，或绕过安全过滤。有时，由于某种原因（配置、实现等），某些存在缺陷的浏览器可能不遵守这些 RFC，而问题不会立即得到修复。在此情况下，可以通过指定该选项来放宽 HAProxy 的解析规则，以接受部分无效请求。大多数规则出于历史原因主要针对 H1 解析。较新的 HTTP 版本趋向于更加规范，应用程序也更严格地遵循这些协议。

当设置此选项时，遵循以下规则：

    * 仅在 H1 中，头名称中的无效字符（包括 NULL 字符）不会被拒绝；但该头
      将被丢弃。

    * 仅在 H1 中，头值中的 NULL 字符将被接受；

    * 仅在 H1 中，URI 中大于 127 的字符将被接受。URI 中允许出现的字符
      列表由 RFC3986 明确定义，字符 0-31、32（空格）、34（'"'）、60
      （'<'）、62（'>'）、92（'&#92;'）、94（'^'）、96（'`'）、123（'{'）、
      124（'|'）、125（'}'）、127（delete）及以上的字符通常不被允许。在
      H1 中，介于（0..32）与 127 之间的所有字符始终会被阻止。大于 127
      （不含）的所有字符也会被阻止，除非启用了此选项。其他字符（33..126）
      则完全不会被检查。

    * 在 H1 和 H2 中，包含片段引用（位于路径之后的 '#'）的 URL 将被接受；

    * 仅在 H1 中，不会对 CONNECT 请求的授权部分（authority）执行检查；

    * 仅在 H1 中，不会对授权部分与 Host 头的值执行检查。

    * 仅在 H1 中，对 HTTP 版本的测试将放宽。它允许 HTTP/0.9 的 GET 请求
      通过（不指定版本），也允许不同的协议名称（例如 RTSP），以及主版本
      号和次版本号使用多个数字。

    * 仅在 H1 中，未能提供有效 "Sec-Websocket-Key" 头字段的 WebSocket
      （RFC6455）请求将被接受。

此选项默认情况下绝不可启用，因为它会隐藏应用程序的缺陷和安全漏洞。仅在确认问题存在后方可部署。

启用此选项后，无效但被接受的 H1 请求将被捕获，以便后续通过 UNIX 统计套接字上的 "show errors" 请求进行分析。执行此操作还有助于确认问题已解决。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：“option accept-unsafe-violations-in-http-response”以及统计套接字上的 “show errors”。

<a id="entry-4-2-option-accept-unsafe-violations-in-http-response"></a>

**`option accept-unsafe-violations-in-http-response`**

```haproxy
option accept-unsafe-violations-in-http-response
no option accept-unsafe-violations-in-http-response
```

启用或禁用对 HTTP 响应解析的宽松处理

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

与“option accept-unsafe-violations-in-http-request”类似，此选项可用于放宽对 HTTP 响应的解析规则。仅当目标服务器为可信的旧版服务器时，才应启用此选项以接受部分无效响应。大多数规则出于历史原因针对 H1 解析。较新的 HTTP 版本通常更为规范，应用程序也更严格遵循这些协议。

当设置此选项时，遵循以下规则：

    * 仅在 H1 中，长度超过 3 位数字但数值可容纳于 16 位的状态码不会被
      拒绝。

    * 仅在 H1 中，头名称中的无效字符（包括 NULL 字符）不会被拒绝；但该头
      将被丢弃。

    * 仅在 H1 中，头值中的 NULL 字符将被接受；

    * 仅在 H1 中，Transfer-Encoding 头的空值或多个 "chunked" 值出现将被
      接受；

    * 仅在 H1 中，不会对授权部分与 Host 头的值执行检查。

    * 仅在 H1 中，对 HTTP 版本的测试将放宽。它允许不同的协议名称（例如
      RTSP），以及主版本号和次版本号使用多个数字。

    * 仅在 H1 中，未能提供有效 "Sec-Websocket-Accept" 头字段的 WebSocket
      （RFC6455）响应将被接受。

此选项默认情况下绝不可启用，因为它会隐藏应用程序的缺陷和安全漏洞。仅在确认问题存在后方可部署。

启用此选项后，响应中的错误头名称仍会被接受，但会完整捕获响应内容，以便后续通过 UNIX 统计套接字上的 "show errors" 请求进行分析。执行此操作还有助于确认问题已解决。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：“option accept-unsafe-violations-in-http-request”以及统计套接字上的 “show errors”。

<a id="entry-4-2-option-allbackups"></a>

**`option allbackups`**

```haproxy
option allbackups
no option allbackups
```

可同时使用所有备用服务器，或仅使用第一个备用服务器。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

默认情况下，当所有正常服务器均不可用时，首个处于运行状态的备用服务器将接收全部流量。
有时可能更希望同时使用多个备用服务器，因为仅使用一个可能不够。当启用 "option allbackups" 时，若所有正常服务器均不可用，负载均衡将在所有备用服务器之间进行。将使用相同的负载均衡算法，并尊重服务器的权重。因此，备用服务器之间将不再存在优先级顺序。

该选项通常用于静态服务器集群，当应用程序完全离线时，返回“抱歉”页面。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

<a id="entry-4-2-option-checkcache"></a>

**`option checkcache`**

```haproxy
option checkcache
no option checkcache
```

分析所有服务器响应，并阻止包含可缓存 Cookie 的响应

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

某些高级框架会在所有位置设置应用 Cookie，且并不总是为开发者提供足够的控制权，以管理响应的缓存方式。当缓存对象返回会话 Cookie 时，用户通过相同缓存时发生会话交叉或窃取的风险极高。在某些情况下，阻止响应比让敏感会话信息暴露在外更为妥当。

选项 "checkcache" 启用对所有服务器响应的深度检查，以确保其严格符合 HTTP 规范中关于可缓存性的要求。该选项会仔细检查服务器响应中的 "Cache-Control"、"Pragma" 和 "Set-Cookie" 头，以判断是否存在客户端代理缓存 Cookie 的风险。启用此选项后，仅以下响应可传递给客户端： - 所有不含 "Set-Cookie" 头的响应； - 所有返回码非 200、203、204、206、300、301、404、405、410、414、501 的响应，前提是服务器未设置 "Cache-Control: public" 头字段； - 所有通过非 GET、HEAD、OPTIONS、TRACE 方法发起的请求所导致的响应，前提是服务器未设置 "Cache-Control: public" 头字段； - 所有包含 "Pragma: no-cache" 头的响应； - 所有包含 "Cache-Control: private" 头的响应； - 所有包含 "Cache-Control: no-store" 头的响应； - 所有包含 "Cache-Control: max-age=0" 头的响应； - 所有包含 "Cache-Control: s-maxage=0" 头的响应； - 所有包含 "Cache-Control: no-cache" 头的响应； - 所有包含 "Cache-Control: no-cache=\"set-cookie\"" 头的响应； - 所有包含 "Cache-Control: no-cache=\"set-cookie," 头的响应（允许 "set-cookie" 之后包含其他字段）； - 所有既不包含新鲜度信息（带有 "max-age" 或 "s-maxage" 的 "Cache-control" 头，或 "Expires" 头），也不包含验证器（"ETag" 或 "Last-Modified" 头）的响应，因为符合规范的缓存不会存储此类响应。

如果响应不满足这些要求，则其将被阻止，效果等同于来自 "http-response deny" 规则的响应，返回 "HTTP 502 bad gateway"。会话状态显示为 "PH--"，表示代理在处理头时阻断了响应。此外，日志中将发送告警，以便管理员知晓需进行修复。

由于该选项对应用影响较大，应用在上线生产环境前应充分测试启用该选项的情况。在测试过程中，即使生产环境不使用该选项，也建议始终启用，以便报告潜在危险的应用行为。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

<a id="entry-4-2-option-clitcpka"></a>

**`option clitcpka`**

```haproxy
option clitcpka
no option clitcpka
```

启用或禁用在客户端侧发送 TCP keepalive 数据包

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

当客户端与服务器之间存在防火墙或其他会话感知组件，且协议涉及长时间会话及较长空闲期（例如远程桌面）时，中间组件可能因会话空闲时间过长而决定终止该会话，从而带来风险。

启用套接字级别的 TCP 持久连接可使系统定期向连接的另一端发送数据包，从而保持连接处于活跃状态。持久连接探测之间的延迟由系统控制，且取决于操作系统及其调优参数。

必须理解，持久连接报文不会在应用层发出或接收，仅网络协议栈能够感知到它们。因此，即使代理的一端已使用持久连接来维持连接活跃，这些持久连接报文也不会被转发至代理的另一端。

请注意，这与 HTTP 持久连接无关。

使用选项 "clitcpka" 可在连接的客户端一侧启用 TCP 持久连接探测，当 HAProxy 与客户端之间的会话超时被察觉时，此功能应能提供帮助。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：“option srvtcpka”、“option tcpka”

<a id="entry-4-2-option-contstats"></a>

**`option contstats`**

```haproxy
option contstats
```

启用持续的流量统计信息更新

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

默认情况下，用于统计信息计算的计数器仅在流结束时才递增。在提供小对象时，该机制工作良好；但在处理大对象（例如大型图片或归档文件）或音视频流时，由 HAProxy 计数器生成的图表会呈现类似刺猬的形态。启用此选项后，计数器会在流过程中频繁递增，通常每 5 秒一次，这通常足以生成清晰的图表。由于重新计数会直接触碰热点路径，因此默认不启用，因为这可能导致会话数量极大时产生大量唤醒，从而造成轻微性能下降。

<a id="entry-4-2-option-disable-h2-upgrade"></a>

**`option disable-h2-upgrade`**

```haproxy
option disable-h2-upgrade
no option disable-h2-upgrade
```

启用或禁用从 HTTP/1.x 客户端连接隐式升级至 HTTP/2。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

默认情况下，HAProxy 能够在从特定 HTTP 连接接收到的首个请求与 HTTP/2 连接前缀匹配时，隐式将 HTTP/1.x 客户端连接升级为 HTTP/2 连接（即字符串 "PRI \* HTTP/2.0&#92;r&#92;n&#92;r&#92;nSM&#92;r&#92;n&#92;r&#92;n"）。
通过这种方式，可在非 SSL 连接上同时支持 HTTP/1.x 与 HTTP/2 客户端。
必须使用此选项以禁用隐式升级。
请注意，此隐式升级仅支持 HTTP 代理，因此该选项也仅适用于 HTTP 代理。
此外，可通过在 bind 行指定 "proto h2" 强制在明文连接上启用 HTTP/2。
最后，此选项适用于所有 bind 行。
如需禁用特定 bind 行的隐式 HTTP/2 升级，可使用 "proto h1"。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

<a id="entry-4-2-option-dontlog-normal"></a>

**`option dontlog-normal`**

```haproxy
option dontlog-normal
no option dontlog-normal
```

启用或禁用正常、成功的连接日志记录

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

某些大型站点每秒需处理数千个连接，日志记录成为一大难题。部分站点甚至被迫关闭日志功能，无法对生产环境问题进行调试。启用此选项后，正常连接（即未发生错误、超时、重试或重分派的连接）将不会被记录。此举可为异常情况保留磁盘空间。在 HTTP 模式下，将检查响应状态码，状态码为 5xx 的响应仍会被记录。

强烈不建议使用此选项，因为大多数情况下，复杂问题的关键信息存在于常规日志中，而这些日志不会在此处记录。如需分离日志，请改用 `log-separate-errors` 选项。

另请参阅：“log”、“dontlognull”、“log-separate-errors”以及 [第 8 节](/zh/haproxy/configuration-logging/) 中关于日志记录的内容。

<a id="entry-4-2-option-dontlognull"></a>

**`option dontlognull`**

```haproxy
option dontlognull
no option dontlognull
```

启用或禁用空连接日志记录

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

在某些环境中，存在一些组件会定期连接到各个系统，以确保其仍处于活跃状态。这可能是来自另一台负载均衡器，也可能是来自监控系统。默认情况下，即使是一个简单的端口探测或扫描也会产生日志。如果这些连接导致日志过于冗杂，可以启用选项 `dontlognull`，以指示未传输任何数据的连接将不会被记录，这通常对应于此类探测。请注意，错误仍会返回给客户端，并计入统计信息。若不希望如此，可改用选项 `http-ignore-probes`。

在不受控制的环境（例如互联网）中，通常不建议使用此选项，否则扫描及其他恶意活动将不会被记录。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：“log”、“http-ignore-probes”、“monitor-uri”以及关于日志记录的[第 8 节](/zh/haproxy/configuration-logging/)。

<a id="entry-4-2-option-external-check"></a>

**`option external-check`**

```haproxy
option external-check
```

使用外部进程进行服务器健康检查

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

可以使用外部命令测试服务器的健康状态。这通过运行使用 "external-check command" 设置的可执行文件来实现。

必须设置全局选项 "external-check"。

另请参阅："external-check"、"external-check command"、"external-check path"

<a id="entry-4-2-option-forwarded"></a>

**`option forwarded [ proto ]`**

```haproxy
option forwarded [ proto ]
                 [ host | host-expr <host_expr> ]
                 [ by | by-expr <by_expr> ] [ by_port | by_port-expr <by_port_expr>]
                 [ for | for-expr <for_expr> ] [ for_port | for_port-expr <for_port_expr>]
no option forwarded
```

启用在发送至服务器的请求中插入 rfc 7239 forwarded 头

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<host_expr>     可选参数，指定自定义样本表达式，将其结果用作 'host' 参数值。

<by_expr>       可选参数，指定自定义样本表达式，将其结果用作 'by' 参数的节点名称值。

<for_expr>      可选参数，指定自定义样本表达式，将其结果用作 'for' 参数的节点名称值。

<by_port_expr>  可选参数，指定自定义样本表达式，将其结果用作 'by' 参数的节点端口值。

<for_port_expr> 可选参数，指定自定义样本表达式，将其结果用作 'for' 参数的节点端口值。
```

由于 HAProxy 以反向代理模式运行，服务器会丢失部分请求上下文（例如请求来源：客户端 IP 地址、所用协议等...）

一种常见的应对此限制的方法是使用广为人知的 X-Forwarded-For 和 X-Forwarded-* 等头字段，将部分上下文信息暴露给底层服务器或应用程序。尽管过去该方法曾有效且广泛部署，但并未得到 IETF 的官方支持，可能引发互操作性及安全问题。

为解决此问题，IETF 已定义了一种新的 HTTP 扩展：forwarded 头（RFC7239）。更多信息请参见 <https://www.rfc-editor.org/rfc/rfc7239.html>

此单一头字段的使用可在同一头中传递大量信息，且最重要的是，解决了代理链问题。（RFC 允许多个级联代理向已存在的头字段追加各自的值。）

该选项可在 defaults、listen 或 backend 段中指定，但在 frontend 段中将被忽略。

设置选项 forwarded 且不带参数时，将使用默认隐式行为。默认行为启用 proto 参数，并注入原始客户端 IP。

等效的显式/手动配置如下：

```text
option forwarded proto for
```

关键字 'by' 用于在转发头中启用 'by' 参数（"nodename"）。该功能允许嵌入请求代理信息。若不可用（例如：UNIX 监听器），'by' 值将设为 "unknown"。

关键字 'by-expr' 用于在转发头中启用 'by' 参数（"nodename"）。它允许嵌入请求代理信息。若样本表达式 `<by_expr>` 有效，则 'by' 值将被设置为该表达式的计算结果；否则，将被设置为 "unknown"。

关键字 'for' 用于在转发头中启用 'for' 参数（"nodename"）。它允许嵌入请求客户端信息。若不可用（例如：UNIX 监听器），'for' 值将设为 "unknown"。

关键字 'for-expr' 用于在转发头中启用 'for' 参数（"nodename"）。它允许嵌入请求客户端信息。若样本表达式 `<for_expr>` 有效，则 'for' 值将被设置为该表达式的计算结果；否则，将被设置为 "unknown"。

关键字 'by_port' 用于向 'by' 参数提供“nodeport”信息。'by_port' 要求必须设置 'by' 或 'by-expr'，否则将被忽略。若可用，“nodeport”将被设为代理（目标）端口，否则将被忽略。

关键字 'by_port-expr' 用于向 'by' 参数提供“nodeport”信息。'by_port-expr' 要求必须设置 'by' 或 'by-expr'，否则将被忽略。若样本表达式 `<by_port_expr>` 有效，“nodeport”将被设置为该表达式的计算结果，否则将被忽略。

关键字 'for_port' 用于向 'for' 参数提供“nodeport”信息。'for_port' 要求必须设置 'for' 或 'for-expr'，否则将被忽略。“nodeport”将在可用时设为客户端（源）端口，否则将被忽略。

关键字 'for_port-expr' 用于向 'for' 参数提供“nodeport”信息。'for_port-expr' 要求必须设置 'for' 或 'for-expr'，否则将被忽略。“nodeport”将被设置为样本表达式 `<for_port_expr>` 的结果（若有效），否则将被忽略。

示例：

```shell
# Those servers want the ip address and protocol of the client request
# Resulting header would look like this:
#   forwarded: proto=http;for=127.0.0.1
backend www_default
    mode http
    option forwarded
    #equivalent to: option forwarded proto for

# Those servers want the requested host and hashed client ip address
# as well as client source port (you should use seed for xxh32 if ensuring
# ip privacy is a concern)
# Resulting header would look like this:
#   forwarded: host="haproxy.org";for="_000000007F2F367E:60138"
backend www_host
    mode http
    option forwarded host for-expr src,xxh32,hex for_port

# Those servers want custom data in host, for and by parameters
# Resulting header would look like this:
#   forwarded: host="host.com";by=_haproxy;for="[::1]:10"
backend www_custom
    mode http
    option forwarded host-expr str(host.com) by-expr str(_haproxy) for for_port-expr int(10)

# Those servers want random 'for' obfuscated identifiers for request
# tracing purposes while protecting sensitive IP information
# Resulting header would look like this:
#   forwarded: for=_000000002B1F4D63
backend www_for_hide
    mode http
    option forwarded for-expr rand,hex
```

另请参阅："option forwardfor"、"option originalto"

<a id="entry-4-2-option-forwardfor"></a>

**`option forwardfor [ except <network> ] [ header <name> ] [ if-none ]`**

```haproxy
option forwardfor [ except <network> ] [ header <name> ] [ if-none ]
```

启用向发送至服务器的请求插入 X-Forwarded-For 头

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<network> 是可选参数，对匹配 <network> 的源禁用此选项。
<name>    是可选参数，指定不同的 "X-Forwarded-For" 头名称。
```

由于 HAProxy 以反向代理模式运行，服务器看到的客户端地址为其 IP 地址。
当服务器日志需要记录客户端的真实 IP 地址时，这种情况有时会造成困扰。为解决此问题，HAProxy 可在发送至服务器的所有请求中添加知名的 HTTP 头 “X-Forwarded-For”。该头包含表示客户端 IP 地址的值。由于此头始终被追加到现有头列表的末尾，服务器必须配置为仅使用该头的最后一个出现位置。请参阅服务器手册，了解如何启用对这一标准头的使用。请注意，仅应使用该头的最后一个出现位置，因为客户端可能已携带了该头。

关键字 "header" 可用于指定一个不同的头名称，以替代默认的 "X-Forwarded-For"。当可能已从其他应用（例如 stunnel）接收到 "X-Forwarded-For" 头时，此功能非常有用，可确保保留原有头信息。此外，若后端服务器不使用 "X-Forwarded-For" 头，而需要其他头（例如 Zeus Web 服务器要求使用 "X-Cluster-Client-IP"），也可通过此方式指定。

有时，同一个 HAProxy 实例可能同时用于直接客户端访问和反向代理访问（例如，当使用 SSL 反向代理解密 HTTPS 流量时）。可以通过添加 "except" 关键字并指定网络地址，禁用对已知源地址或网络的头信息添加。在此情况下，任何与该网络匹配的源 IP 都不会触发该头信息的添加。常见用法包括私有网络或 127.0.0.1。支持 IPv4 和 IPv6。

此外，关键字 "if-none" 表示仅当该头不存在时才添加该头。
此选项仅应在完全可信的环境中使用，因为如果传入 HAProxy 的头由终端用户控制，可能会引发安全问题。

该选项可在前端或后端中指定。若其中至少一个使用了该选项，将添加对应头信息。请注意，若前端和后端均定义了该头信息的子参数，则后端的设置优先于前端。对于 "if-none" 参数，若前端或后端中至少有一方未指定该参数，则其要求添加操作为强制性，因此该方优先。

示例：

```shell
# Public HTTP address also used by stunnel on the same machine
frontend www
    mode http
    option forwardfor except 127.0.0.1  # stunnel already adds the header

# Those servers want the IP Address in X-Client
backend www
    mode http
    option forwardfor header X-Client
```

另请参阅：“option httpclose”、“option http-server-close”、“option http-keep-alive”

<a id="entry-4-2-option-h1-case-adjust-bogus-client"></a>

**`option h1-case-adjust-bogus-client`**

```haproxy
option h1-case-adjust-bogus-client
no option h1-case-adjust-bogus-client
```

启用或禁用向伪造客户端发送的 HTTP/1 头的大小写调整

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

由于 RFC7230 明确指出，头名称没有标准大小写形式，因此其大小写不敏感。
应用程序必须以不区分大小写的方式处理头名称。
但某些不合规的应用程序违反标准，错误地依赖浏览器通常使用的大小写形式。
这一问题在 HTTP/2 中变得尤为关键，因为所有头名称必须以小写形式传输，HAProxy 也遵循相同约定。
无论 HTTP 版本为何，所有头名称均以小写形式发送给客户端和服务器。

当 HAProxy 收到 HTTP/1 响应时，其头名称会被转换为小写形式，经处理后以该格式发送给客户端。若已知某客户端违反 HTTP 标准，且无法正确处理来自 HAProxy 的响应，则可通过启用此选项，并使用全局指令 h1-case-adjust 或 h1-case-adjust-file 指定需重新格式化的头列表，将小写头名称转换为其他格式后再发送给客户端。此操作仅应作为临时解决方案，待客户端修复期间使用，因为依赖此类 workaround 的客户端可能易受内容伪装攻击，必须彻底修复。

请注意，此选项不会影响符合标准的客户端。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：“option h1-case-adjust-bogus-server”、“h1-case-adjust”、“h1-case-adjust-file”。

<a id="entry-4-2-option-h1-case-adjust-bogus-server"></a>

**`option h1-case-adjust-bogus-server`**

```haproxy
option h1-case-adjust-bogus-server
no option h1-case-adjust-bogus-server
```

启用或禁用向伪造服务器发送的 HTTP/1 头的大小写调整

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

由于 RFC7230 明确指出，头名称没有标准大小写形式，因此其大小写不敏感。
应用程序必须以不区分大小写的方式处理头名称。
但某些不合规的应用程序违反标准，错误地依赖浏览器通常使用的大小写形式。
这一问题在 HTTP/2 中变得尤为关键，因为所有头名称必须以小写形式传输，HAProxy 也遵循相同约定。
无论 HTTP 版本为何，所有头名称均以小写形式发送给客户端和服务器。

当 HAProxy 收到 HTTP/1 请求时，其请求头名称会被转换为小写形式，并以该格式发送至服务器。若已知某服务器违反 HTTP 标准，无法正确处理来自 HAProxy 的请求，则可通过启用此选项，并使用全局指令 `h1-case-adjust` 或 `h1-case-adjust-file` 指定需重新格式化的请求头列表，将小写请求头名称转换为其他格式后再发送至服务器。此操作仅应作为临时解决方案，用于等待服务器修复的过渡期间，因为依赖此类 workaround 的服务器可能易受内容伪装攻击，必须彻底修复。

请注意，此选项不会影响符合标准的服务器。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：“option h1-case-adjust-bogus-client”、“h1-case-adjust”、“h1-case-adjust-file”。

<a id="entry-4-2-option-http-buffer-request"></a>

**`option http-buffer-request`**

```haproxy
option http-buffer-request
no option http-buffer-request
```

启用或禁用在继续处理前等待接收完整的 HTTP 请求体

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

有时需要在获取 HTTP 请求体之后再做出决策。例如，“balance url_param” 就是这样做的。第一个用例是在连接到服务器之前，缓冲来自慢速客户端的请求。第二个用例是根据请求体的内容做出路由决策。在前端或后端中设置此选项，将强制 HTTP 处理等待，直到接收完整个请求体或请求缓冲区已满。对于某些滥用 HTTP 协议、期望前端与后端之间实现无缓冲传输的应用程序，此选项可能产生不良副作用，因此应务必避免默认启用。

另请参阅：“option http-no-delay”、“timeout http-request”、“http-request wait-for-body”

<a id="entry-4-2-option-http-drop-request-trailers"></a>

**`option http-drop-request-trailers`**

```haproxy
option http-drop-request-trailers
no option http-drop-request-trailers
```

从请求发送至服务器时移除 HTTP trailers

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| no \| yes

参数：无

启用此选项后，请求中发现的任何 HTTP 追随者（trailers）将在发送至服务器前被丢弃。

RFC9110#section-6.5.1 指出，尾部字段可以与头字段合并。这应为有意为之，但可能对某些应用程序造成问题，尤其是当恶意客户端将敏感头字段隐藏在尾部部分，而某些中间节点在未进行特定检查的情况下将其与头字段合并时。在此情况下，可在后端启用此选项，以在将请求发送至服务器前丢弃任何发现的尾部字段。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅："option http-drop-response-trailers"

<a id="entry-4-2-option-http-drop-response-trailers"></a>

**`option http-drop-response-trailers`**

```haproxy
option http-drop-response-trailers
no option http-drop-response-trailers
```

从响应中移除 HTTP trailers 后再发送给客户端

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

此选项与“option http-drop-request-trailers”类似，但必须用于在向客户端发送响应前丢弃响应中的尾部字段。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅："option http-drop-request-trailers"

<a id="entry-4-2-option-http-ignore-probes"></a>

**`option http-ignore-probes`**

```haproxy
option http-ignore-probes
no option http-ignore-probes
```

启用或禁用对空连接和请求超时的日志记录

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

最近，一些浏览器开始实现“预连接”功能，即在用户可能访问最近浏览过的网站时，预先建立连接。这导致大量连接被建立到网站，若超时先触发，则结果为 408 请求超时；若浏览器先决定关闭连接，则结果为 400 错误请求。这些情况会污染日志并增加错误计数器。虽然已有“option dontlognull”，但在此场景下仍不充分。相反，此选项执行以下操作：— 若连接关闭前未收到任何数据，则阻止向客户端发送任何 400/408 消息；— 在此情况下阻止生成任何日志；— 阻止任何错误计数器被递增

这样，空连接将被静默忽略。请注意，除非明确需要，否则不建议使用此选项，因为它会隐藏真实问题。未收到请求并看到 408 错误的最常见原因是客户端与中间设备（如 VPN）之间存在 MTU 不一致，导致过大数据包被阻断。此类问题通常也出现在 POST 请求以及携带大 Cookie 的 GET 请求中。日志通常是检测此类问题的唯一途径。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：“log”、“dontlognull”、“errorfile”以及 [第 8 节](/zh/haproxy/configuration-logging/) 中关于日志记录的内容。

<a id="entry-4-2-option-http-keep-alive"></a>

**`option http-keep-alive`**

```haproxy
option http-keep-alive
no option http-keep-alive
```

启用或禁用客户端到服务器的 HTTP/1.x 连接中的 HTTP 持久连接

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

默认情况下，HAProxy 以持久连接模式处理 HTTP/1.x 的持久连接：对于每个连接，它会处理每个请求和响应，并在两端保持连接空闲。可通过多个选项更改此模式，例如“option http-server-close”或“option httpclose”。此选项可恢复持久连接模式，当在 defaults 段中使用了其他模式时，此功能尤为有用。

设置 "option http-keep-alive" 可在客户端和服务器端启用 HTTP 持久连接模式。该模式在客户端侧可实现最低延迟（尤其适用于慢速网络），在服务器侧可实现最快会话复用，但需以维持与服务器的空闲连接为代价。通常情况下，使用此选项可使小对象的请求速率大约达到 "http-server-close" 选项的两倍。此选项主要适用于以下两种场景：

    - 当服务器不遵循 HTTP 规范且对连接而非请求进行认证时（例如 NTLM
      认证）；

    - 当与服务器的连接建立开销相较于从服务器获取相关对象的开销更为显著
      时。

最后一种情况可能出现在服务器是快速静态缓存服务器时。

目前，日志不会标明请求是否来自同一会话。日志中报告的接受时间对应于前一个请求的结束时间，请求时间对应于等待新请求所花费的时间。若未设置，持久连接的请求时间仍受 "timeout http-keep-alive" 或 "timeout http-request" 定义的超时限制。

此选项会禁用并替换任何先前配置的 "option httpclose" 或 "option http-server-close"。

另请参阅：“option httpclose”、“option http-server-close”、“option prefer-last-server”和“option http-pretend-keepalive”。

<a id="entry-4-2-option-http-no-delay"></a>

**`option http-no-delay`**

```haproxy
option http-no-delay
no option http-no-delay
```

指示系统在 HTTP 中优先考虑较低的交互延迟，而非性能。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

在 HTTP 中，每个数据负载均为单向传输，且不涉及交互性概念。任何代理都应合理地对数据进行排队，以保证较低的延迟。极少数服务器到服务器的应用程序滥用 HTTP 协议，期望数据负载阶段具有高度交互性，即在单个请求中双向交错传输大量数据块。这完全不符合 HTTP 规范，且在大多数代理或服务器上无法正常工作。当此类应用程序通过 HAProxy 尝试实现时，虽然可以运行，但由于网络优化机制倾向于通过等待足够数据以发送完整数据包来提升性能，因此会遭遇显著延迟。典型延迟约为每往返一次 200 毫秒。请注意，这种情况仅出现在异常使用场景中。正常使用场景，如 CONNECT 请求或 WebSocket，不受影响。

当“option http-no-delay”出现在连接所使用的前端或后端中时，所有此类优化都将被禁用，以实现最快的数据交换。当然，这并不能保证功能正常，因为可能在其他任何位置出现故障。但如果应用程序通过 HAProxy 可以正常工作，那么其性能将达到最优。该选项不应默认启用，除非发现存在此类缺陷的应用程序，否则不应使用。启用该选项会导致带宽和 CPU 使用率上升，在高延迟环境中可能显著降低性能。

另请参阅："option http-buffer-request"

<a id="entry-4-2-option-http-pretend-keepalive"></a>

**`option http-pretend-keepalive`**

```haproxy
option http-pretend-keepalive
no option http-pretend-keepalive
```

定义 HAProxy 是否向服务器通告 HTTP/1.x 连接的保持连接状态。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

当启用 "option http-server-close" 或 "option httpclose" 时，HAProxy 会在转发至服务器的 HTTP/1.x 请求中添加 "Connection: close" 头。不幸的是，当某些服务器检测到该头时，会自动停止对长度未知的响应使用分块编码，而这一行为与实际无关。结果是，客户端或缓存可能接收到不完整的响应却未察觉，误认为响应已完整。

通过设置 "option http-pretend-keepalive"，HAProxy 会令服务器误以为连接将保持活跃。服务器因此不会回退到上述异常的非期望状态。当 HAProxy 收到完整的响应后，将关闭与服务器的连接，其行为与启用 "option httpclose" 时一致。这样，客户端可获得正常的响应，且服务器端的连接得以正确关闭。

建议默认情况下不要启用此选项，因为大多数服务器在收到最后一个数据包后会更高效地自行关闭连接，并略微提前释放其缓冲区。此外，网络中增加的数据包可能会略微降低整体峰值性能。然而需要注意的是，启用此选项后，HAProxy 需要完成的工作量会略微减少。因此，如果 HAProxy 是整个架构中的性能瓶颈，启用此选项可能节省少量 CPU 周期。

该选项可在后端和 listen 段中设置。在前端段中使用将被忽略，并在启动时报告警告。此选项与后端相关，因此在前端设置并无实际意义。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：“option httpclose”、“option http-server-close” 和 “option http-keep-alive”

<a id="entry-4-2-option-http-restrict-req-hdr-names"></a>

**`option http-restrict-req-hdr-names { preserve | delete | reject }`**

```haproxy
option http-restrict-req-hdr-names { preserve | delete | reject }
```

设置 HAProxy 对包含非 "[a-zA-Z0-9-]" 字符集字符的 HTTP 请求头名称的处理策略

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
preserve  禁用过滤。这是未配置 FastCGI 应用程序的 HTTP 代理的默认模式。

delete    移除头名称包含 "[a-zA-Z0-9-]" 字符集以外字符的请求头。
          这是配置了 FastCGI 应用程序的 HTTP 后端的默认模式。

reject    若请求的头名称包含 "[a-zA-Z0-9-]" 字符集以外的字符，则以 403-Forbidden 响应拒绝请求。
```

此选项可用于限制请求头名称仅包含字母、数字和连字符字符（[A-Za-z0-9-]）。在与不遵循 HTTP 协议的服务器互操作时，此限制可能是必须的，因为这些服务器无法正确处理头名称中的某些字符。对于 FastCGI 应用程序而言，此限制也可能为必须，因为头名称中所有非字母数字字符均会被下划线替换（'\_'）。因此，很容易混淆头名称并绕过某些规则。例如，“X-Forwarded-For” 和 "X_Forwarded-For" 头均会被转换为 "HTTP_X_FORWARDED_FOR"。

请注意，此选项按代理逐个评估，且在完成 http-request 规则评估之后进行。

<a id="entry-4-2-option-http-server-close"></a>

**`option http-server-close`**

```haproxy
option http-server-close
no option http-server-close
```

在服务器端启用或禁用 HTTP/1.x 连接关闭

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

默认情况下，HAProxy 以持久连接模式运行，针对持久的 HTTP/1.x 连接：对于每个连接，HAProxy 会处理每个请求和响应，并在两端保持连接空闲。可通过多个选项更改此模式，例如“option http-server-close”或“option httpclose”。设置“option http-server-close”可在服务器端启用 HTTP connection-close 模式，同时保留客户端侧支持 HTTP 持久连接和流水线化的能力。该模式可实现客户端侧（慢速网络）最低延迟，并在服务器端实现最快会话复用，以节省服务器资源，与“option httpclose”效果类似。此外，只要服务器符合 RFC7230 的要求，该模式还允许非持久连接能力的服务器以持久连接模式向客户端提供服务。请注意，部分服务器在收到请求中的“Connection: close”时，可能并不完全符合这些要求。其结果是持久连接将永远无法使用。一种解决方法是启用“option http-pretend-keepalive”。

目前，日志不会标明请求是否来自同一会话。日志中报告的接受时间对应于前一个请求的结束时间，请求时间对应于等待新请求所花费的时间。若未设置，持久连接的请求时间仍受 "timeout http-keep-alive" 或 "timeout http-request" 定义的超时限制。

该选项可在前端和后端中设置。若持有连接的前端或后端中至少有一个启用了此选项，则该选项生效。启用后将禁用并替换任何先前配置的“option httpclose”或“option http-keep-alive”。请查阅 [第 4 节](/zh/haproxy/proxies/)（“代理”）了解当前端与后端选项不同时，此选项如何与其他选项协同工作。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：“option httpclose”、“option http-pretend-keepalive” 和 “option http-keep-alive”。

<a id="entry-4-2-option-http-use-proxy-header"></a>

**`option http-use-proxy-header`**

```haproxy
option http-use-proxy-header
no option http-use-proxy-header
```

使用非标准的 Proxy-Connection 头代替 Connection 头

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

根据 RFC7230 明确规定，HTTP/1.1 代理必须使用 Connection 头来表明其希望维持持久连接或非持久连接。然而，浏览器和代理在代理连接中均忽略该头，并改用未公开、非标准的 Proxy-Connection 头。当尝试在浏览器与此类代理之间部署负载均衡器时，问题便随之产生，因为 HAProxy 所理解的行为与客户端和代理之间所达成的共识存在差异。

通过在前端中设置此选项，HAProxy 可在检测到代理请求时自动切换至使用该非标准头。此处定义的代理请求是指 URI 既不以 '/' 也不以 '\*' 开头的请求。此选项与 HTTP 隧道模式不兼容。请注意，该选项只能在前端中指定，并将影响请求的整个生命周期。

此外，当设置此选项时，若请求需要认证，且该请求本身是通过代理转发的，则会自动切换为使用代理认证头。这使得可在现有代理前端检查或强制执行认证。

此选项通常不应使用，仅在代理前端使用时例外。

另请参阅：“option httpclose” 和 “option http-server-close”。

<a id="entry-4-2-option-httpchk"></a>

**`option httpchk`**

```haproxy
option httpchk
option httpchk <uri>
option httpchk <method> <uri>
option httpchk <method> <uri> <version>
option httpchk <method> <uri> <version> <host>
```

启用 HTTP 协议检查服务器健康状态

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<method>  是请求使用的可选 HTTP 方法。未设置时使用 "OPTIONS"，因为此方法通常处理开销较低，
          且容易从日志中过滤掉。可使用任何方法，但不建议自行创建非标准方法。

<uri>     是 HTTP 请求引用的 URI，默认值为 " / "，几乎任何服务器均默认可访问；
          也可改为任何其他 URI，允许包含查询字符串。

<version> 是可选的 HTTP 版本字符串，默认值为 "HTTP/1.0"。
          某些服务器在 HTTP 1.0 下可能行为异常，改用 HTTP/1.1 有时会有帮助。
          注意，HTTP/1.1 要求必须提供 Host 字段。

<host>    是可选的 HTTP Host 头值，默认未设置。它是日志格式字符串。
```

默认情况下，服务器健康检查仅包含尝试建立 TCP 连接。当指定 "option httpchk" 时，在建立 TCP 连接后会发送完整的 HTTP 请求，响应码为 2xx 或 3xx 被视为有效，而所有其他响应均表示服务器故障，包括无任何响应的情况。

与 "http-check" 指令结合使用时，可自定义 HTTP 健康检查期间发送的请求，或配置对响应的匹配规则。也可配置 send/expect 序列，方式与 TCP 健康检查中的 "tcp-check" 指令相同。

默认情况下，服务器配置用于打开连接以执行 HTTP 健康检查。也可通过使用 "http-check connect" 规则覆盖服务器参数。

`httpchk` 选项并不要求必须使用 HTTP 后端，它同样适用于普通的 TCP 后端。这在使用 inetd 守护进程绑定到特定端口的简单脚本检测时尤为有用。然而，它始终内部依赖 HTX 多路复用器。因此，这意味着请求格式化和响应解析将严格遵循规范。

示例：

```shell
# Relay HTTPS traffic to Apache instance and check service availability
# using HTTP request "OPTIONS * HTTP/1.1" on port 80.
backend https_relay
    mode tcp
    option httpchk OPTIONS * HTTP/1.1
    http-check send hdr Host www
    server apache1 192.168.1.1:443 check port 80
```

另请参阅：`option ssl-hello-chk`、`option smtpchk`、`option mysql-check`、`option pgsql-check`、`http-check` 以及 `check`、`port` 和 `inter` 服务器选项。

<a id="entry-4-2-option-httpclose"></a>

**`option httpclose`**

```haproxy
option httpclose
no option httpclose
```

启用或禁用 HTTP/1.x 连接关闭

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

默认情况下，HAProxy 以持久连接模式运行，针对持久的 HTTP/1.x 连接：每个连接在处理完每个请求和响应后，会在两端保持空闲状态。可通过多个选项更改此模式，例如 "option http-server-close" 或 "option httpclose"。

若设置 "option httpclose"，HAProxy 将根据该选项的设置位置关闭客户端或服务器连接。前端用于客户端连接，后端用于服务器连接。若在监听器上设置该选项，则同时作用于客户端和服务器连接。HAProxy 会检查每个方向是否已设置 "Connection: close" 头，若缺失则添加。

此选项还可与 "option http-pretend-keepalive" 一同使用，该选项将禁用发送 "Connection: close" 请求头，但接收完整响应后仍会关闭连接。

它会禁用并替换任何先前配置的 "option http-server-close" 或 "option http-keep-alive"。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅："option http-server-close"。

<a id="entry-4-2-option-httplog"></a>

**`option httplog [ clf ]`**

```haproxy
option httplog [ clf ]
```

启用 HTTP 请求、流状态和计时器的日志记录

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
clf       添加 "clf" 参数后，输出采用 CLF 格式，而非 HAProxy 默认的 HTTP 格式。
          当需要将 HAProxy 日志交给仅支持 CLF 格式且无法扩展的特定日志分析器时，可使用此项。
```

默认情况下，日志输出格式非常简陋，仅包含源地址和目标地址以及实例名称。通过指定 "option httplog"，每行日志将变为更丰富的格式，包括但不限于：HTTP 请求、连接计时器、流状态、连接数量、捕获的头字段和 Cookie、前端、后端及服务器名称，当然还包括源地址和端口。

仅指定 "option httplog" 时，将自动清除默认设置的 'clf' 模式。

"option httplog" 会覆盖之前设置的 "log-format" 指令。

另请参阅 [第 8 节](/zh/haproxy/configuration-logging/) 中关于日志记录的内容。

<a id="entry-4-2-option-httpslog"></a>

**`option httpslog`**

```haproxy
option httpslog
```

启用 HTTPS 请求、流状态及计时器的日志记录

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

默认情况下，日志输出格式非常简陋，仅包含源地址和目标地址以及实例名称。通过指定 "option httpslog"，每行日志将变为更丰富的格式，包括但不限于：HTTP 请求、连接计时器、流状态、连接数量、捕获的头和 Cookie、前端、后端和服务器名称、SSL 证书验证状态和 SSL 握手状态，以及当然的源地址和端口。

"option httpslog" 会覆盖之前所有的 "log-format" 指令。

另请参阅 [第 8 节](/zh/haproxy/configuration-logging/) 中关于日志记录的内容。

<a id="entry-4-2-option-idle-close-on-response"></a>

**`option idle-close-on-response`**

```haproxy
option idle-close-on-response
no option idle-close-on-response
```

如果正在进行软停止，则避免关闭空闲的前端连接

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

默认情况下，软停止期间空闲连接将被关闭。在某些环境中，客户端与代理之间可能已建立一些空闲连接，以便稍后发送请求。如果未对写入错误进行适当的重试，这可能导致 HAProxy 重载时出现错误。尽管正确的实现应在连接或写入错误时重试，但此选项的引入是为了支持与 2.4 版本之前 HAProxy 的向后兼容性。事实上，在 2.4 版本之前，HAProxy 会在关闭连接前等待最后一个请求和响应，并添加 "Connection: close" 头，从而通知客户端该连接不可重用。

在实际案例中，此行为曾在 AWS 环境下观察到，即在 HAProxy 前端部署 ALB 时出现。最终结果为 ALB 在 HAProxy 重载期间返回 502 错误。

请注意，使用此选项可能导致连接空闲时间过长时旧进程数量增加。在频繁重载的情况下，可能需要相应调整客户端超时设置和/或“hard-stop-after”参数。

另请参阅：“timeout client”、“timeout client-fin”、“timeout http-request”、“hard-stop-after”

<a id="entry-4-2-option-independent-streams"></a>

**`option independent-streams`**

```haproxy
option independent-streams
no option independent-streams
```

启用或禁用双向独立超时处理

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

默认情况下，当通过套接字发送数据时，该套接字的写超时和读超时都会被刷新，因为我们认为该套接字存在活动，且没有其他方式判断是否应接收数据。

当大多数应用程序均期望此默认行为时，仍存在一种情形下希望禁用该行为，仅在有传入数据时才刷新读取超时。这种情况常见于超时时间较长且交换数据量较小的流，例如 telnet 会话。若服务器突然消失，输出数据会累积在系统的套接字缓冲区中，两个超时均会被正确刷新，但无法得知服务器是否已无法接收这些数据，因此不会触发超时。然而，当底层协议始终回显已发送的数据时，仅通过读取超时即可自行检测该问题。请注意，该问题不会出现在更冗余的协议中，因为数据不会在套接字缓冲区中长时间累积。

当此选项在前端设置时，将禁用向客户端发送数据时的读取超时更新。此情况可能用途有限。当此选项在后端设置时，将禁用向服务器发送数据时的读取超时更新。此举通常会导致慢速链路上的大规模 HTTP 上传失败，因此应谨慎使用。

另请参阅：“timeout client”、“timeout server” 和 “timeout tunnel”

<a id="entry-4-2-option-ldap-check"></a>

**`option ldap-check`**

```haproxy
option ldap-check
```

使用 LDAPv3 健康检查测试服务器

可用于以下上下文：tcp

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

可以测试服务器是否正确使用 LDAPv3 协议，而不仅仅是测试其是否接受 TCP 连接。启用此选项后，会向服务器发送 LDAPv3 匿名简单绑定消息，并分析响应以确认是否收到 LDAPv3 绑定响应消息。

仅当 LDAP 响应包含成功 resultCode（<http://tools.ietf.org/html/rfc4511#section-4.1.9>）时，服务器才被视为有效。

绑定请求的日志记录取决于服务器，具体配置方法请参阅相关文档。

示例：

```text
option ldap-check
```

另请参阅："option httpchk"

<a id="entry-4-2-option-log-health-checks"></a>

**`option log-health-checks`**

```haproxy
option log-health-checks
no option log-health-checks
```

启用或禁用健康检查状态更新的日志记录

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

默认情况下，当服务器处于 UP 状态时，会记录失败的健康检查；当服务器处于 DOWN 状态时，会记录成功的健康检查，因此额外信息的记录量有限。

当启用此选项时，健康检查状态或服务器健康状况的任何变化都将被记录，从而能够知晓某服务器在崩溃前是否曾间歇性地检查失败，或确切地了解其何时未能响应有效的 HTTP 状态，何时端口开始拒绝连接，以及何时服务器完全停止响应。

请注意，由健康检查以外的原因引起的状态变更（例如通过 CLI 执行的启用/禁用操作）不会被此选项记录。

另请参阅：“option httpchk”、“option ldap-check”、“option mysql-check”、“option pgsql-check”、“option redis-check”、“option smtpchk”、“option tcp-check”、“log”以及 [第 8 节](/zh/haproxy/configuration-logging/) 关于日志记录的内容。

<a id="entry-4-2-option-log-separate-errors"></a>

**`option log-separate-errors`**

```haproxy
option log-separate-errors
no option log-separate-errors
```

更改非完全成功连接的日志级别

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

有时在日志中查找错误并不容易。此选项可提升包含潜在重要信息的日志级别，例如错误、超时、重试、重分派或 HTTP 状态码 5xx。日志级别将从“info”提升至“err”。这使得大多数 syslog 守护进程能够将这些日志单独记录到不同的文件中。请注意，不要从原始文件中移除这些日志，否则将丢失顺序信息，而顺序信息提供了非常重要的上下文。

使用此选项，处理每秒数千个连接的大型站点可将正常流量日志记录至循环缓冲区，仅归档较小的错误日志。

另请参阅：“log”、“dontlognull”、“dontlog-normal”以及 [第 8 节](/zh/haproxy/configuration-logging/) 中关于日志记录的内容。

<a id="entry-4-2-option-logasap"></a>

**`option logasap`**

```haproxy
option logasap
no option logasap
```

启用或禁用早期日志记录。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

默认情况下，当日志格式别名和样本提取项在日志格式字符串定义中全部返回值，或流终止时，将输出日志。这使得内置日志格式字符串能够计入传输时间，或日志消息中的字节数。

当处理长连接（如大文件传输或 RDP）时，请求或连接在日志中出现可能需要较长时间。使用 "option logasap" 选项后，日志消息将在 TCP 模式下服务器连接建立时，或 HTTP 模式下服务器发送完整头信息时立即生成。日志中缺失的信息包括总字节数，该值仅反映消息生成前已传输的数据量，以及总时间，该值未计入连接剩余生命周期或传输时间。对于 HTTP 情况，建议捕获 Content-Length 响应头，以便日志至少能指示预期传输的字节数。

示例：

```text
listen http_proxy 0.0.0.0:80
    mode http
    option httplog
    option logasap
    log 192.168.2.200 local3
```

```text
    >>> Feb  6 12:14:14 localhost \
          haproxy[14389]: 10.0.1.2:33317 [06/Feb/2009:12:14:14.655] http-in \
          static/srv1 9/10/7/14/+30 200 +243 - - ---- 3/1/1/1/0 1/0 \
          "GET /image.iso HTTP/1.0"
```

另请参阅："option httplog"、"capture response header"，以及 [第 8 节](/zh/haproxy/configuration-logging/) 关于日志记录的内容。

<a id="entry-4-2-option-mysql-check"></a>

**`option mysql-check [ user <username> [ { post-41 | pre-41 | post-80 } ] ]`**

```haproxy
option mysql-check [ user <username> [ { post-41 | pre-41 | post-80 } ] ]
```

使用 MySQL 健康检查对服务器进行测试

可用于以下上下文：tcp

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<username> 是连接 MySQL 服务器时使用的用户名。
post-41    发送兼容 v4.1 之后客户端的检查（默认值）。
pre-41     发送兼容 v4.1 之前客户端的检查。
post-80    发送兼容 v8.0 之后客户端的检查，设置 CLIENT_PLUGIN_AUTH 能力，
           并使用 mysql_native_password 认证插件。
           连接 MySQL 8.0+ 服务器且健康检查用户使用 mysql_native_password 认证时，使用此选项。例如：
             CREATE USER 'haproxy'@'%' IDENTIFIED WITH mysql_native_password BY '';
```

若指定用户名，检查过程将发送两个 MySQL 数据包：一个客户端认证数据包和一个 QUIT 数据包，以正确关闭 MySQL 会话。随后，解析 MySQL 握手初始化数据包和/或错误数据包。这是一种基础但实用的测试，不会在服务器端产生错误或中断连接。然而，该测试要求存在一个未锁定且无密码的授权用户。要在 MySQL 中创建一个基本的受限用户并可选地设置资源限制：

```text
CREATE USER '<username>'@'<ip_of_haproxy|network_of_haproxy/netmask>'
/*!50701 WITH MAX_QUERIES_PER_HOUR 1 MAX_UPDATES_PER_HOUR 0 */
/*M!100201 MAX_STATEMENT_TIME 0.0001 */;
```

如果不指定用户名（该做法已弃用且不推荐），检查仅包括解析 MySQL 握手初始化数据包或错误数据包，此模式下不会发送任何内容。有报告指出，若检查频率过高和/或流量不足，可能导致锁定。实际上，在此情况下，需检查 MySQL "max_connect_errors" 值，即如果在前一次连接中断后，服务器在少于 MySQL "max_connect_errors" 次尝试内成功建立连接，则该主机的错误计数将被清零。若 HAProxy 服务器被阻塞，“FLUSH HOSTS” 语句是解除阻塞的唯一方法。

请注意，这不会检查数据库是否存在或数据库一致性。如需执行此类检查，可以使用 xinetd 等外部检查工具。

该检查要求 MySQL 版本 ≥ 3.22，对于较旧版本，请使用 TCP 检查。

通常情况下，传入的 MySQL 服务器需要看到客户端的 IP 地址，以实现多种用途，包括 IP 权限匹配和连接日志记录。在可能的情况下，建议在通过 "source" 关键字的 "usesrc" 参数连接服务器时，对客户端 IP 地址进行伪装，这需要透明代理功能已编译启用，并且 MySQL 服务器需通过运行 HAProxy 的主机来路由客户端连接。

另请参阅："option httpchk"

<a id="entry-4-2-option-nolinger"></a>

**`option nolinger`**

```haproxy
option nolinger
no option nolinger
```

启用或禁用会话关闭后立即清理资源

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

当客户端或服务器以非正常方式中止连接（例如，物理断开连接）时，会话超时将被触发，会话随之关闭。但该会话将在系统中保持 FIN_WAIT1 状态一段时间，占用部分资源，并可能限制建立新连接的能力。

当发生此情况时，可以启用“option nolinger”选项，强制系统在关闭连接时立即清除套接字中待处理的数据。此时会发出 TCP RST，待处理数据被截断，会话将立即从系统的表中清除。对客户端而言，通常可见的效果是：若关闭操作发生在最后一个数据块时（例如重定向或错误响应），响应数据会被截断。在服务器端，当通过隧道转发时，若客户端中断连接，该选项有助于立即释放源端口。两种情况下均会发出 TCP 重置，由于会话被立即销毁，因此不会发生重传。在丢包率较高的网络中，这可能加剧问题，尤其是在丢包侧存在防火墙时，因为防火墙可能接收到并处理该重置（从而清除其会话状态），并阻止该会话的后续流量，包括来自另一侧的重传数据。因此，若另一侧未收到该重置，将永远无法再次接收 RST，而防火墙可能会记录大量被阻断的数据包。

出于上述所有原因，强烈建议不要使用此选项，除非在万不得已的情况下作为最后手段。在大多数场景中，使用 "client-fin" 或 "server-fin" 超时可实现类似效果，且行为更加可靠。在 Linux 上，还可选择使用 "tcp-ut" 绑定或服务器设置。

该选项可在前端和后端中使用，具体取决于其所需的位置。
在前端使用以处理客户端，在后端使用以处理服务器。
尽管该选项在“defaults”段中技术上受支持，但应避免在此处使用，以免意外传播至本不应使用该选项的段，从而引发问题。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：“timeout client-fin”、“timeout server-fin”、“tcp-ut” 绑定或服务器关键字。

<a id="entry-4-2-option-originalto"></a>

**`option originalto [ except <network> ] [ header <name> ]`**

```haproxy
option originalto [ except <network> ] [ header <name> ]
```

启用向发送至服务器的请求中插入 X-Original-To 头

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<network> 是可选参数，对匹配 <network> 的源禁用此选项。
<name>    是可选参数，指定不同的 "X-Original-To" 头名称。
```

由于 HAProxy 可以工作在透明模式下，客户端的每个请求都可能被重定向至代理，而 HAProxy 本身可将每个请求转发至复杂的 SQUID 环境，此时 SO_ORIGINAL_DST 的目标主机将丢失。当需要基于目标 IP 地址设置访问规则时，这种情况会带来困扰。为解决此问题，HAProxy 可向发送至服务器的所有请求添加新的 HTTP 头 "X-Original-To"。该头包含表示原始目标 IP 地址的值。必须配置为仅使用该头的最后一次出现。请注意，仅应使用该头的最后一次出现，因为客户端可能已携带了该头。

关键字 "header" 可用于指定一个不同的头名称，以替换默认的 "X-Original-To"。当可能已从其他应用接收了 "X-Original-To" 头，且需要保留该头时，此功能非常有用。此外，若后端服务器不使用 "X-Original-To" 头，而需要其他头名称时，也可使用此功能。

有时，同一个 HAProxy 实例可能同时用于直接客户端访问和反向代理访问（例如，当使用 SSL 反向代理解密 HTTPS 流量时）。可以通过添加 "except" 关键字并指定网络地址，禁用对已知目标地址或网络的头字段添加。在此情况下，任何与该网络匹配的目标 IP 都不会触发该头字段的添加。常见用法包括私有网络或 127.0.0.1。支持 IPv4 和 IPv6。

该选项可在前端或后端中指定。若其中至少一个使用了该选项，将添加该头。请注意，若前后端均定义了该头的子参数，后端的设置将优先于前端。

示例：

```shell
# Original Destination address
frontend www
    mode http
    option originalto except 127.0.0.1

# Those servers want the IP Address in X-Client-Dst
backend www
    mode http
    option originalto header X-Client-Dst
```

另请参阅：“option httpclose”、“option http-server-close”。

<a id="entry-4-2-option-persist"></a>

**`option persist`**

```haproxy
option persist
no option persist
```

启用或禁用对已关闭服务器的强制持久化

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

当 HTTP 请求到达一个包含引用已失效服务器的 cookie 的后端时，默认情况下会将其重分派至另一台服务器。若确实需要，可使用“option persist”强制请求首先发送至该已失效服务器。常见应用场景为服务器处于极端负载状态，导致其频繁波动。在此情况下，用户仍会被引导至其会话初始连接的服务器，以期获得正确服务。建议与该选项配合使用“option redispatch”，以便在无法连接至该服务器（服务器已彻底失效）时，最终将客户端重定向至另一台有效服务器。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：“option redispatch”、“retries”、“force-persist”

<a id="entry-4-2-option-pgsql-check-user"></a>

**`option pgsql-check user <username>`**

```haproxy
option pgsql-check user <username>
```

使用 PostgreSQL 健康检查对服务器进行测试

可用于以下上下文：tcp

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<username> 是连接 PostgreSQL 服务器时使用的用户名。
```

该检查发送一个 PostgreSQL StartupMessage，并等待收到 Authentication request 或 ErrorResponse 消息。这是一种基础但实用的测试，不会在服务器端产生错误或中断连接。此检查与 "mysql-check" 完全相同。

另请参阅："option httpchk"

<a id="entry-4-2-option-prefer-last-server"></a>

**`option prefer-last-server`**

```haproxy
option prefer-last-server
no option prefer-last-server
```

允许多个负载均衡的请求保持在同一个服务器上

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

当所使用的负载均衡算法不具备确定性时，若此前请求已发送至 HAProxy 仍保持连接的服务器，则在同一会话中尽可能将后续请求也发送至同一服务器，有时是可取的。请注意，这与持久性不同，因为此处仅表示一种偏好，HAProxy 会尝试应用该偏好，但不提供任何形式的保证。此功能的实际用途在于对服务器发起的持久连接。启用该选项后，HAProxy 将尝试复用与服务器关联的现有连接，而非重新均衡至另一服务器，从而避免关闭连接。该机制对静态文件服务器具有实际意义。与哈希算法结合使用时，此选项意义不大。请注意，当负载均衡算法不具备确定性时，HAProxy 已自动尝试保持与返回 401 响应的服务器或返回 407 响应的代理（需认证）的连接。在处理存在缺陷的 NTLM 认证挑战时，此行为为强制要求，且对排查部分异常应用具有显著帮助。在这些环境中，启用 prefer-last-server 选项也可能有益，以避免每次响应后重新分配流量。

本文档中明确指出，哪些负载均衡算法属于确定性算法较为有用。

确定性算法在可用服务器集合未发生变化的前提下，对给定客户端数据始终选择相同的服务器。通常情况下，确定性算法通过哈希或查找传入请求中的信息来选择目标服务器。然而，这并非总是成立；例如，“static-rr”算法也可视为确定性算法，因为服务器选择基于服务器的静态权重，使得选择结果可预测。“sticky”算法为返回客户端提供确定性路由。

对于非确定性算法，这些算法根据动态服务器状态或简单轮询选择服务器，因此两个连续的请求无法保证落在同一台服务器上。option prefer-last-server 专门为此类算法设计。roundrobin 和 leastconn 即为这类算法的示例。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅："option http-keep-alive"

<a id="entry-4-2-option-redispatch"></a>

**`option redispatch`**

```haproxy
option redispatch
option redispatch <interval>
no option redispatch
```

在连接失败时启用或禁用会话重分派

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<interval> 是可选的整数值，控制连接重试时重分派的频率。
           正值 P 表示每第 P 次重试发生重分派；负值 N 表示在最终重试之前倒数第 N 次重试发生重分派。
           例如，默认值 -1 保留原有行为，在最后一次重试时重分派；
           正值 1 表示每次重试都重分派；正值 3 表示每第三次重试重分派。
           值为 0 时禁用重分派。
```

在 HTTP 模式下，如果客户端通过 Cookie 指定的服务器宕机，客户端可能会持续连接到该服务器，例如使用 "option persist" 或 "force-persist" 时，因为客户端无法清除 Cookie，将无法再访问服务。

启用 "option redispatch" 可使代理打破基于 cookie 或一致性哈希的持久性，将请求重新分派至可用的服务器。

从可用服务器列表的子集中选择活跃服务器。未处于宕机或维护状态（即未进行健康检查，或已被检查为“正常”）的活跃服务器，按以下顺序进行选择：

```text
1. 任何活跃的非备用服务器（若有），否则

2. 若未设置 "allbackups" 选项，则为列表中的第一个备用服务器，否则

3. 若设置了 "allbackups" 选项，则为任何备用服务器。
```

重试时，HAProxy 会尝试选择除上一次以外的另一台服务器。新服务器将从当前服务器列表中选取。

有时，如果在重试期间更新了列表（例如，发生大量重试且耗时超过检查服务器是否已宕机所需的时间，导致将其从列表中移除并回退到备用服务器列表），连接仍可能被重定向至备用服务器。

它还允许在发生多次连接失败时，重试连接到另一台服务器。当然，这要求将“retries”设置为非零值。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅："option persist"、"force-persist"、"retries"

<a id="entry-4-2-option-redis-check"></a>

**`option redis-check`**

```haproxy
option redis-check
```

使用 Redis 健康检查对服务器进行测试

可用于以下上下文：tcp

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

可以测试服务器是否正确使用 REDIS 协议，而不仅仅是测试其是否接受 TCP 连接。启用此选项后，HAProxy 会向服务器发送 PING REDIS 命令，并分析响应以查找 "+PONG" 响应消息。

示例：

```text
option redis-check
```

另请参阅："option httpchk"、"option tcp-check"、"tcp-check expect"

<a id="entry-4-2-option-smtpchk"></a>

**`option smtpchk`**

```haproxy
option smtpchk
option smtpchk <hello> <domain>
```

使用 SMTP 健康检查测试服务器

可用于以下上下文：tcp

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<hello>   是可选参数，指定使用的 "hello" 命令，可为 "HELO"（SMTP）或 "EHLO"（ESMTP）。
          所有其他值均转换为默认命令（"HELO"）。

<domain>  是向服务器通告的域名，仅在指定了 hello 命令时才能设置（此时必须设置）。
          默认使用 "localhost"。
```

当设置 "option smtpchk" 时，健康检查将包含 TCP 连接后跟一个 SMTP 命令。默认情况下，该命令为 "HELO localhost"。服务器返回的响应码将被分析，仅以 "2" 开头的响应码被视为有效。所有其他响应，包括无响应的情况，均视为错误，并表示服务器已失效。

此测试适用于 SMTP 服务器或中继。根据请求的不同，某些服务器可能不会记录每次连接尝试，因此建议进行试验以优化行为。使用 telnet 连接端口 25 通常比调整配置更简便。

大多数情况下，传入的 SMTP 服务器需要查看客户端的 IP 地址，以实现多种目的，包括垃圾邮件过滤、防伪造和日志记录。在可能的情况下，建议在使用 "source" 关键字的 "usesrc" 参数连接服务器时，对客户端 IP 地址进行伪装，这需要编译时启用透明代理功能。

示例：

```text
option smtpchk HELO mydomain.org
```

另请参阅："option httpchk"、"source"

```haproxy
option socket-stats
no option socket-stats
```

启用或禁用为每个套接字单独收集和提供统计信息。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

<a id="entry-4-2-option-splice-auto"></a>

**`option splice-auto`**

```haproxy
option splice-auto
no option splice-auto
```

启用或禁用套接字在两个方向上的自动内核加速

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

当在前端或后端启用此选项时，HAProxy 将自动评估是否可利用内核 TCP 拼接技术在客户端与服务器之间双向转发数据。HAProxy 使用启发式算法估算拼接是否可能提升性能。两个方向的处理相互独立。请注意，所采用的启发式算法并不激进，以避免拼接的过度使用。此选项要求在编译时启用拼接功能，并可通过全局选项 "nosplice" 全局禁用。由于拼接使用管道，因此使用该功能需确保有足够的空闲管道。

重要提示：基于内核的 TCP 拼接是 Linux 特有的功能，最早出现在内核 2.6.25 版本中。该功能通过在内核层面直接在套接字之间传输数据，无需将数据复制到用户空间，从而显著提升性能并节省 CPU 周期。由于早期实现存在缺陷，可能导致数据损坏或效率低下，因此该功能默认未启用，使用时应格外谨慎。尽管无法检测实现的正确性，但 2.6.29 版本是首个提供正确实现的版本。如有疑问，可使用全局配置项 "nosplice" 全局禁用拼接功能。

示例：

```text
option splice-auto
```

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：`option splice-request`、`option splice-response` 以及全局选项 `nosplice` 和 `maxpipes`

<a id="entry-4-2-option-splice-request"></a>

**`option splice-request`**

```haproxy
option splice-request
no option splice-request
```

启用或禁用请求的套接字自动内核加速

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

当在前端或后端启用此选项时，HAProxy 将尽可能使用内核 TCP 拼接技术，将客户端到服务器的数据直接转发。若无可用的管道资源，仍可能采用 recv/send 方式。此选项需在编译时启用拼接功能，且可通过全局选项 "nosplice" 全局禁用。由于拼接依赖管道，使用该功能要求系统具备足够的空闲管道资源。

请注意：有关使用限制，请参阅“option splice-auto”。

示例：

```text
option splice-request
```

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅："option splice-auto"、"option splice-response" 以及全局选项 "nosplice" 和 "maxpipes"

<a id="entry-4-2-option-splice-response"></a>

**`option splice-response`**

```haproxy
option splice-response
no option splice-response
```

启用或禁用对响应的套接字自动进行内核加速

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

当在前端或后端启用此选项时，HAProxy 将尽可能使用内核 TCP 拼接技术，将数据从服务器转发至客户端。若无可用的管道资源，仍可能采用 recv/send 方式。此选项需在编译时启用拼接功能，且可通过全局选项 "nosplice" 全局禁用。由于拼接依赖管道，使用该功能要求系统具备足够的空闲管道资源。

请注意：有关使用限制，请参阅“option splice-auto”。

示例：

```text
option splice-response
```

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅："option splice-auto"、"option splice-request" 以及全局选项 "nosplice" 和 "maxpipes"

<a id="entry-4-2-option-spop-check"></a>

**`option spop-check`**

```haproxy
option spop-check
```

使用 SPOP 健康检查对服务器进行测试

可用于以下上下文：tcp

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

可以测试服务器是否正确地使用 SPOP 协议，而不仅仅是测试其是否接受 TCP 连接。启用此选项后，HAProxy 与服务器之间将执行 HELLO 握手，随后分析响应以检查是否报告了错误。

示例：

```text
option spop-check
```

另请参阅："option httpchk"

<a id="entry-4-2-option-srvtcpka"></a>

**`option srvtcpka`**

```haproxy
option srvtcpka
no option srvtcpka
```

启用或禁用在服务器端发送 TCP keepalive 数据包

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

当客户端与服务器之间存在防火墙或其他会话感知组件，且协议涉及长时间会话及较长空闲期（例如远程桌面）时，中间组件可能因会话空闲时间过长而决定终止该会话，从而带来风险。

启用套接字级别的 TCP 持久连接可使系统定期向连接的另一端发送数据包，从而保持连接处于活跃状态。持久连接探测之间的延迟由系统控制，且取决于操作系统及其调优参数。

必须理解，持久连接报文不会在应用层发出或接收，仅网络协议栈能够感知到它们。因此，即使代理的一端已使用持久连接来维持连接活跃，这些持久连接报文也不会被转发至代理的另一端。

请注意，这与 HTTP 持久连接无关。

使用选项 "srvtcpka" 可在连接的服务器端启用 TCP 持久连接探测，当 HAProxy 与服务器之间的会话超时被察觉时，此功能应能提供帮助。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅："option clitcpka"、"option tcpka"

<a id="entry-4-2-option-ssl-hello-chk"></a>

**`option ssl-hello-chk`**

```haproxy
option ssl-hello-chk
```

使用 SSLv3 客户端问候消息进行服务器健康检查

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

当通过 HAProxy 以 TCP 模式中继某些基于 SSL 的协议时，可以测试服务器是否正确地使用 SSL 通信，而不仅仅是测试其是否接受 TCP 连接。当设置 "option ssl-hello-chk" 时，连接建立后会向服务器发送一个纯 SSLv3 客户端问候消息，然后分析响应以查找 SSL 服务器问候消息。只有当响应中包含该服务器问候消息时，才认为服务器有效。

所有服务器均经过测试，确保其能正确响应 SSLv3 客户端握手消息，且大多数服务器甚至不会记录仅包含握手消息的请求，这一点值得肯定。

请注意，即使 HAProxy 未编译 SSL 支持，此健康检查仍可正常工作，因为它会伪造 SSL 消息。当 SSL 支持可用时，建议使用原生 SSL 健康检查，而非此方法。

另请参阅：“option httpchk”、“check-ssl”

<a id="entry-4-2-option-tcp-check"></a>

**`option tcp-check`**

```haproxy
option tcp-check
```

使用 tcp-check send/expect 序列执行健康检查

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

此健康检查方法旨在与“tcp-check”命令列表结合使用，以支持发送/期望类型的健康检查序列。

TCP 健康检查目前支持 4 种操作模式：   - 无 "tcp-check" 指令：健康检查仅包含一次连接尝试，此为默认模式。

    - 仅提及 "tcp-check send" 或 "tcp-check send-binary"：用于在建立连接的
      同时发送一个字符串。对于某些协议，例如发送 "QUIT" 消息可避免服务器
      为每次健康检查记录连接错误。检查结果仍仅基于能否打开连接。

    - 仅提及 "tcp-check expect"：用于测试欢迎横幅（banner）。连接打开后，
      HAProxy 等待服务器呈现一些内容，这些内容必须通过某些规则的校验。
      检查结果将基于内容与规则之间的匹配情况。适用于 POP、IMAP、SMTP、
      FTP、SSH、TELNET。

    - 同时提及 "tcp-check send" 和 "tcp-check expect"：用于测试 hello 类
      协议。HAProxy 发送消息，服务器作出响应，随后分析该响应。检查结果
      将基于响应内容与规则之间的匹配情况。这通常适用于需要绑定或请求/
      响应模型的协议。LDAP、MySQL、Redis 和 SSL 就是此类协议的例子，尽管
      它们均已具有对相应协议理解更深入的专用检查。在此模式下，可以发送
      多个问题，并分析多个应答。

第五种模式可用于在脚本的不同步骤中插入注释。

对于每个创建的 tcp-check 规则，可以添加一个 "comment" 指令，后接一个字符串。该字符串将在日志中以及调试模式下的 stderr 中输出。此功能有助于实现用户友好的错误报告。"comment" 指令为可选。

在执行健康检查期间，可通过使用 "tcp-check set-var" 操作，提供变量作用域以存储数据样本。可使用 "tcp-check unset-var" 释放这些变量。

示例：

```shell
# perform a POP check (analyze only server's banner)
option tcp-check
tcp-check expect string +OK\ POP3\ ready comment POP\ protocol

# perform an IMAP check (analyze only server's banner)
option tcp-check
tcp-check expect string *\ OK\ IMAP4\ ready comment IMAP\ protocol

# look for the redis master server after ensuring it speaks well
# redis protocol, then it exits properly.
# (send a command then analyze the response 3 times)
option tcp-check
tcp-check comment PING\ phase
tcp-check send PING\r\n
tcp-check expect string +PONG
tcp-check comment role\ check
tcp-check send info\ replication\r\n
tcp-check expect string role:master
tcp-check comment QUIT\ phase
tcp-check send QUIT\r\n
tcp-check expect string +OK

构造一个 HTTP 请求，然后分析响应
（分析前发送多个头）
option tcp-check
tcp-check comment forge\ and\ send\ HTTP\ request
tcp-check send HEAD\ /\ HTTP/1.1\r\n
tcp-check send Host:\ www.mydomain.com\r\n
tcp-check send User-Agent:\ HAProxy\ tcpcheck\r\n
tcp-check send \r\n
tcp-check expect rstring HTTP/1\..\ (2..|3..) comment check\ HTTP\ response

```

另请参阅：“tcp-check connect”、“tcp-check expect” 和 “tcp-check send”。

<a id="entry-4-2-option-tcp-smart-accept"></a>

**`option tcp-smart-accept`**

```haproxy
option tcp-smart-accept
no option tcp-smart-accept
```

启用或禁用在连接建立过程中保存一个 ACK 数据包

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：无

当 HTTP 连接请求到达时，系统会代表 HAProxy 进行确认，随后客户端立即发送请求，系统在通知 HAProxy 新连接的同时也对该请求进行确认。HAProxy 随后读取请求并发送响应。这意味着系统会额外发送一次 TCP ACK，而该 ACK 实际上是多余的，因为 HAProxy 完全可以在发送响应时一并确认该请求。

因此，在 HTTP 模式下，HAProxy 会自动请求系统在支持该功能的平台（目前至少包括 Linux）上避免发送此无用的 ACK。这不会造成任何问题，因为如果响应耗时超过预期，系统将在 40 毫秒后仍会发送该 ACK。

在复杂的网络故障排查会话中，可能需要禁用此优化，因为延迟确认（delayed ACKs）会使排查数据包延迟位置时更加复杂。此时可通过指定“no option tcp-smart-accept”恢复到正常行为。

也可以通过简单地指定“option tcp-smart-accept”来强制对非 HTTP 代理生效。例如，对于 SMTP 等某些服务，服务器会先发起通信，此时该选项可能具有实际意义。

建议避免在 defaults 段中强制设置此选项。如有疑问，可通过在该选项前添加 "default" 关键字将其恢复为自动值，或使用 "no" 关键字禁用该选项。

另请参阅："option tcp-smart-connect"

<a id="entry-4-2-option-tcp-smart-connect"></a>

**`option tcp-smart-connect`**

```haproxy
option tcp-smart-connect
no option tcp-smart-connect
```

启用或禁用在连接过程中保存一个 ACK 数据包

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

在某些系统（至少为 Linux）上，HAProxy 可以请求内核在收到连接请求时，不立即发送空的 ACK，而是直接发送缓冲区请求。此举可减少网络中一个数据包的传输，从而提升性能。对于某些服务器而言，此机制也具有实用性，因为它们能随连接建立立即获取请求数据。

当后端中设置 "option tcp-smart-connect" 时，此功能被启用。由于该功能会增加网络故障排查的复杂性，因此默认情况下未启用。

仅在客户端率先发起通信的协议（如 HTTP）中启用此功能才有意义。在其他情况下，若无数据可替代 ACK 发送，则发送正常的 ACK。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅："option tcp-smart-accept"

<a id="entry-4-2-option-tcpka"></a>

**`option tcpka`**

```haproxy
option tcpka
```

启用或禁用在两端发送 TCP keepalive 数据包

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

当客户端与服务器之间存在防火墙或其他会话感知组件，且协议涉及长时间会话及较长空闲期（例如远程桌面）时，中间组件可能因会话空闲时间过长而决定终止该会话，从而带来风险。

启用套接字级别的 TCP 持久连接可使系统定期向连接的另一端发送数据包，从而保持连接处于活跃状态。持久连接探测之间的延迟由系统控制，且取决于操作系统及其调优参数。

必须理解，持久连接报文不会在应用层发出或接收，仅网络协议栈能够感知到它们。因此，即使代理的一端已使用持久连接来维持连接活跃，这些持久连接报文也不会被转发至代理的另一端。

请注意，这与 HTTP 持久连接无关。

启用选项 "tcpka" 可在连接的客户端和服务器两端均发送 TCP 持久连接探测。请注意，此选项仅在 "defaults" 或 "listen" 段中有效。若在前端中使用此选项，仅客户端会启用持久连接；若在后端中使用此选项，仅服务器端会启用持久连接。因此，强烈建议在配置跨前端和后端分布时，显式使用 "option clitcpka" 和 "option srvtcpka"。

另请参阅："option clitcpka"、"option srvtcpka"

<a id="entry-4-2-option-tcplog"></a>

**`option tcplog [clf]`**

```haproxy
option tcplog [clf]
```

启用 TCP 连接的高级日志记录，包括流状态和计时器信息

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
clf       添加 "clf" 参数后，输出采用 CLF 格式，而非 HAProxy 默认的 TCP 格式。
          当需要将 HAProxy 日志交给仅支持 CLF 格式且无法扩展的特定日志分析器时，可使用此项。
          由于此格式要求 HTTP 格式，部分值已预设：HTTP 请求显示为 TCP，响应码显示为 000。
```

默认情况下，日志输出格式非常简陋，仅包含源地址和目标地址以及实例名称。通过指定“option tcplog”，每条日志行将变为更丰富的格式，包含但不限于连接计时器、流状态、连接数量、前端、后端和服务器名称，以及源地址和端口。该选项适用于纯 TCP 代理，以便确定是客户端还是服务器端断开连接或超时。对于常规 HTTP 代理，建议使用“option httplog”，其信息更为完整。

"option tcplog" 会覆盖之前所有的 "log-format" 指令。

另请参阅：“option httplog”，以及 [第 8 节](/zh/haproxy/configuration-logging/) 关于日志记录的内容。

<a id="entry-4-2-option-transparent"></a>

**`option transparent        (deprecated)`**

```haproxy
option transparent        (deprecated)
no option transparent     (deprecated)
```

启用客户端透明代理

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

此选项的引入旨在为第 3 层负载均衡器提供第 7 层持久性。其原理是利用操作系统将来自远程地址的入站连接重定向至本地进程（此处为 HAProxy），并让该进程知晓最初请求的地址。启用此选项后，未携带 Cookie 的会话将被转发至入站请求的原始目标 IP 地址（该地址应与另一台设备的地址匹配），而携带 Cookie 的请求仍会被转发至相应的服务器。

请注意，与普遍认知相反，此选项并不会在建立连接时向服务器呈现客户端的 IP 地址。

从 3.3 版本开始，该选项已被弃用，因其曾存在多项内部技术限制。使用该选项将发出警告，如确需使用，可通过全局关键字 "expose-deprecated-directives" 避免警告。

正确做法是在地址 0.0.0.0 上声明一个服务器，该服务器将负责连接到预期的目标地址。服务器还将正确处理与目标服务器的空闲连接。

示例：

```shell
# option transparent  ## before 3.3
server transparent 0.0.0.0
```

另请参阅“source”关键字的“usesrc”参数，以及“bind”关键字的“transparent”选项。

option use-small-buffers [ queue \| l7-retries \| check ]\*

为指定类别启用小缓冲区支持。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

此选项可用于在不同位置启用小缓冲区支持，以节省内存。默认情况下，不带参数时，尽可能在所有可能的位置使用小缓冲区。否则，可将其限制为仅在以下位置启用：

- queue：启用后，若连接被排队，将使用小缓冲区存储请求，前提是请求足够小。
- l7-retries：启用后，启用 L7 重试时将使用小缓冲区保存请求。
- check：启用后，健康检查请求将使用小缓冲区。

启用后，将使用小缓冲区，但仅在可行时。若数据过大，则自动改用常规缓冲区。小缓冲区的大小可通过 "tune.bufsize.small" 全局设置进行配置。

如果该选项在“defaults”段中已启用，可以在特定实例中通过在其前添加“no”关键字来禁用。

另请参阅：tune.bufsize.small

<a id="entry-4-2-persist-rdp-cookie"></a>

**`persist rdp-cookie`**

```haproxy
persist rdp-cookie
persist rdp-cookie(<name>)
```

启用基于 RDP 会话 Cookie 的持久性

可用于以下上下文：tcp

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<name>    是可选的要检查的 RDP Cookie 名称，省略时使用默认名称 "msts"。
          目前没有合理的理由更改该名称。
```

此语句启用基于 RDP Cookie 的会话保持功能。RDP Cookie 包含在已知服务器列表中定位服务器所需的所有信息。因此，当在后端中设置此选项时，请求将被分析；若发现 RDP Cookie，则对其进行解码。若解码结果匹配某个仍处于 UP 状态的已知服务器（或已设置 "option persist"），则连接将被转发至该服务器。

请注意，此配置仅在 TCP 后端中有效，但要使其生效，前端必须等待足够长的时间，以确保 RDP Cookie 已存在于请求缓冲区中。这与使用“rdp-cookie”负载均衡方法的要求相同。因此，强烈建议将所有配置项置于单一的“listen”段中。

此外，必须理解，仅当终端服务器配置为“令牌重定向模式”时，才会发出此 RDP 令牌，这意味着已禁用“IP 地址重定向”选项。

示例：

```text
listen tse-farm
    bind :3389
    # wait up to 5s for an RDP cookie in the request
    tcp-request inspect-delay 5s
    tcp-request content accept if RDP_COOKIE
    # apply RDP cookie persistence
    persist rdp-cookie
    # if server is unknown, let's balance on the same cookie.
    # alternatively, "balance leastconn" may be useful too.
    balance rdp-cookie
    server srv1 1.1.1.1:3389
    server srv2 1.1.1.2:3389
```

另请参阅："balance rdp-cookie"、"tcp-request" 以及 "req.rdp_cookie" ACL。

<a id="entry-4-2-quic-initial"></a>

**`quic-initial <action> [ { if | unless } <condition> ]`**

```haproxy
quic-initial <action> [ { if | unless } <condition> ]
```

对传入的 QUIC Initial 数据包执行一个动作。与 "tcp-request connection" 不同，该动作在任何连接元素实例化之前、SSL 握手启动和完成之前执行，因此在需要拒绝连接尝试时效率更高。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes(!) \| yes \| yes \| no

参数：

```text
<action>    定义条件成立时执行的动作，参见下文。

<condition> 是仅基于第4层的标准 ACL 条件（参见第 7 节）。
            但 QUIC initial 规则执行得过早，即使某些第4层样本提取方法没有配置警告，
            也可能产生未定义的运行时行为，不过不会导致崩溃。
            目前仅应视内部样本和第4层的 "src*"、"dst*" 为受支持的方法。
```

此动作在 QUIC 数据包解析的早期阶段执行。因此，仅支持极少量的动作：   - accept   - dgram-drop   - reject   - send-retry

<a id="entry-4-2-rate-limit-sessions"></a>

**`rate-limit sessions <rate>`**

```haproxy
rate-limit sessions <rate>
```

在前端上设置每秒可接受的新会话数量限制

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
<rate>    <rate> 参数是整数，表示前端每秒接受的新会话数上限。
```

当前端每秒新建会话数达到指定数量时，将停止接受新的连接，直至速率再次低于限制。在此期间，待处理的会话将保留在套接字的连接队列（系统缓冲区）中，HAProxy 甚至不会察觉到会话正在等待。在对高负载服务设置极低限制时，建议使用 "backlog" 关键字增加套接字的连接队列长度。

该功能在阻止基于连接的攻击或对脆弱服务器的服务滥用方面尤为高效。由于会话速率每毫秒测量一次，因此精度极高。此外，限制立即生效，无需任何延迟即可检测到阈值。

示例：将 SMTP 的连接速率限制为每秒最多 10 次



```haproxy
listen smtp
    mode tcp
    bind :25
    rate-limit sessions 10
    server smtp1 127.0.0.1:1025
```


请注意：当达到最大速率时，前端的状态不会改变，但如果启用了“socket-stats”选项，其套接字将在统计信息中显示为“WAITING”。

另请参阅：`backlog` 关键字以及 "fe_sess_rate" ACL 条件。

<a id="entry-4-2-redirect-location"></a>

**`redirect location <loc> [code <code>] <option> [{if | unless} <condition>]`**

```haproxy
redirect location <loc> [code <code>] <option> [{if | unless} <condition>]
redirect prefix   <pfx> [code <code>] <option> [{if | unless} <condition>]
redirect scheme   <sch> [code <code>] <option> [{if | unless} <condition>]
```

若满足条件，则返回 HTTP 重定向

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| yes

如果满足条件，则 HTTP 请求将导致重定向响应。若未指定条件，则重定向无条件生效。

参数：

```text
<loc>     使用 "redirect location" 时，将 <loc> 的确切值放入 HTTP "Location" 头。
          用于 "http-request" 规则时，<loc> 遵循自定义日志格式，可包含动态值（参见第 8.2.6 节）。

<pfx>     使用 "redirect prefix" 时，将 <pfx> 与完整 URI 路径拼接构建 "Location" 头，
          除非指定 "drop-query"，否则包含查询字符串。<pfx> 恰好等于 "/" 时，
          不在原始 URI 前插入任何内容，可重定向到同一 URL，例如插入 Cookie。
          用于 "http-request" 规则时，<pfx> 遵循自定义日志格式，可包含动态值（参见第 8.2.6 节）。

<sch>     使用 "redirect scheme" 时，将 <sch>、"://"、第一个 "Host" 头及 URI 路径拼接构建
          "Location" 头，除非指定 "drop-query"，否则包含查询字符串。
          未找到路径或路径为 "*" 时，改用 "/"。未找到 "Host" 头时，返回空的主机部分，
          多数近期浏览器理解为重定向到同一主机。主要用于将 HTTP 重定向至 HTTPS。
          用于 "http-request" 规则时，<sch> 遵循自定义日志格式，可包含动态值（参见第 8.2.6 节）。

<code>    是可选参数，指定 HTTP 重定向类型。仅支持 301、302、303、307 和 308，未指定时默认 302。
          301 表示 "Moved permanently"（永久移动），浏览器可缓存 Location；
          302 表示 "Moved temporarily"（临时移动），浏览器不应缓存重定向。
          303 与 302 相似，但浏览器使用 GET 方法获取目标。
          307 与 302 相似，但明确要求复用相同方法；同理，需复用相同方法时，以 308 替代 301。

<option>  可通过以下选项调整重定向行为：

  - "drop-query"
    用于基于前缀的重定向时，目标中不包含查询字符串，例如可用于将用户导向非安全页面。
    对 location 类型的重定向无效。

  - "append-slash"
    可与 "drop-query" 组合，将未以 '/' 结尾的 URL 重定向到末尾带 '/' 的同一 URL。
    可用于确保搜索引擎仅看到一个 URL，推荐使用状态码 301。

  - "ignore-empty"
    仅当目标由日志格式表达式生成（即用于 http-request 或 http-response）时有效。
    表达式结果为空时，静默跳过规则。主要用于通过简单映射对已知路径执行批量重定向。

  - "set-cookie NAME[=value]"
    将包含 NAME（以及可选的 "=value"）的 "Set-Cookie" 头添加到响应。
    有时用于标记用户已经访问，例如防御某些 DoS。未添加其他 Cookie 选项，因此为会话 Cookie。
    对浏览器而言，只有名称且没有等号的 Cookie，与带等号的 Cookie 不同。

  - "set-cookie-fmt <fmt>"
    与上一选项相同，但 "Set-Cookie" 头由日志格式字符串 <fmt> 的求值结果填充。
    应确保遵循 "NAME[=value]" 格式，因为配置解析期间不进行特殊检查。

  - "clear-cookie NAME[=]"
    添加包含 NAME（以及可选的 "="）的 "Set-Cookie" 头，但将 "Max-Age" 设为零，通知浏览器删除 Cookie。
    例如用于登出页面。清除 "NAME" 不会删除以 "NAME=value" 设置的 Cookie；
    必须清除 "NAME="，因为浏览器区分两者。

  - "keep-query"
    用于基于 location 的重定向时，将原始 URI 的查询字符串（若有）附加到目标。
    未找到时不添加。目标已有查询字符串时，用 '&' 分隔并附加原始查询字符串。
```

示例：仅将登录 URL 重定向至 HTTPS。

```haproxy
acl clear      dst_port  80
acl secure     dst_port  8080
acl login_page url_beg   /login
acl logout     url_beg   /logout
acl uid_given  url_reg   /login?userid=[^&]+
acl cookie_set hdr_sub(cookie) SEEN=1

redirect prefix   https://mysite.com set-cookie SEEN=1 if !cookie_set
redirect prefix   https://mysite.com           if login_page !secure
redirect prefix   http://mysite.com drop-query if login_page !uid_given
redirect location http://mysite.com/           if !login_page secure
redirect location / clear-cookie USERID=       if logout
```



示例：对未带斜杠的文章请求发送重定向


```haproxy
acl missing_slash path_reg ^/article/[^/]*$
redirect code 301 prefix / drop-query append-slash if missing_slash
```


示例：当 SSL 由 HAProxy 处理时，将所有 HTTP 流量重定向至 HTTPS。

```haproxy
redirect scheme https if !{ ssl_fc }
```


示例：在所有未包含 'www.' 前缀的主机前添加该前缀


```haproxy
http-request redirect code 301 location      \
  http://www.%[hdr(host)]%[capture.req.uri]  \
  unless { hdr_beg(host) -i www }
```


示例：仅将旧网址永久重定向至新网址


```haproxy
http-request redirect code 301 location               \
  %[path,map_str(old-blog-articles.map)] ignore-empty
```


请参阅 [第 7 节](/zh/haproxy/acls-and-samples/) 了解 ACL 的使用方法。

<a id="entry-4-2-retries"></a>

**`retries <value>`**

```haproxy
retries <value>
```

设置在服务器发生故障后执行的重试次数

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<value>   是请求或连接尝试失败后，在服务器上重试的次数。
```

默认情况下，重试仅适用于新的连接尝试。然而，当使用“retry-on”指令时，其他条件也可能触发重试（例如，空响应、非期望的状态码），每种情况均计为一次尝试，当尝试次数累计达到此处指定的值时，将返回错误。

为避免在服务器重启时立即重新连接，对同一服务器的重试操作前会应用一个倒转计时器，其时长为 min("timeout connect", 1 秒)。

当启用 "option redispatch" 时，即使 Cookie 指向另一台服务器，也可能在其他服务器上执行重试。默认情况下，这仅限于最后一次重试，除非向 "option redispatch" 传递参数。

另请参阅："option redispatch"

<a id="entry-4-2-retry-on"></a>

**`retry-on [space-delimited list of keywords]`**

```haproxy
retry-on [space-delimited list of keywords]
```

指定在何时尝试自动重试失败的请求。此设置仅在“mode”设置为 http 时有效，其他情况下将被静默忽略。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
 <keywords>  是空格分隔的关键字或 HTTP 状态码列表，每项表示一种希望重试请求的失败事件。
             更改此设置前，请阅读底部注意事项。支持：

   none              永不重试。

   conn-failure      连接或 SSL 握手失败，导致请求未能发送时重试。这是默认值。

   empty-response    已发送部分请求后，服务器连接关闭，且未收到任何服务器数据时重试。
                     可能是服务器侧请求超时、网络状况差，或服务器在处理请求时崩溃或重启。

   junk-response     服务器返回的内容不像完整 HTTP 响应时重试，包括不完整的响应头及非 HTTP 内容。
                     此类情况下重试通常不是好主意，可能是配置错误（错误的服务器端口），
                     或请求危害服务器（如缓冲区溢出攻击）。

   response-timeout  等待服务器响应请求时，服务器超时到期。可能是网络状况差、
                     复用了已在路径中失效的空闲连接，或请求处理成本极高。
                     对执行繁重数据库处理（如全表扫描）的服务器，通常不应在此类情况下重试，
                     以免放大拒绝服务攻击。

   0rtt-rejected     重试通过早期数据发送且被服务器拒绝的请求，此类请求通常认为可以安全重试。

   <status>          以下任一 HTTP 状态码："401"（Unauthorized）、"403"（Forbidden）、
                     "404"（Not Found）、"408"（Request Timeout）、
"421"（Misdirected Request）、"425"（Too Early）、
"429"（Too Many Requests）、"500"（Server Error）、
"501"（Not Implemented）、"502"（Bad Gateway）、
"503"（Service Unavailable）、"504"（Gateway Timeout）。

   all-retryable-errors
                     对任何视为可重试的错误重试请求，目前启用 "conn-failure"、"empty-response"、
                     "junk-response"、"response-timeout"、"0rtt-rejected"、"500"、"502"、"503" 和 "504"。
```

使用此指令会替换之前的所有设置，而非累加。

请注意，使用除 "none" 和 "conn-failure" 以外的任何值都需要分配缓冲区并将整个请求复制到其中，因此会产生内存和性能影响。无法放入单个缓冲区的请求将永远不会重试（参见全局设置 tune.bufsize）。

必须确保应用程序内置了重放保护机制，例如在请求中传递唯一事务 ID，或确保重放相同请求无任何后果。否则，除 "conn-failure" 和 "none" 外，使用任何其他重试值都极为危险。静态文件服务器和缓存通常被认为对任何类型的重试均安全。使用状态码可快速将连接从表现出异常行为（如内存不足、文件系统问题等）的服务器中移除，但此时建议立即执行重分派，将连接转至另一台服务器（请参见 "option redispatch"）。最后，必须理解，大多数故障的根本原因在于请求本身，对导致服务器异常的请求进行重试，通常会使该服务器状况更糟，或在发生重分派时导致整个服务状况恶化。

除非确切了解应用程序如何处理重放请求，否则不应使用此指令。

默认值为 "conn-failure"。

示例：

```text
retry-on 503 504
```

另请参阅："retries"，"option redispatch"，"tune.bufsize"

<a id="entry-4-2-server"></a>

**`server <name> <address>[:[port]] [param*]`**

```haproxy
server <name> <address>[:[port]] [param*]
```

在后端中声明服务器

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

参数：

```text
<name>    是分配给服务器的内部名称，出现在日志和告警中。
          设置了 "http-send-name-header" 时，将其添加到发往服务器的请求头。
          名称在 backend 段内必须唯一。

<address> 是服务器的 IPv4 或 IPv6 地址，也支持可解析的主机名，但在启动期间解析。
          地址 "0.0.0.0" 或 "*" 具有特殊含义：将连接转发到与客户端连接相同的 IP 地址。
          适合透明代理架构，客户端连接被拦截后，HAProxy 必须转发到原始目标地址。
          与 "transparent" 关键字的作用基本相同，但使用服务器配置可限制并发并报告统计信息。
          可在地址前加地址族前缀，忽略地址格式并强制使用指定地址族，
          例如指定不包含斜杠（'/'）的 unix 套接字路径。目前支持：
                - 'ipv4@'  -> 地址始终为 IPv4
                - 'ipv6@'  -> 地址始终为 IPv6
                - 'unix@'  -> 地址是本地 unix 套接字路径
                - 'abns@'  -> 地址位于抽象命名空间（仅 Linux）
                - 'abnsz@'  -> 地址位于抽象命名空间（仅 Linux），但显式以零终止，
                   不使用 \0 填充 sun_path；适合连接未实现 haproxy 默认 abns 命名逻辑的程序。
                - 'sockpair@' -> 地址是已连接的 unix 套接字或 socketpair 的 FD。
                  建立连接时，后端创建一对已连接套接字，通过 FD 传递其中一个。
                  bind 端将收到的套接字用作客户端 FD。应谨慎使用。
                - 'quic4@' [ EXPERIMENTAL] -> 地址解析为 IPv4，使用 UDP 协议。
                  后端侧 QUIC 视为实验性功能，主要因为会阻止运行时删除服务器。
                  使用时要求启用全局关键字 "expose-experimental-directives"。
                - 'quic6@' [ EXPERIMENTAL] -> 地址解析为 IPv6，使用 UDP 协议，同样标记为实验性功能。
                - 'rhttp@' [ EXPERIMENTAL ] -> 反向 HTTP 场景中被动服务器使用的自定义地址族。
                  这是实验性功能，要求在此 server 之前的一行中启用 "expose-experimental-directives"。
          地址参数可能需要引用环境变量，参见第 2.3 节。
          可通过 "init-addr" 改变启动时解析 IP 地址的方式。

<port>    是可选的端口参数。设置时，所有连接均发送到此端口；未设置时，使用客户端连接的同一端口。
          也可在端口前加 "+" 或 "-"，此时将该值加到客户端端口上，得到服务器端口。

<param*>  是此服务器的参数列表。"server" 关键字支持大量选项，有专门的一节完整介绍。详情见第 5 节。
```

示例：

```text
server first  10.1.1.1:1080 cookie first  check inter 1000
server second 10.1.1.2:1080 cookie second check inter 1000
server transp ipv4@
server backup "${SRV_BACKUP}:1080" backup
server www1_dc1 "${LAN_DC1}.101:80"
server www1_dc2 "${LAN_DC2}.101:80"
```

请注意：关于 Linux 的抽象命名空间套接字，“abns” HAProxy 套接字使用 sun_path 的完整长度作为地址长度。其他一些程序（如 socat）默认仅使用字符串长度。如需使 socat 的抽象套接字定义与 HAProxy 兼容，请向 socat 的任意抽象套接字定义传递选项 ",unix-tightsocklen=0"，或改用 "abnsz" HAProxy 套接字族。

另请参阅：“default-server”、“http-send-name-header”以及[第 5 节](/zh/haproxy/bind-and-server-options/) 中关于服务器选项的说明

<a id="entry-4-2-server-state-file-name"></a>

**`server-state-file-name [ { use-backend-name | <file> } ]`**

```haproxy
server-state-file-name [ { use-backend-name | <file> } ]
```

设置服务器状态文件为可读，加载并应用到此后端中可用的服务器。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

仅当指令 "load-server-state-from-file" 设置为 "local" 时生效。若未提供 `<file>`，且使用了 "use-backend-name" 或该指令未设置，则使用后端名称。若 `<file>` 以斜杠 '/' 开头，则视为绝对路径。否则，将 `<file>` 与全局指令 "server-state-base" 拼接。

示例：以下最小配置将使 HAProxy 查找状态服务器文件 '/etc/haproxy/states/bk'：

    global
      server-state-file-base /etc/haproxy/states

    backend bk
      load-server-state-from-file

另请参阅：“server-state-base”、“load-server-state-from-file” 和 “show servers state”

<a id="entry-4-2-server-template"></a>

**`server-template <prefix> <num | range> <fqdn>[:<port>] [params*]`**

```haproxy
server-template <prefix> <num | range> <fqdn>[:<port>] [params*]
```

设置模板以使用共享参数初始化服务器。这些服务器的名称由 `<prefix>` 和 \<num \| range\> 参数构建。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

参数：

```text
<prefix>  要创建的服务器名称的前缀。

<num | range>
          若提供 <num>，此模板初始化 <num> 个服务器，名称后缀从 1 到 <num>。
          也可提供范围 <num_low>-<num_high>，以 <num_low> 到 <num_high> 作为服务器名称后缀。

<fqdn>    为此模板初始化的所有服务器指定的 FQDN。

<port>    与 "server" 的 <port> 参数含义相同（参见 "server" 关键字）。

<params*>
          "server" 关键字支持的其余服务器参数。
```

示例：

```shell
# Initializes 3 servers with srv1, srv2 and srv3 as names,
# google.com as FQDN, and health-check enabled.
server-template srv 1-3 google.com:80 check

# or
server-template srv 3 google.com:80 check

# would be equivalent to:
server srv1 google.com:80 check
server srv2 google.com:80 check
server srv3 google.com:80 check


```

<a id="entry-4-2-source"></a>

**`source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | client | clientip } ]`**

```haproxy
source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | client | clientip } ]
source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | hdr_ip(<hdr>[,<occ>]) } ]
source <addr>[:<port>] [interface <name>]
```

设置传出连接的源地址

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<addr>    是 HAProxy 连接服务器前绑定的 IPv4 地址，也用作健康检查的源地址。

          默认值 0.0.0.0 表示由系统选择到达目标最合适的地址。
          可在地址前加地址族前缀，忽略地址格式并强制使用指定地址族，
          例如指定不包含斜杠（'/'）的 unix 套接字路径。目前支持：
            - 'ipv4@' -> 地址始终为 IPv4
            - 'ipv6@' -> 地址始终为 IPv6
            - 'unix@' -> 地址是本地 unix 套接字路径
            - 'abns@' -> 地址位于抽象命名空间（仅 Linux）
            - 'abnsz@'  -> 地址位于以零终止的抽象命名空间（仅 Linux）

          地址参数可能需要引用环境变量，参见第 2.3 节。

<port>    是可选端口，通常不需要，但在某些特殊场景可能有用。
          默认值为零，表示由系统选择空闲端口。后端不支持端口范围；
          若要强制使用范围，必须在每条 "server" 行中指定。

<addr2>   是在完全透明代理模式下转发连接时向服务器呈现的 IP 地址，
          目前仅部分打过补丁的 Linux 内核支持。
          指定此地址后，连接服务器的客户端将以此地址呈现，而健康检查仍使用 <addr>。

<port2>   是在完全透明代理模式下向服务器呈现的可选端口（参见上方 <addr2>）。
          默认值为零，表示由系统选择空闲端口。

<hdr>     是用于提取要绑定的 IP 的 HTTP 头名称。该头是逗号分隔的列表，可包含多个 IP 地址，
          默认使用最后一次出现的值。用于配合 X-Forwarded-For，
          自动绑定到前一个代理（通常是 Stunnel）看到的客户端 IP 地址。
          要使用最后一个以外的值，参见下方 <occ>。
          未找到头或指定位置的值时，不进行绑定，使用代理的默认 IP 地址。
          与任何 HTTP 头一样，头名称不区分大小写。

<occ>     是多值头中要使用的值的位置，与 "hdr_ip(<hdr>)" 组合，以指定源 IP 地址使用哪个值。
          正值从第一个值起计算，1 表示第一个；负值相对于最后一个值，-1 表示最后一个。
          适合基础设施入口设置 X-Forwarded-For 后，在相隔多个代理层的位置仍需使用该头的情况。
          未指定时假定为 -1，传入零则禁用此功能。

<name>    是出站流量可选绑定的接口名称。支持该功能的系统（目前仅 Linux）允许将到服务器的全部流量
          绑定到此接口，即使它不是系统根据路由表选择的接口。必须极其谨慎地使用，并且需要 root 权限。
```

“source” 关键字在复杂环境中非常有用，当仅允许特定地址连接到服务器时尤为必要。例如，当必须通过公共网关使用私有地址时，系统可能无法自行确定合适的源地址，此时该关键字便显得尤为重要。

通过“usesrc”可选关键字，可使用某些修补版 Linux 内核提供的扩展。该功能允许代理使用不属于本机系统的 IP 地址连接服务器。此模式称为“完全透明代理模式”。要使该模式正常工作，目标服务器必须通过运行 HAProxy 的机器将流量返回至该地址，且通常需在该机器上启用 IP 转发功能。

在“完全透明代理”模式下，可以强制指定一个特定的 IP 地址呈现给服务器。实际上，这种用法并不常见。更常见的做法是让 HAProxy 向服务器呈现客户端的 IP 地址。实现这一点有两种方法：

    - 呈现客户端的 IP 地址和端口。这是透明度最高的模式，但当机器上启用了
      IP 连接跟踪时可能会引发问题，因为同一连接可能以不同的状态被看到
      两次。不过，此方案的巨大优势在于不会将系统限制在 6.4 万个出站
      “地址+端口”组合内，因为可以使用客户端地址的所有取值范围。

    - 仅呈现客户端的 IP 地址，并选用一个空闲端口。此方案仍相当优雅，但
      透明度略低（下游防火墙日志将与上游不匹配）。它的缺点是将并发连接数
      限制在通常的 6.4 万个端口内。不过，由于上游和下游端口不同，机器上
      的本地 IP 连接跟踪不会因同一会话的复用而受到干扰。

此选项为后端中所有服务器设置默认源地址。也可在“defaults”段中指定。更精细的源地址配置可通过“source”服务器选项在服务器级别实现。详情请参见 [第 5 节](/zh/haproxy/bind-and-server-options/)。

要使 "usesrc" 正常工作，需具备 root 权限，或在支持的系统上具备 "cap_net_raw" 能力。另请参阅 "setcap" 全局指令。

示例：

```text
backend private
    # Connect to the servers using our 192.168.1.200 source address
    source 192.168.1.200

backend transparent_ssl1
    # Connect to the SSL farm from the client's source address
    source 192.168.1.200 usesrc clientip

backend transparent_ssl2
    # Connect to the SSL farm from the client's source address and port
    # not recommended if IP conntrack is present on the local machine.
    source 192.168.1.200 usesrc client

backend transparent_ssl3
    # Connect to the SSL farm from the client's source address. It
    # is more conntrack-friendly.
    source 192.168.1.200 usesrc clientip

backend transparent_smtp
    # Connect to the SMTP farm from the client's source address/port
    # with Tproxy version 4.
    source 0.0.0.0 usesrc clientip

backend transparent_http
    # Connect to the servers using the client's IP as seen by previous
    # proxy.
    source 0.0.0.0 usesrc hdr_ip(x-forwarded-for,-1)
```

另请参阅：[第 5 节](/zh/haproxy/bind-and-server-options/) 中的 "source" 服务器选项、Linux 内核的 Tproxy 补丁（位于 [www.balabit.com](http://www.balabit.com)），以及 "bind" 关键字。

<a id="entry-4-2-srvtcpka-cnt"></a>

**`srvtcpka-cnt <count>`**

```haproxy
srvtcpka-cnt <count>
```

设置 TCP 在服务器端丢弃连接前应发送的最大保活探测次数。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<count>   是保活探测的最大次数。
```

此关键字对应套接字选项 TCP_KEEPCNT。若未指定此关键字，则使用系统级 TCP 参数（tcp_keepalive_probes）。该设置的可用性取决于操作系统。已知其在 Linux 上可用。

另请参阅：“option srvtcpka”、“srvtcpka-idle”、“srvtcpka-intvl”。

<a id="entry-4-2-srvtcpka-idle"></a>

**`srvtcpka-idle <timeout>`**

```haproxy
srvtcpka-idle <timeout>
```

设置连接在 TCP 开始发送保活探测前需保持空闲的时间，若启用，则在服务器端发送 TCP 保活数据包。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<timeout> 是连接保持空闲多久后 TCP 开始发送保活探测的时间。默认单位为秒，
          也可在数值后添加单位后缀，使用其他单位，详见本文开头的说明。
```

此关键字对应套接字选项 TCP_KEEPIDLE。若未指定此关键字，则使用系统级 TCP 参数（tcp_keepalive_time）。该设置的可用性取决于操作系统。已知其在 Linux 上可用。

另请参阅：“option srvtcpka”、“srvtcpka-cnt”、“srvtcpka-intvl”。

<a id="entry-4-2-srvtcpka-intvl"></a>

**`srvtcpka-intvl <timeout>`**

```haproxy
srvtcpka-intvl <timeout>
```

设置服务器端单个 keepalive 探测之间的间隔时间。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<timeout> 是两次保活探测之间的时间。默认单位为秒，也可在数值后添加单位后缀，
          使用其他单位，详见本文开头的说明。
```

此关键字对应套接字选项 TCP_KEEPINTVL。若未指定此关键字，则使用系统级 TCP 参数（tcp_keepalive_intvl）。该设置的可用性取决于操作系统。已知其在 Linux 上可用。

另请参阅：“option srvtcpka”、“srvtcpka-cnt”、“srvtcpka-idle”。

<a id="entry-4-2-stats-admin"></a>

**`stats admin { if | unless } <cond>`**

```haproxy
stats admin { if | unless } <cond>
```

若满足/不满足某一条件，则启用统计信息管理级别

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| yes

此语句在满足（或不满足）特定条件时，启用统计信息管理级别。

管理级别允许通过 Web 界面启用或禁用服务器。出于安全考虑，统计信息页面默认为只读。若在段中设置了“stats scope”指令，则仅限这些指令指定的代理可接受状态变更；对其他代理的访问将被拒绝。

当前，POST 请求的大小受限于缓冲区大小减去预留缓冲区空间，这意味着如果服务器列表过长，请求将无法被处理。建议一次仅修改少量服务器。

管理员 POST 请求容易受到 CSRF 攻击。虽然通过检查 Origin（若无 Origin，则检查 Referer）是否与 Host 头匹配在一定程度上缓解了该问题，但不足以完全防止攻击。无法完全防范此类攻击。建议避免在公共接口上暴露该功能，并限制可访问的用户范围。

示例：

```shell
# statistics admin level only for localhost
backend stats_localhost
    stats enable
    stats admin if LOCALHOST
```

示例：

```shell
# statistics admin level always enabled because of the authentication
backend stats_auth
    stats enable
    stats auth  admin:AdMiN123
    stats admin if TRUE
```

示例：

```shell
# statistics admin level depends on the authenticated user
userlist stats-auth
    group admin    users admin
    user  admin    insecure-password 'AdMiN123'
    group readonly users haproxy
    user  haproxy  insecure-password 'haproxy'

backend stats_auth
    stats enable
    acl AUTH       http_auth(stats-auth)
    acl AUTH_ADMIN http_auth_group(stats-auth) admin
    stats http-request auth unless AUTH
    stats admin if AUTH_ADMIN
```

另请参阅：“stats enable”、“stats auth”、“stats http-request”、“stats scope”、[第 12.2 节](/zh/haproxy/other-sections/#section-12-2) 关于 userlists 的说明以及 [第 7 节](/zh/haproxy/acls-and-samples/) 关于 ACL 使用的说明。

<a id="entry-4-2-ssl-f-use"></a>

**`ssl-f-use [<sslbindconf> ...]*`**

```haproxy
ssl-f-use [<sslbindconf> ...]*
```

为当前前端分配证书。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| no

参数：

```text
<sslbindconf> 支持 bind 行中的以下关键字
（参见第 5.1 节：绑定选项）：

- allow-0rtt
- alpn
- ca-file
- ca-verify-file
- ciphers
- ciphersuites
- client-sigalgs
- crl-file
- curves
- ecdhe
- ktls
- no-alpn
- no-ca-names
- npn
- sigalgs
- ssl-min-ver
- ssl-max-ver
- verify

sslbindconf 还支持 crt-store 的 load 关键字中的以下选项（参见第 12.7.1 节：加载选项）：

- crt
- key
- ocsp
- issuer
- sctl
- ocsp-update
```

为证书 `<crtname>` 分配至由前端名称自动创建的 crt-list，该列表名称以 @ 为前缀（例如：@frontend1）。

此隐式 crt-list 将被分配给当前前端中的每一行 "ssl" 绑定。

通过 stats socket 发出的 crt-list 命令对此 crt-list 生效，因此可以替换、移除或添加证书和 SSL 选项。

示例：

```text
frontend https
    bind :443 ssl
    bind quic4@:443 ssl
    ssl-f-use crt foobar.pem.rsa sigalgs "RSA-PSS+SHA256"
    ssl-f-use crt test.foobar.pem
    ssl-f-use crt test2.foobar.crt key test2.foobar.key ocsp test2.foobar.ocsp ocsp-update on
```

另请参阅：crt-list 和 crt。

<a id="entry-4-2-stats-auth"></a>

**`stats auth <user>:<passwd>`**

```haproxy
stats auth <user>:<passwd>
```

启用统计信息并配置认证，授予账户访问权限

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<user>    是获准访问的用户名。

<passwd>  是该用户的明文密码。
```

此语句启用默认设置的统计信息，并仅限制已声明的用户访问。可根据需要重复此语句，以允许任意数量的用户。当用户尝试访问统计信息但未提供有效账户时，将返回“401 Forbidden”响应，浏览器会提示用户输入有效的用户名和密码。返回给浏览器的“realm”可使用“stats realm”进行配置。

由于认证方法为 HTTP Basic 认证，密码在网络中以明文形式传输。因此，决定配置文件也使用明文密码，以提醒用户此类密码不应具有敏感性，且不得与任何其他账户共享。

还可以通过使用 "stats scope" 缩小报告中显示的代理范围。

尽管仅凭此语句即可启用统计信息报告，但建议设置所有其他参数，以避免依赖默认的非显式参数。

示例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

另请参阅：“stats enable”、“stats realm”、“stats scope”、“stats uri”

<a id="entry-4-2-stats-enable"></a>

**`stats enable`**

```haproxy
stats enable
```

启用统计信息报告并使用默认设置

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

此语句启用统计信息报告，并使用编译时定义的默认设置。除非另有说明，否则以下设置将被采用：   - stats uri : /haproxy?stats   - stats realm: "HAProxy Statistics"   - stats auth : 无认证   - stats scope: 无限制

尽管仅凭此语句即可启用统计信息报告，但建议设置所有其他参数，以避免依赖默认的非显式参数。

示例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

另请参阅：“stats auth”、“stats realm”、“stats uri”

<a id="entry-4-2-stats-hide-version"></a>

**`stats hide-version`**

```haproxy
stats hide-version
```

启用统计信息并隐藏 HAProxy 版本报告

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

统计信息页面可报告一些有用的状态信息，包括 HAProxy 的版本。然而，通常认为向任何人披露精确版本号存在风险，因为这可能帮助攻击者针对已知漏洞实施特定攻击。使用“stats hide-version”语句可从统计信息报告中移除版本信息。对于公开站点或登录凭证较弱的站点，建议启用此设置，且该选项为默认值。

尽管仅凭此语句即可启用统计信息报告，但建议设置所有其他参数，以避免依赖默认的非显式参数。

示例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

另请参阅：“stats auth”、“stats enable”、“stats realm”、“stats uri”、“stats show-version”

<a id="entry-4-2-stats-http-request"></a>

**`stats http-request { allow | deny | auth [realm <realm>] }`**

```haproxy
stats http-request { allow | deny | auth [realm <realm>] }
             [ { if | unless } <condition> ]
```

统计信息访问控制

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

与 "http-request" 类似，这些选项允许精细控制对统计信息的访问。每个选项后可跟 if/unless 和 ACL。首个条件匹配的选项（或无条件的选项）为最终结果。对于 "deny"，返回 403 错误；对于 "allow"，执行正常处理；对于 "auth"，返回 401/407 错误码，客户端需输入用户名和密码。

每个实例中可配置的 http-request 语句数量没有固定限制。

另请参阅：“http-request”，[第 12.2 节](/zh/haproxy/other-sections/#section-12-2) 关于 userlists 的说明以及 [第 7 节](/zh/haproxy/acls-and-samples/) 关于 ACL 使用的说明。

<a id="entry-4-2-stats-realm"></a>

**`stats realm <realm>`**

```haproxy
stats realm <realm>
```

启用统计信息并设置认证域

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<realm>   是向浏览器报告的 HTTP Basic Authentication 认证域的名称。
          浏览器在提示用户输入有效用户名和密码的弹出窗口中显示它。
```

领域以单个单词读取，因此其中的任何空格都应使用反斜杠（'&#92;'）进行转义。

此语句仅在与 "stats auth" 配合使用时才有用，因为其仅与认证相关。

尽管仅凭此语句即可启用统计信息报告，但建议设置所有其他参数，以避免依赖默认的非显式参数。

示例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

另请参阅：“stats auth”、“stats enable”、“stats uri”

<a id="entry-4-2-stats-refresh"></a>

**`stats refresh <delay>`**

```haproxy
stats refresh <delay>
```

启用统计信息并自动刷新

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<delay>   是建议的刷新延迟，单位为秒，将返回给访问报告页面的浏览器。
          浏览器可自行采用其他延迟，但一般遵守此值，按此秒数间隔刷新页面。
          也可在数值后添加单位后缀，指定其他非默认时间单位，详见本文开头的说明。
```

此语句在显示负载均衡器活动的持续页面监控界面中非常有用。启用后，HTML 报告页面将包含一个“刷新”/“停止刷新”的链接，用户可选择是否需要页面自动刷新。

尽管仅凭此语句即可启用统计信息报告，但建议设置所有其他参数，以避免依赖默认的非显式参数。

示例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

另请参阅：“stats auth”、“stats enable”、“stats realm”、“stats uri”

<a id="entry-4-2-stats-scope"></a>

**`stats scope { <name> | "." }`**

```haproxy
stats scope { <name> | "." }
```

启用统计信息并限制访问范围

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<name>    是要报告的 listen、frontend 或 backend 段的名称。
          特殊名称 "."（单个点号）表示此语句所在的段。
```

当指定此语句时，报告中仅显示通过该语句列出的段。其余所有段将被隐藏，且在管理模式下尝试更改其状态的操作将被拒绝。若需报告多个段，可多次使用此语句。请注意，名称检查仅通过简单的字符串比较执行，且不会验证指定的段名称是否真实存在。

尽管仅凭此语句即可启用统计信息报告，但建议设置所有其他参数，以避免依赖默认的非显式参数。

示例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

另请参阅：“stats auth”、“stats enable”、“stats realm”、“stats uri”和“stats admin”

<a id="entry-4-2-stats-show-desc"></a>

**`stats show-desc [ <desc> ]`**

```haproxy
stats show-desc [ <desc> ]
```

在统计信息页面上启用描述信息的报告。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

    `<desc>`    为可选的要显示的描述。若未指定，将自动使用 global 段中的
              描述代替。

此语句对向客户提供共享服务的用户很有用，其中节点或描述应针对每位客户有所不同。

尽管仅凭此语句即可启用统计信息报告，但建议设置所有其他参数，以避免依赖默认的非显式参数。默认情况下，描述信息不会显示。

示例：

```shell
# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats show-desc Master node for Europe, Asia, Africa
    stats uri       /admin?stats
    stats refresh   5s
```

另请参阅全局段中的 "show-node"、"stats enable"、"stats uri" 和 "description"。

<a id="entry-4-2-stats-show-legends"></a>

**`stats show-legends`**

```haproxy
stats show-legends
```

启用在统计信息页面报告附加信息

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

启用在统计信息页面报告附加信息：   - cap：功能（代理）   - mode：tcp、http 或 health 之一（代理）   - id：SNMP ID（代理、套接字、服务器）   - IP（套接字、服务器）   - cookie（后端、服务器）

尽管仅此语句已足以启用统计信息报告，但建议设置所有其他参数，以避免依赖默认的非显式参数。默认行为是不显示此信息。

另请参阅：“stats enable”、“stats uri”。

<a id="entry-4-2-stats-show-modules"></a>

**`stats show-modules`**

```haproxy
stats show-modules
```

在统计信息页面启用额外的统计信息模块

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

新增列将作为提示工具栏，添加到包含额外统计信息值的行末尾。

尽管仅此语句已足以启用统计信息报告，但建议设置所有其他参数，以避免依赖默认的非显式参数。默认行为是不显示此信息。

另请参阅：“stats enable”、“stats uri”。

<a id="entry-4-2-stats-show-node"></a>

**`stats show-node [ <name> ]`**

```haproxy
stats show-node [ <name> ]
```

在统计信息页面上启用主机名报告。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<name>    是要报告的可选名称。未指定时，自动采用 global 段中的节点名称。
```

此语句对向客户提供共享服务的用户很有用，当为每位客户提供的统计页面中节点或描述信息不同时尤为适用。默认行为是不显示主机名。

尽管仅凭此语句即可启用统计信息报告，但建议设置所有其他参数，以避免依赖默认的非显式参数。

示例：

```shell
# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats show-node Europe-1
    stats uri       /admin?stats
    stats refresh   5s
```

另请参阅全局段中的“show-desc”、“stats enable”、“stats uri”和“node”。

<a id="entry-4-2-stats-show-version"></a>

**`stats show-version`**

```haproxy
stats show-version
```

启用统计信息并显示 HAProxy 版本报告

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：无

统计信息页面可报告一些有用的运行状态信息，包括 HAProxy 的版本。然而，通常认为向任何人披露精确版本号存在风险，因为这可能帮助攻击者针对已知漏洞实施特定攻击，因此默认情况下该功能被禁用。“stats show-version” 可启用版本信息的显示。对于公开站点或登录凭证较弱的站点，不建议启用此功能。

另请参阅：“stats auth”、“stats enable”、“stats realm”、“stats uri”、“stats hide-version”

<a id="entry-4-2-stats-uri"></a>

**`stats uri <prefix>`**

```haproxy
stats uri <prefix>
```

启用统计信息，并定义用于访问统计信息的 URI 前缀

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<prefix>  是将重定向到统计信息页面的所有 URI 的前缀。
          此前缀可以包含问号（'?'），用于指定查询字符串的一部分。
```

统计信息 URI 会在中继流量中被拦截，因此它会作为正常应用页面的一部分显示。强烈建议确保所选 URI 永远不会出现在应用中，否则将无法在应用中访问该页面。

HAProxy 内置的默认 URI 为 "/haproxy?stats"，但此值可在构建时更改，因此建议在此处始终显式指定。通常建议在 URI 中包含问号，以确保中间代理不会缓存结果。此外，由于任何以该前缀开头的字符串均会被视为统计信息请求，问号有助于确保没有任何有效 URI 会以相同字符串开头。

有时使用“/”作为 URI 前缀非常方便，可将该语句单独置于一个“listen”实例中。这样便于将某个地址或端口专门用于统计信息。

尽管仅凭此语句即可启用统计信息报告，但建议设置所有其他参数，以避免依赖默认的非显式参数。

示例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

另请参阅：“stats auth”、“stats enable”、“stats realm”

<a id="entry-4-2-stick-match"></a>

**`stick match <pattern> [table <table>] [{if | unless} <cond>]`**

```haproxy
stick match <pattern> [table <table>] [{if | unless} <cond>]
```

定义一个请求模式匹配条件，以将用户绑定到某台服务器

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

参数：

```text
<pattern>  是第 7.3 节所述的样本表达式规则，描述分析入站请求或连接中的哪些元素，
           以在粘性表中找到匹配条目。此规则为必需项。

<table>    是可选的粘性表名称，未指定时使用同一后端的表。粘性表通过 "stick-table" 语句声明。

<cond>     是可选的匹配条件，仅在其他条件满足（或不满足）时才按特定条件匹配。
           例如，通常按源 IP 地址匹配，但请求经过已知代理时，改为按包含该 IP 地址的头匹配。
```

某些协议或应用需要复杂的会话粘性规则，无法始终依赖 Cookie 或哈希机制。"stick match" 语句用于描述从传入请求或连接中提取会话粘性准则的规则。详见 [第 7 节](/zh/haproxy/acls-and-samples/)，其中列出了所有可能的模式和转换规则。

必须使用 "stick-table" 语句声明表格。表格类型必须与模式兼容。默认情况下，使用同一后端中存在的类型。可以通过使用 "table" 关键字引用其他后端的表格来共享表格。若引用了其他表格，则使用后端内服务器的 ID。默认情况下，每个后端内的服务器 ID 均从 1 开始，因此服务器顺序已足够。但若有疑问，强烈建议通过 "id" 设置显式指定服务器 ID。

可以使用“if”或“unless”后跟条件，来限制“stick match”语句适用的条件。参见 [第 7 节](/zh/haproxy/acls-and-samples/) 了解基于 ACL 的条件。

对“stick match”语句的数量没有限制。第一个匹配的语句将导致请求被导向与创建该条目时所用服务器相同的服务器。通过这种方式，可使用多个匹配作为备选方案。

会话粘性规则在持久化 Cookie 之后进行检查，因此如果已使用 Cookie 选择服务器，则这些规则不会影响会话粘性。通过这种方式，可以非常方便地插入 Cookie 并基于 IP 地址进行匹配，从而在 HTTP 与 HTTPS 之间维持会话粘性。

示例：

```shell
# forward SMTP users to the same server they just used for POP in the
# last 30 minutes
backend pop
    mode tcp
    balance roundrobin
    stick store-request src
    stick-table type ip size 200k expire 30m
    server s1 192.168.1.1:110
    server s2 192.168.1.1:110

backend smtp
    mode tcp
    balance roundrobin
    stick match src table pop
    server s1 192.168.1.1:25
    server s2 192.168.1.1:25
```

另请参阅：“stick-table”、“stick on”、[第 11 节](/zh/haproxy/stick-tables-and-peers/) 关于 stick-table 的说明，以及 [第 7 节](/zh/haproxy/acls-and-samples/) 关于 ACL 和样本提取的说明。

<a id="entry-4-2-stick-on"></a>

**`stick on <pattern> [table <table>] [{if | unless} <condition>]`**

```haproxy
stick on <pattern> [table <table>] [{if | unless} <condition>]
```

定义一个请求模式，用于将用户关联到服务器

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

请注意：此形式与“stick match”后接“stick store-request”完全等价，两者使用相同的参数。详情请参阅这两个关键字。仅作为编写更易维护配置的便利性而提供。

示例：

```shell
# The following form ...
stick on src table pop if !localhost

# ...is strictly equivalent to this one:
stick match src table pop if !localhost
stick store-request src table pop if !localhost


# Use cookie persistence for HTTP, and stick on source address for HTTPS as
# well as HTTP without cookie. Share the same table between both accesses.
backend http
    mode http
    balance roundrobin
    stick on src table https
    cookie SRV insert indirect nocache
    server s1 192.168.1.1:80 cookie s1
    server s2 192.168.1.1:80 cookie s2

backend https
    mode tcp
    balance roundrobin
    stick-table type ip size 200k expire 30m
    stick on src
    server s1 192.168.1.1:443
    server s2 192.168.1.1:443
```

另请参阅：“stick match”、“stick store-request”以及 [第 11 节](/zh/haproxy/stick-tables-and-peers/) 中关于 stick-tables 的内容。

<a id="entry-4-2-stick-store-request"></a>

**`stick store-request <pattern> [table <table>] [{if | unless} <condition>]`**

```haproxy
stick store-request <pattern> [table <table>] [{if | unless} <condition>]
```

定义用于在会话粘性表中创建条目的请求模式

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

参数：

```text
<pattern>  是第 7.3 节所述的样本表达式规则，描述在选择服务器之后，
           入站请求或连接中的哪些元素将被分析、提取并存储到表中。

<table>    是可选的粘性表名称，未指定时使用同一后端的表。粘性表通过 "stick-table" 语句声明。

<cond>     是可选的存储条件，仅在某些条件满足（或不满足）时才存储特定信息。
           例如，通常存储源 IP 地址，但请求经过已知代理时，改为存储包含该 IP 地址的头的转换结果。
```

某些协议或应用需要复杂的会话粘性规则，无法始终依赖 Cookie 或哈希。`stick store-request` 语句用于定义规则，说明应从请求中提取什么内容以及何时提取，以便将其存储到会话粘性表中，供后续请求通过 `stick match` 语句进行匹配。显然，所提取的部分必须具有实际意义，并且在后续请求中具备匹配的可能性。例如，存储客户端 IP 地址通常具有意义；存储 URL 参数中的 ID 也具有意义。而存储源端口几乎永远没有意义，因为其值会随机变化。有关可能的模式和转换规则的完整列表，请参见 [第 7 节](/zh/haproxy/acls-and-samples/)。

必须使用 "stick-table" 语句声明表格。表格类型必须与模式兼容。默认情况下，使用同一后端中存在的类型。可以通过使用 "table" 关键字引用其他后端的表格来共享表格。若引用了其他表格，则使用后端内服务器的 ID。默认情况下，每个后端内的服务器 ID 均从 1 开始，因此服务器顺序已足够。但若有疑问，强烈建议通过 "id" 设置显式指定服务器 ID。

可以使用“if”或“unless”后跟条件，来限制“stick store-request”语句适用的条件。该条件将在解析请求时进行评估，因此可使用任意判断标准。参见 [第 7 节](/zh/haproxy/acls-and-samples/) 了解基于 ACL 的条件。

无限制“stick store-request”语句的数量，但每个请求或响应最多允许同时存储 8 个。这使得无论规则数量多少，均可从请求或响应中提取最多 8 个条件并进行存储。仅保留前 8 个匹配的条件。利用此机制，可同时向多个表写入数据，以提高在其他协议或访问方式下识别用户的可能性。可以使用多个针对同一表的 store-request 规则，通过按优先级降序排列规则，以确定最可靠的判定依据。对于给定表，仅存储首个提取的条件。后续引用同一表的 store-request 规则将被跳过，其 ACL 也不会被评估。

"store-request" 规则在建立服务器连接后进行评估，因此表中将包含实际处理请求的服务器。

示例：

```shell
# forward SMTP users to the same server they just used for POP in the
# last 30 minutes
backend pop
    mode tcp
    balance roundrobin
    stick store-request src
    stick-table type ip size 200k expire 30m
    server s1 192.168.1.1:110
    server s2 192.168.1.1:110

backend smtp
    mode tcp
    balance roundrobin
    stick match src table pop
    server s1 192.168.1.1:25
    server s2 192.168.1.1:25
```

另请参阅：“stick-table”、“stick on”、[第 11 节](/zh/haproxy/stick-tables-and-peers/) 关于 stick-table 的说明，以及 [第 7 节](/zh/haproxy/acls-and-samples/) 关于 ACL 和样本提取的内容。

<a id="entry-4-2-stick-store-response"></a>

**`stick store-response <pattern> [table <table>] [{if | unless} <condition>]`**

```haproxy
stick store-response <pattern> [table <table>] [{if | unless} <condition>]
```

定义用于在会话粘性表中创建条目的响应模式

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

参数：

```text
<pattern>  是第 7.3 节所述的样本表达式规则，描述在选择服务器之后，
           响应或连接中哪些元素将被分析、提取并存储到表中。

<table>    是可选的粘性表名称，未指定时使用同一后端的表。粘性表通过 "stick-table" 语句声明。

<cond>     是可选的存储条件，仅在某些条件满足（或不满足）时存储特定信息。
           例如，仅当响应为 SSL server hello 时存储 SSL 会话 ID。
```

某些协议或应用需要复杂的会话粘性规则，无法始终依赖 Cookie 或哈希。`stick store-response` 语句用于定义规则，说明从响应中提取什么内容以及何时提取，以便将其存储到会话粘性表中，供后续请求通过 `stick match` 语句进行匹配。显然，所提取的内容必须具有意义，并且在后续请求中具备匹配的可能性。例如，从响应头中提取 ID 是合理的。详见 [第 7 节](/zh/haproxy/acls-and-samples/)，获取所有可能的匹配模式和转换规则的完整列表。

必须使用 "stick-table" 语句声明表格。表格类型必须与模式兼容。默认情况下，使用同一后端中存在的类型。可以通过使用 "table" 关键字引用其他后端的表格来共享表格。若引用了其他表格，则使用后端内服务器的 ID。默认情况下，每个后端内的服务器 ID 均从 1 开始，因此服务器顺序已足够。但若有疑问，强烈建议通过 "id" 设置显式指定服务器 ID。

可以使用“if”或“unless”后跟条件来限制“stick store-response”语句适用的条件。该条件将在解析响应时进行评估，因此可使用任意判断标准。参见 [第 7 节](/zh/haproxy/acls-and-samples/) 了解基于 ACL 的条件。

本节中，“stick store-response” 语句的数量没有限制，但每个请求或响应最多只能同时存储 8 个数据。这使得无论规则数量多少，均可从请求或响应中提取最多 8 个条件并进行存储。仅保留前 8 个匹配的条件。利用此机制，可同时向多个表写入数据，以提高在其他协议或访问方式下识别用户的可能性。可以使用多个针对同一表的 store-response 规则，通过按优先级降序排列规则，以确定最可靠的判定依据。对于给定表，仅存储第一个提取的条件。后续引用同一表的 store-response 规则将被跳过，其 ACL 也不会被评估。然而，即使某个 store-request 规则引用了某表，store-response 规则仍可使用同一表。这意味着每个表可同时从请求和响应中各学习一个元素。

该表将包含处理请求的真实服务器。

示例：

```shell
# Learn SSL session ID from both request and response and create affinity.
backend https
    mode tcp
    balance roundrobin
    # maximum SSL session ID length is 32 bytes.
    stick-table type binary len 32 size 30k expire 30m

    acl clienthello req.ssl_hello_type 1
    acl serverhello res.ssl_hello_type 2

    # use tcp content accepts to detects ssl client and server hello.
    tcp-request inspect-delay 5s
    tcp-request content accept if clienthello

    # no timeout on response inspect delay by default.
    tcp-response content accept if serverhello

    # SSL session ID (SSLID) may be present on a client or server hello.
    # Its length is coded on 1 byte at offset 43 and its value starts
    # at offset 44.

    # Match and learn on request if client hello.
    stick on req.payload_lv(43,1) if clienthello

    # Learn on response if server hello.
    stick store-response resp.payload_lv(43,1) if serverhello

    server s1 192.168.1.1:443
    server s2 192.168.1.1:443
```

另请参阅：“stick-table”、“stick on”、[第 11 节](/zh/haproxy/stick-tables-and-peers/) 关于 stick-table 的说明，以及 [第 7 节](/zh/haproxy/acls-and-samples/) 关于 ACL 和模式提取的内容。

<a id="entry-4-2-stick-table-type"></a>

**`stick-table type <type> size <size> [expire <expire>] [args...]`**

```haproxy
stick-table type <type> size <size> [expire <expire>] [args...]
```

配置当前段的会话粘性表

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| yes

用于声明和配置 stick-table。请参阅 [第 11.1 节](/zh/haproxy/stick-tables-and-peers/#section-11-1) 以获取完整说明及支持的参数列表。仅类型和大小为必填项。

<a id="entry-4-2-tcp-check-comment"></a>

**`tcp-check comment <string>`**

```haproxy
tcp-check comment <string>
```

为后续的 tcp-check 规则定义注释，若该规则执行失败，将在日志中报告。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<string>  是后续 tcp-check 规则失败时添加到日志中的注释消息。
```

仅适用于 connect、send 和 expect 规则。可用于生成用户友好的错误报告。

另请参阅：“option tcp-check”、“tcp-check connect”、“tcp-check send”和“tcp-check expect”。

<a id="entry-4-2-tcp-check-connect"></a>

**`tcp-check connect [default] [port <expr>] [addr <ip>] [send-proxy] [via-socks4]`**

```haproxy
tcp-check connect [default] [port <expr>] [addr <ip>] [send-proxy] [via-socks4]
                  [ssl] [sni <sni>] [alpn <alpn>] [linger]
                  [proto <name>] [comment <msg>]
```

打开一个新连接

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
comment <msg>  定义规则求值失败时报告的消息。

default      使用 server 行的默认选项进行健康检查，仅使用未被重新定义的服务器选项。

port <expr>  未设置时，使用检查端口或服务器端口，指定 HAProxy 连接的位置。
             <port> 必须为 1 到 65535 的有效 TCP 端口整数，或样本提取表达式。

addr <ip>    定义健康检查使用的 IP 地址。

send-proxy   发送 PROXY 协议字符串。

via-socks4   通过上游 socks4 代理执行出站健康检查。

ssl          打开加密连接。

sni <sni>    指定通过 SSL 执行健康检查时使用的 SNI。

alpn <alpn>  定义通过 ALPN 通告的协议。协议列表由逗号分隔的协议名称组成，
             例如 "http/1.1,http/1.0"（不含引号）。未设置时使用服务器的 ALPN。

proto <name> 强制此连接使用指定的多路复用器协议，必须为可在后端侧使用的 TCP 复用协议。
             可用协议列表通过 haproxy -vv 报告。

linger       干净地关闭连接，而非仅发送 RST。
```

当应用程序运行在多个 TCP 端口上，或 HAProxy 在单个后端中对多个服务进行负载均衡时，在将服务器视为正常运行之前，分别探测所有服务是有意义的。

当服务器行上未配置 TCP 端口，且未使用 server port 指令时，则必须将 'tcp-check connect port `<port>`' 作为序列中的第一步。

在 tcp-check 规则集中，必须包含一个 'connect' 规则，且规则集必须以 'connect' 规则开头。此举旨在确保管理员清楚了解其操作意图。

当连接必须启动规则集时，仍可由 set-var、unset-var 或 comment 规则先行。

示例：

```shell
# check HTTP and HTTPs services on a server.
# first open port 80 thanks to server line port directive, then
# tcp-check opens port 443, ciphered and run a request on it:
option tcp-check
tcp-check connect
tcp-check send GET\ /\ HTTP/1.0\r\n
tcp-check send Host:\ haproxy.1wt.eu\r\n
tcp-check send \r\n
tcp-check expect rstring (2..|3..)
tcp-check connect port 443 ssl
tcp-check send GET\ /\ HTTP/1.0\r\n
tcp-check send Host:\ haproxy.1wt.eu\r\n
tcp-check send \r\n
tcp-check expect rstring (2..|3..)
server www 10.0.0.1 check port 80

# check both POP and IMAP from a single server:
option tcp-check
tcp-check connect port 110 linger
tcp-check expect string +OK\ POP3\ ready
tcp-check connect port 143
tcp-check expect string *\ OK\ IMAP4\ ready
server mail 10.0.0.1 check
```

另请参阅："option tcp-check"、"tcp-check send"、"tcp-check expect"

<a id="entry-4-2-tcp-check-expect"></a>

**`tcp-check expect [min-recv <int>] [comment <msg>]`**

```haproxy
tcp-check expect [min-recv <int>] [comment <msg>]
                 [ok-status <st>] [error-status <st>] [tout-status <st>]
                 [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                 [!] <match> <pattern>
```

指定在通用健康检查期间要收集和分析的数据

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
comment <msg>  定义规则求值失败时报告的消息。

min-recv  是可选参数，定义对当前 expect 规则求值所需的最少数据量。
          接收字节数低于此限制时，检查等待更多数据。可用于消除匹配规则的歧义，
          或避免对已知尚不完整的内容执行昂贵的正则匹配。
          使用精确字符串（string 或 binary）时，取字符串长度与此参数的较小值。
          设为 -1 时忽略此参数；expect 规则不匹配时，检查等待更多数据。
          设为 0 时，求值结果始终是确定的。

ok-status <st>     是可选参数，在 expect 规则求值成功且为 tcp-check 规则集的最后一条规则时，
                   设置检查状态。支持 "L7OK"、"L7OKC"、"L6OK" 和 "L4OK"：
                     - L7OK : 第 7 层检查通过
                     - L7OKC: 第 7 层检查有条件通过，将服务器设为 NOLB 状态
                     - L6OK : 第 6 层检查通过
                     - L4OK : 第 4 层检查通过
                   默认使用 "L7OK"。

error-status <st>  是可选参数，在 expect 规则求值发生错误时设置检查状态。
                   支持 "L7OKC"、"L7RSP"、"L7STS"、"L6RSP" 和 "L4CON"：
                     - L7OKC: 第 7 层检查有条件通过，将服务器设为 NOLB 状态
                     - L7RSP: 第 7 层响应无效：协议错误
                     - L7STS: 第 7 层响应错误，例如 HTTP 5xx
                     - L6RSP: 第 6 层响应无效：协议错误
                     - L4CON: 第 1-4 层连接问题
                   默认使用 "L7RSP"。

tout-status <st>   是可选参数，在 expect 规则求值超时时设置检查状态。
                   支持 "L7TOUT"、"L6TOUT" 和 "L4TOUT"：
                     - L7TOUT: 第 7 层（HTTP/SMTP）超时
                     - L6TOUT: 第 6 层（SSL）超时
                     - L4TOUT: 第 1-4 层超时
                   默认使用 "L7TOUT"。

on-success <fmt>   是可选参数，在 expect 规则求值成功且为 tcp-check 规则集的最后一条规则时，
                   自定义日志中报告的信息消息。<fmt> 为自定义日志格式字符串（参见第 8.2.6 节）。

on-error <fmt>     是可选参数，在 expect 规则求值发生错误时，自定义日志中报告的信息消息。
                   <fmt> 为自定义日志格式字符串（参见第 8.2.6 节）。

status-code <expr> 是可选参数，设置成功或错误时在日志中报告的检查状态码。
                   <expr> 是标准 HAProxy 表达式，由样本提取后接若干转换器构成。

<match>   指定如何在响应中查找特定模式，可为 "string"、"rstring"、"binary" 或 "rbinary"。
          关键字前可加感叹号（"!"）来反转匹配。感叹号与关键字之间允许空格。
          所支持关键字的更多详情见下文。

<pattern> 是要查找的模式，可为字符串或正则表达式。
          包含空格时，必须用通常的反斜杠（'\'）转义。
          使用 binary 匹配时，模式必须为偶数个十六进制数字，每两个数字表示一个字节。
          十六进制数字可使用大写或小写。
```

可用的匹配项与它们的 http-check 对应项故意设计得相似：

```text
string <string>: 检查响应缓冲区中的精确字符串匹配。
                  缓冲区包含此字符串时，健康检查响应视为有效。
                  "string" 前加 "!" 时，消息体包含该字符串则将响应视为无效。
                  可用于查找协议响应中必需的模式，或在协议标语出现特定错误时检测故障。

rstring <regex>: 对响应缓冲区进行正则表达式检查。
                  缓冲区匹配表达式时，健康检查响应视为有效。
                  "rstring" 前加 "!" 时，消息体匹配表达式则将响应视为无效。

string-lf <fmt>: 在响应缓冲区中匹配自定义日志格式。
                  缓冲区包含对 <fmt> 按第 8.2.6 节自定义日志格式规则求值得到的字符串时，
                  健康检查响应视为有效。前加 "!" 时，缓冲区包含字符串则将响应视为无效。

binary <hexstring>: 检查响应缓冲区中是否精确匹配十六进制形式的字符串。
                     缓冲区包含该十六进制字符串时，健康检查响应视为有效，用于匹配二进制协议中的数据。

rbinary <regex>: 类似 "rstring"，对响应缓冲区进行正则表达式检查，
                  但先将缓冲区转换为十六进制形式，包括 NUL 字节，
                  使所有正则引擎均可匹配任意二进制内容。
                  十六进制转换占用原始响应的两倍空间，因此预期模式最多只能覆盖响应缓冲区的一半。

binary-lf <hexfmt>: 在响应缓冲区中匹配十六进制形式的自定义日志格式。
                     缓冲区包含对 <fmt> 按自定义日志格式规则（参见第 8.2.6 节）求值得到的十六进制字符串时，
                     健康检查响应视为有效。前加 "!" 时，缓冲区包含此字符串则将响应视为无效。
                     匹配前，先将十六进制字符串转换为二进制字符串。
```

请注意，响应内容大小将受到全局 "tune.bufsize" 选项的限制，该选项默认值为 16384 字节。因此，当使用 "string"、"rstring" 或二进制模式时，过大的响应可能无法包含必需的模式。若确实需要处理大尺寸响应，可通过设置全局变量更改默认最大尺寸。但需注意，解析非常大的响应会消耗部分 CPU 资源，尤其是在使用正则表达式时，且始终建议将检查聚焦于较小的资源。此外，当前状态下，检查无法在响应中的空字符之后匹配任何字符串或正则表达式。同样，无法请求匹配空字符。

示例：

```shell
# perform a POP check
option tcp-check
tcp-check expect string +OK\ POP3\ ready

# perform an IMAP check
option tcp-check
tcp-check expect string *\ OK\ IMAP4\ ready

# look for the redis master server
option tcp-check
tcp-check send PING\r\n
tcp-check expect string +PONG
tcp-check send info\ replication\r\n
tcp-check expect string role:master
tcp-check send QUIT\r\n
tcp-check expect string +OK

```

另请参阅：option tcp-check、tcp-check connect、tcp-check send、tcp-check send-binary、http-check expect、tune.bufsize

<a id="entry-4-2-tcp-check-send"></a>

**`tcp-check send <data> [comment <msg>]`**

```haproxy
tcp-check send <data> [comment <msg>]
tcp-check send-lf <fmt> [comment <msg>]
```

指定一个字符串或自定义日志格式，作为通用健康检查中的问题发送

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
comment <msg>  定义规则求值失败时报告的消息。

<data>         是通用健康检查会话中发送的字符串。

<fmt>          是通用健康检查会话中求值后发送的自定义日志格式（参见第 8.2.6 节）。
```

示例：

```shell
# look for the redis master server
option tcp-check
tcp-check send info\ replication\r\n
tcp-check expect string role:master
```

另请参阅："option tcp-check"、"tcp-check connect"、"tcp-check expect"、"tcp-check send-binary"、"tune.bufsize"

<a id="entry-4-2-tcp-check-send-binary"></a>

**`tcp-check send-binary <hexstring> [comment <msg>]`**

```haproxy
tcp-check send-binary <hexstring> [comment <msg>]
tcp-check send-binary-lf <hexfmt> [comment <msg>]
```

指定十六进制数字字符串或十六进制数字自定义日志格式，作为原始 TCP 健康检查期间的二进制查询发送

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
comment <msg>  定义规则求值失败时报告的消息。

<hexstring>    是通用健康检查会话中转换为二进制后发送的十六进制字符串。

<hexfmt>       是通用健康检查会话中求值并转换为二进制后发送的十六进制自定义日志格式
               （参见第 8.2.6 节）。
```

示例：

```shell
# redis check in binary
option tcp-check
tcp-check send-binary 50494e470d0a # PING\r\n
tcp-check expect binary 2b504F4e47 # +PONG

```

另请参阅："option tcp-check"、"tcp-check connect"、"tcp-check expect"、"tcp-check send"、"tune.bufsize"

<a id="entry-4-2-tcp-check-set-var"></a>

**`tcp-check set-var(<var-name>[,<cond>...]) <expr>`**

```haproxy
tcp-check set-var(<var-name>[,<cond>...]) <expr>
tcp-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
```

此操作用于设置变量的内容。变量在行内声明。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<var-name>   是变量名称。仅可使用 "proc"、"sess" 和 "check" 作用域。详情见第 2.8 节的变量说明。

 <cond>      是一组条件，必须全部为真才会实际设置变量（例如 "ifnotempty"、"ifgt" 等）。
             所有可用条件见 set-var 转换器的说明。

 <expr>      是样本提取表达式，其后可接转换器。

 <fmt>       是以自定义日志格式表示的值（参见第 8.2.6 节的自定义日志格式）。
```

示例：

```text
tcp-check set-var(check.port) int(1234)
tcp-check set-var-fmt(check.name) "%H"

```

<a id="entry-4-2-tcp-check-unset-var"></a>

**`tcp-check unset-var(<var-name>)`**

```haproxy
tcp-check unset-var(<var-name>)
```

释放变量在其作用域内的引用。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<var-name>   是变量名称。仅可使用 "proc"、"sess" 和 "check" 作用域。详情见第 2.8 节的变量说明。
```

示例：

```text
tcp-check unset-var(check.port)

```

<a id="entry-4-2-tcp-request-connection"></a>

**`tcp-request connection <action> <options...> [ { if | unless } <condition> ]`**

```haproxy
tcp-request connection <action> <options...> [ { if | unless } <condition> ]
```

根据第 4 层条件对传入连接执行相应动作

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes(!) \| yes \| yes \| no

参数：

```text
<action>    定义条件成立时执行的动作，参见下文。

<condition> 是仅基于第4层的标准 ACL 条件（参见第 7 节）。
```

在新连接建立后立即，可评估某些条件，以决定该连接是否应被接受、丢弃或对其计数器进行跟踪。由于连接尚未读取，缓冲区也尚未分配，因此这些条件无法使用任何数据内容。此机制可用于以极低开销，快速且有选择性地接受或丢弃来自不同源的连接。若需检查部分内容才能做出决策，则应改用 "tcp-request content" 语句。

“tcp-request connection” 规则按其声明顺序精确评估。若无规则匹配或未定义规则，缺省动作是接受入站连接。可插入的规则数量无特定限制。任何规则均可选择性地跟随一个基于 ACL 的条件，此时仅当该条件求值为真时才进行评估。

条件在动作执行前进行评估，且该动作仅执行一次。因此，即使某个动作改变了作为条件一部分的元素，也不会造成问题。这也意味着多个动作可以依赖同一条件，只要首个改变条件评估结果的动作执行后，其余动作便会自动隐式禁用。例如，当变量为空时，从多个来源为其赋值时即采用此机制。

在 "tcp-request connection" 语法中，首个关键字为规则的动作，可选地后接该动作所需的若干参数。支持的动作及其对应语法详见 [第 4.3 节](/zh/haproxy/proxies/#section-4-3)“动作”（请查找标记为“TCP RqCon”的动作）。

该指令仅在命名的 defaults 段中可用，不可用于匿名段。在关联的代理段之前，将先评估 defaults 段中定义的规则。为避免歧义，在此情况下，同一 defaults 段不可同时被具备前端能力的代理和具备后端能力的代理使用。这意味着，listen 段不可使用定义了此类规则的 defaults 段。

请注意，“if/unless” 条件是可选的。若未在动作中设置条件，则该动作将无条件执行。这在执行 “track-sc\*” 动作时同样有用，也可用于将默认动作更改为拒绝。

示例：接受白名单主机的所有连接，拒绝过快的连接（不计入统计），并跟踪已接受的连接。这会导致来自恶意源的连接速率被限制。

        tcp-request connection accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request connection reject if { src_conn_rate gt 10 }
        tcp-request connection track-sc0 src

示例：接受来自白名单主机的所有连接，统计其他所有连接，并拒绝过快的连接。这会导致滥用行为被阻止，只要其未降低速率。

        tcp-request connection accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request connection track-sc0 src
        tcp-request connection reject if { sc0_conn_rate gt 10 }

示例：为所有已知代理传入的流量启用 PROXY 协议。

        tcp-request connection expect-proxy layer4 if { src -f proxies.lst }

请参阅 [第 7 节](/zh/haproxy/acls-and-samples/) 了解 ACL 的使用方法。

另请参阅：“tcp-request session”、“tcp-request content”、“stick-table”

<a id="entry-4-2-tcp-request-content"></a>

**`tcp-request content <action> [{if | unless} <condition>]`**

```haproxy
tcp-request content <action> [{if | unless} <condition>]
```

根据第 4 层至第 7 层的条件，对新会话执行相应动作

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes(!) \| yes \| yes \| yes

参数：

```text
<action>    定义条件成立时执行的动作，参见下文。

<condition> 是基于第 4-7 层的标准 ACL 条件（参见第 7 节）。
```

在称为“TCP 内容检查”的请求处理早期阶段，可以分析请求内容。在此阶段，每当请求内容更新时，都会评估基于 ACL 的规则，直到匹配到“accept”、“reject”或“switch-mode”规则，或者 TCP 请求检查延迟超时且未匹配任何规则为止。

第一个区别在于，“tcp-request content” 规则可以利用内容来做出决策。大多数情况下，这些决策会涉及协议识别或有效性判断。第二个区别在于，基于内容的规则可在前端和后端中使用。在客户端启用 HTTP 持久连接的情况下，所有 “tcp-request content” 规则都会被重新评估，因此 HAProxy 会记录由 “tcp-request connection” 规则与 “tcp-request content” 规则分配的粘性计数器，且在处理完一个 HTTP 请求后，会清除所有与内容相关的计数器，以便在下一个请求的规则重新评估时再次进行判断。当规则跟踪某些 L7 信息，或基于 L7 ACL 条件时，这一点尤为重要，因为跟踪状态可能在请求之间发生变化。

基于内容的规则按其声明顺序逐一评估。若无规则匹配或未定义规则，缺省动作是接受内容。可插入的规则数量无特定限制。

尽管并非强制要求，但建议在“tcp-request connection”规则中使用 track-sc0，在前端的“tcp-request content”规则中使用 track-sc1，在后端的“tcp-request content”规则中使用 track-sc2。这样做可使配置更具可读性，更易于排查故障，但此仅为指导建议，所有计数器均可在任意位置使用。

在语法中，“tcp-request content” 后的第一个关键字是规则的动作，可选地后接该动作所需的若干参数。支持的动作及其相应语法详见 [第 4.3 节](/zh/haproxy/proxies/#section-4-3) “动作”（请查找标记为“TCP RqCnt”的动作）。

该指令仅在命名的 defaults 段中可用，不可用于匿名段。在关联的代理段之前，将先评估 defaults 段中定义的规则。为避免歧义，在此情况下，同一 defaults 段不可同时被具备前端能力的代理和具备后端能力的代理使用。这意味着，listen 段不可使用定义了此类规则的 defaults 段。

请注意，“if/unless” 条件是可选的。若未在动作中设置条件，则该动作将无条件执行。这在执行 “track-sc\*” 动作时同样有用，也可用于将默认动作更改为拒绝。

请注意，建议使用“tcp-request session”规则来跟踪不依赖第 7 层内容的信息，尤其是在 HTTP 前端中。部分 HTTP 处理在会话级别执行，可能导致请求被提前拒绝。在这种情况下，内容级别的跟踪可能会受到影响。启动时会发出警告，以尽可能防止此类不可靠的使用方式。

可以在 TCP 代理中使用“tcp-request content”规则匹配第 7 层内容，因为 HTTP 特定的 ACL 匹配能够在提取所需数据前，预先解析缓冲区中的内容。如果缓冲区内容无法解析为有效的 HTTP 消息，则 ACL 不会匹配。此处涉及的解析器与所有其他 HTTP 处理所用的解析器完全相同，因此不存在解析结果不同的风险。在 HTTP 前端或 HTTP 后端中，可以保证在规则首次评估时，HTTP 内容始终立即可用，因为 HTTP 解析在连接处理的早期阶段、会话级别即已完成。但对于此类代理，使用“http-request”规则更为自然且建议采用。

跟踪 Layer7 信息也是可行的，前提是规则处理时相关信息已存在。规则处理引擎在待跟踪数据尚未可用时，能够等待直到检查延迟到期。

示例：

```text
tcp-request content use-service lua.deny if { src -f /etc/haproxy/blacklist.lst }
```

示例：

```text
tcp-request content set-var(sess.my_var) src
tcp-request content set-var-fmt(sess.from) %[src]:%[src_port]
tcp-request content unset-var(sess.my_var2)
```

示例：

```shell
# Accept HTTP requests containing a Host header saying "example.com"
# and reject everything else. (Only works for HTTP/1 connections)
acl is_host_com hdr(Host) -i example.com
tcp-request inspect-delay 30s
tcp-request content accept if is_host_com
tcp-request content reject

# Accept HTTP requests containing a Host header saying "example.com"
# and reject everything else. (works for HTTP/1 and HTTP/2 connections)
acl is_host_com hdr(Host) -i example.com
tcp-request inspect-delay 5s
tcp-request content switch-mode http if HTTP
tcp-request content reject   # non-HTTP traffic is implicit here
...
http-request reject unless is_host_com
```

示例：

```shell
# reject SMTP connection if client speaks first
tcp-request inspect-delay 30s
acl content_present req.len gt 0
tcp-request content reject if content_present

# Forward HTTPS connection only if client speaks
tcp-request inspect-delay 30s
acl content_present req.len gt 0
tcp-request content accept if content_present
tcp-request content reject
```

示例：

```shell
# Track the last IP(stick-table type string) from X-Forwarded-For
tcp-request inspect-delay 10s
tcp-request content track-sc0 hdr(x-forwarded-for,-1)
# Or track the last IP(stick-table type ip|ipv6) from X-Forwarded-For
tcp-request content track-sc0 req.hdr_ip(x-forwarded-for,-1)
```

示例：

```shell
# track request counts per "base" (concatenation of Host+URL)
tcp-request inspect-delay 10s
tcp-request content track-sc0 base table req-rate
```

示例：跟踪每个前端和后端的计数器，当后端检测到滥用行为（并标记 gpc0）时，在前端阻止滥用者。

        frontend http
            # Use General Purpose Counter 0 in SC0 as a global abuse counter
            # protecting all our sites
            stick-table type ip size 1m expire 5m store gpc0
            tcp-request connection track-sc0 src
            tcp-request connection reject if { sc0_get_gpc0 gt 0 }
            ...
            use_backend http_dynamic if { path_end .php }

        backend http_dynamic
            # if a source makes too fast requests to this dynamic site (tracked
            # by SC1), block it globally in the frontend.
            stick-table type ip size 1m expire 5m store http_req_rate(10s)
            acl click_too_fast sc1_http_req_rate gt 10
            acl mark_as_abuser sc0_inc_gpc0(http) gt 0
            tcp-request content track-sc1 src
            tcp-request content reject if click_too_fast mark_as_abuser

请参阅 [第 7 节](/zh/haproxy/acls-and-samples/) 了解 ACL 的使用方法。

另请参阅：“tcp-request connection”、“tcp-request session”、“tcp-request inspect-delay” 和 “http-request”。

<a id="entry-4-2-tcp-request-inspect-delay"></a>

**`tcp-request inspect-delay <timeout>`**

```haproxy
tcp-request inspect-delay <timeout>
```

设置内容检查期间允许等待数据的最大时间

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes(!) \| yes \| yes \| yes

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

主要用 HAProxy 作为 TCP 中继的用户，通常会担心未经分析就将任意类型的协议传递给服务器所带来的风险。为了能够分析请求内容，我们必须首先暂存数据，然后再进行分析。此配置项仅用于指定最多暂存数据的时间。

TCP 内容检查在连接到达前端时即刻生效，随后在连接被转发至后端时再次立即生效。这意味着，若前端和后端均配置了 tcp-request 规则，连接可能会经历一次前端延迟和一次后端延迟。

请注意，执行内容检查时，HAProxy 会针对每个新到达的数据块完整评估所有规则，同时考虑这些数据是不完整的事实。如果在前述延迟时间之前没有规则匹配，则在延迟到期时会进行最后一次检查，此时将视内容为最终确定。若未设置延迟，HAProxy 将不会等待，而是立即根据现有信息作出判定。显然，这种情况通常无实际用途，甚至可能产生竞态条件，因此不建议采用此类配置。

请注意，若发生连接错误或关闭，或请求缓冲区显示为满，则检查延迟将缩短。

一旦规则匹配，请求即被释放，并继续正常处理。如果达到超时且无规则匹配，将采用默认策略，允许请求不受影响地通过。

对于大多数协议，将其设置为几秒即可，因为大多数客户端在建立连接后会立即发送完整请求。为覆盖 TCP 重传情况，可额外增加 3 秒或更多，但无需更多。对于某些协议，使用较大值可能更合理，例如确保客户端在服务器之前从不发送数据（如 SMTP），或等待客户端先发送数据后再将数据传递给服务器（如 SSL）。请注意，客户端超时必须至少覆盖检查延迟，否则将先于检查延迟到期。若客户端关闭连接或缓冲区已满，延迟将立即失效，因为内容已无法再更改。

该指令仅在命名的默认段中可用，不可用于匿名段。代理会从其默认段继承此值。

另请参阅：“tcp-request content accept”、“tcp-request content reject”、“timeout client”。

<a id="entry-4-2-tcp-request-session"></a>

**`tcp-request session <action> [{if | unless} <condition>]`**

```haproxy
tcp-request session <action> [{if | unless} <condition>]
```

根据第 5 层条件，对已验证的会话执行相应动作

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes(!) \| yes \| yes \| no

参数：

```text
<action>    定义条件成立时执行的动作，参见下文。

<condition> 是仅基于第5层的标准 ACL 条件（参见第 7 节）。
```

会话验证完成后（即所有握手均已结束），可评估某些条件，以决定该会话是否应被接受、丢弃或对其计数器进行跟踪。这些条件无法使用任何数据内容，因为此时尚未分配缓冲区，且处理在此阶段不能等待。主要用例是将一些早期信息复制到变量中（因为变量在会话中可访问），或跟踪握手后收集的信息，例如 SSL 层级元素（SNI、加密套件、客户端证书的 CN）或 PROXY 协议头中的信息（例如，跟踪通过此方式转发的源地址）。提取的信息可复制到变量中，或使用 "track-sc" 规则进行跟踪。当然，也可在此处决定接受或拒绝，如同其他规则集一样。此处执行的大多数操作也可在 "tcp-request content" 规则中完成，但 HTTP 情况下这些规则会对每个新请求进行评估，这可能并不总是可接受的。例如，规则可能在每次评估时递增计数器。也有可能通过地理位置解析源 IP 地址，将其赋值给会话级变量，然后对所有请求重写源地址为 HTTP 头中的值。若需检查某些内容以作出决策，则必须改用 "tcp-request content" 语句。

"tcp-request session" 规则按其声明顺序精确评估。若无规则匹配或未定义规则，缺省动作是接受入站会话。可插入的规则数量无特定限制。

在 "tcp-request session" 语法中，首个关键字为规则的动作，可选地后接该动作所需的若干参数。支持的动作及其对应语法详见 [第 4.3 节](/zh/haproxy/proxies/#section-4-3) “动作”（请查找标记为“TCP RqSes”的动作）。

该指令仅在命名的 defaults 段中可用，不可用于匿名段。在关联的代理段之前，将先评估 defaults 段中定义的规则。为避免歧义，在此情况下，同一 defaults 段不可同时被具备前端能力的代理和具备后端能力的代理使用。这意味着，listen 段不可使用定义了此类规则的 defaults 段。

请注意，“if/unless” 条件是可选的。若未在动作中设置条件，则该动作将无条件执行。这在执行 “track-sc\*” 动作时同样有用，也可用于将默认动作更改为拒绝。

示例：默认跟踪原始源地址，或来自本地代理的连接中 PROXY 协议所通告的地址。第一条连接级别规则启用对这些连接的 PROXY 协议接收，第二条规则跟踪在可选解码后我们决定保留的任意地址。

        tcp-request connection expect-proxy layer4 if { src -f proxies.lst }
        tcp-request session track-sc0 src

示例：接受来自白名单主机的所有会话，拒绝过快的会话而不进行计数，并跟踪已接受的会话。这会导致来自恶意源的会话速率被限制。

        tcp-request session accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request session reject if { src_sess_rate gt 10 }
        tcp-request session track-sc0 src

示例：接受来自白名单主机的所有会话，统计其他所有会话，并拒绝过快的会话。这会导致滥用行为在未放慢速度前持续被阻止。

        tcp-request session accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request session track-sc0 src
        tcp-request session reject if { sc0_sess_rate gt 10 }

请参阅 [第 7 节](/zh/haproxy/acls-and-samples/) 了解 ACL 的使用方法。

另请参阅："tcp-request connection"、"tcp-request content"、"stick-table"

<a id="entry-4-2-tcp-response-content"></a>

**`tcp-response content <action> [{if | unless} <condition>]`**

```haproxy
tcp-response content <action> [{if | unless} <condition>]
```

根据第 4 层至第 7 层的条件，对会话响应执行动作

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes(!) \| no \| yes \| yes

参数：

```text
<action>    定义条件成立时执行的动作，参见下文。

<condition> 是基于第 4-7 层的标准 ACL 条件（参见第 7 节）。
```

响应内容可在响应处理的早期阶段——“TCP 内容检查”阶段进行分析。在此阶段，每当响应内容更新时，都会评估基于 ACL 的规则，直到满足以下任一条件：匹配到最终规则，或设置了 TCP 响应内容检查延迟且该延迟超时而未匹配到任何规则。

通常情况下，这些决策会考虑协议识别或有效性。

基于内容的规则按其声明顺序逐一评估。若无规则匹配或未定义规则，缺省动作是接受内容。可插入的规则数量无特定限制。

在语法中，“tcp-response content”之后的第一个关键字是规则的动作，可选地后接该动作所需的任意数量参数。支持的动作及其相应语法详见 [第 4.3 节](/zh/haproxy/proxies/#section-4-3)“动作”（请查找标记为“TCP RsCnt”的动作）。

该指令仅在命名的 defaults 段中可用，不可用于匿名段。在关联的代理段之前，将先评估 defaults 段中定义的规则。为避免歧义，在此情况下，同一 defaults 段不可同时被具备前端能力的代理和具备后端能力的代理使用。这意味着，listen 段不可使用定义了此类规则的 defaults 段。

请注意，“if/unless” 条件是可选的。若未在动作中设置条件，则该动作将无条件执行。这在将默认动作更改为拒绝时可能很有用。

支持多种类型的动作：

可以使用 "tcp-response content" 规则匹配第 7 层内容，但必须确保已完整缓冲响应内容，否则将无法匹配任何内容。为实现此目的，最佳方案是在检测期间识别 HTTP 协议。

请参阅 [第 7 节](/zh/haproxy/acls-and-samples/) 了解 ACL 的使用方法。

另请参阅："tcp-request content"，"tcp-response inspect-delay"

<a id="entry-4-2-tcp-response-inspect-delay"></a>

**`tcp-response inspect-delay <timeout>`**

```haproxy
tcp-response inspect-delay <timeout>
```

设置在内容检查期间等待响应的最大允许时间

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes(!) \| no \| yes \| yes

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

该指令仅在命名的默认段中可用，不可用于匿名段。代理会从其默认段继承此值。

另请参阅：“tcp-response content”、“tcp-request inspect-delay”。

<a id="entry-4-2-timeout-check"></a>

**`timeout check <timeout>`**

```haproxy
timeout check <timeout>
```

设置额外的检查超时，但仅在连接已成功建立后生效。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

若启用，HAProxy 将使用 min("timeout connect", "inter") 作为检查的连接超时，同时使用 "timeout check" 作为额外的读取超时。使用 "min" 是为了避免那些设置了极长 "timeout connect"（例如因队列或 tarpit 机制而需要如此设置）的用户降低检查速度。（请注意，没有任何合理理由需要设置如此长的连接超时，因为始终可以使用 "timeout queue" 和 "timeout tarpit" 来避免这种情况）。

若未设置“timeout check”，HAProxy 将使用“inter”作为完整检查超时（连接 + 读取）时间，与所有 \<1.3.15 版本的行为完全一致。

在大多数情况下，检查请求的处理比普通请求更简单、更快，因此人们可能希望将性能滞后的服务器剔除，故该超时值应小于“timeout server”。

该参数仅适用于后端，但可在“defaults”段中统一指定一次。
实际上，这是避免遗漏的最简便解决方案之一。

另请参阅：“timeout connect”、“timeout queue”、“timeout server”、“timeout tarpit”。

<a id="entry-4-2-timeout-client"></a>

**`timeout client <timeout>`**

```haproxy
timeout client <timeout>
```

设置客户端的最大不活动时间。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

空闲超时适用于客户端预期确认或发送数据的场景。在 HTTP 模式下，该超时在以下两个阶段尤为重要：客户端发送请求的初始阶段，以及客户端读取服务器发送数据的响应阶段。尽管如此，在初始阶段，建议将“timeout http-request”设置为更小值，以更好地防范类似 Slowloris 的攻击。默认情况下，该值以毫秒为单位指定，但若在数值后附加单位，也可使用其他单位，具体单位说明请参见本文档顶部。在 TCP 模式（以及在一定程度上的 HTTP 模式）下，强烈建议客户端超时与服务器超时保持一致，以避免复杂且难以排查的情况。建议将超时值设置为略高于 3 秒的整数倍（例如 4 秒或 5 秒），以覆盖一个或多个 TCP 数据包丢失的情况。若存在长生命周期流与短生命周期流混合的情况（例如 WebSocket 与 HTTP 混用），建议考虑使用“timeout tunnel”，该设置将覆盖“timeout client”和“timeout server”对隧道的设定，同时也会覆盖“timeout client-fin”对半关闭连接的设定。

该参数仅适用于前端，但可在“defaults”段中统一指定一次。
这实际上是避免遗漏的最简单方法之一。未指定超时将导致无限超时，这不推荐使用。虽然这种用法被接受且可正常工作，但在启动时会报告警告，因为如果系统未配置超时，可能导致已过期会话在系统中累积。

另请参阅：“timeout server”、“timeout tunnel”、“timeout http-request”。

<a id="entry-4-2-timeout-client-fin"></a>

**`timeout client-fin <timeout>`**

```haproxy
timeout client-fin <timeout>
```

设置半关闭连接在客户端一侧的不活动超时。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

当客户端在某一方向连接已关闭的情况下仍需确认或发送数据时，将应用不活跃超时。该超时与“timeout client”不同，仅适用于单向关闭的连接。此设置特别有助于避免在客户端未正常断开时，连接长时间处于 FIN_WAIT 状态。此类问题在长连接（如 RDP 或 WebSocket）中尤为常见。请注意，当连接单向关闭时，该超时可覆盖“timeout tunnel”。在向 HTTP/2 连接发送 GOAWAY 帧后，该超时将应用于空闲连接，通常表明连接应快速结束。

此参数仅适用于前端，但可在“defaults”段中统一指定一次。
默认情况下未设置，因此半关闭连接将使用其他超时设置（timeout.client 或 timeout.tunnel）。

另请参阅：“timeout client”、“timeout server-fin” 和 “timeout tunnel”。

<a id="entry-4-2-timeout-client-hs"></a>

**`timeout client-hs <timeout>`**

```haproxy
timeout client-hs <timeout>
```

设置等待客户端 TLS 握手完成的最大时间。该设置对 TCP 和 QUIC 连接均适用。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

如果未设置此握手超时，则使用客户端超时作为替代。

<a id="entry-4-2-timeout-connect"></a>

**`timeout connect <timeout>`**

```haproxy
timeout connect <timeout>
```

设置连接尝试连接服务器时等待成功的最长时间。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

如果服务器与 HAProxy 位于同一局域网内，连接应立即建立（小于几毫秒）。无论如何，建议通过设置略高于 3 秒倍数的超时值（例如 4 秒或 5 秒），以覆盖一个或多个 TCP 数据包丢失的情况。默认情况下，若未指定，连接超时还会将队列超时和 tarpit 超时设置为相同值。

此参数仅适用于后端，但可在“defaults”段中统一指定一次。
实际上，这是避免遗漏的最简便方法之一。未指定超时将导致无限超时，这不推荐使用。虽然此类用法被接受且可正常工作，但在启动时会报告警告，因为若系统未配置超时，可能导致系统中积聚大量失败会话。

另请参阅：“timeout check”、“timeout queue”、“timeout server”、“timeout tarpit”。

<a id="entry-4-2-timeout-http-keep-alive"></a>

**`timeout http-keep-alive <timeout>`**

```haproxy
timeout http-keep-alive <timeout>
```

设置等待新 HTTP 请求出现的最大允许时间

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

默认情况下，持久连接在等待新请求时的超时时间由“timeout http-request”设置。然而，这并不总是方便的，因为部分用户希望设置非常短的持久连接超时时间以更快释放连接，而另一些用户则倾向于设置较长的超时时间，但一旦请求开始处理，仍希望保持较短的超时时间。

本文档中的“http-keep-alive”超时用于满足这些需求。该超时将定义在发送响应后，等待下一个 HTTP 请求开始的最长时间。一旦收到请求的第一个字节，将使用“http-request”超时来等待完整请求的到达。请注意，新请求前的空行不会重置超时，也不会被计为新的请求。

此外，两者之间还存在另一差异：当连接在 http-keep-alive 超时期间到期时，不会返回错误，连接仅被关闭。若连接在等待请求完成期间于 "http-request" 超时到期，则会在关闭连接前向客户端返回 HTTP 408 错误，除非前端中设置了 "option http-ignore-probes"。

在一般情况下，“timeout http-keep-alive” 用于防止客户端在访问大量短连接的网站时，长时间保持空闲连接。可通过在 HTTP/1.1 中将该值设置为几十至几百毫秒来实现。这样，在客户端请求页面后，连接将立即关闭，无需保持连接以等待客户端后续活动。在此场景下，浏览器的下一次活动将导致在 TCP 和/或 SSL 层进行新的握手。一个常见用例是仅向 HTTPS 页面重定向的 HTTP 站点。此类连接不应保持空闲过久，因为它们不会被重用，除非可能用于获取 favicon。

另一种用例恰恰相反：某些网站希望允许客户端长时间复用空闲连接（例如 30 秒至 1 分钟），但不希望为首个请求等待如此长时间，以避免成为一种极为廉价的攻击向量。此时，可将 http-keep-alive 超时设置为较大值，而 http-request 超时保持较低（几秒）。

当设置为极小值时，未启用流水线化的额外请求很可能通过另一条连接进行处理，除非请求确实实现了流水线化，而这一点在 HTTP/1.1 中极为罕见（即不等待响应即连续发送请求）。大多数 HTTP/1.1 实现均采用发送请求、等待响应后再发送下一个请求的方式。对于拥有数十万客户端的站点，此处对 HTTP/1.1 使用较小值可节省内存和套接字资源，但会增加握手计算开销。

处理 HTTP/2 时，对小数值需格外注意。HTTP/2 的特性是将多个请求复用到单一连接上，以减少重新建立 TCP 和/或 SSL 层的开销。该协议还使用控制帧，对早期关闭 TCP 连接的处理效果较差。极少数情况下，这可能导致数据在离开 HAProxy 后于传输途中被截断（此时 HAProxy 甚至无法记录错误）。建议为 HTTP/2 连接设置的最低起始值约为 4 秒。该值可防止大多数现代持久连接实现无谓地保持已失效的连接，同时仍允许后续请求复用连接。然而，应根据实际需求进行调整，此值仅作为参考起点。

如果未设置此参数，则使用“http-request”超时；若两者均未设置，则“timeout client”仍会在较低层级生效。该参数应在前端设置以生效，除非前端处于 TCP 模式，此时将使用 HTTP 后端的超时设置。

另请参阅：“timeout http-request”，“timeout client”。

<a id="entry-4-2-timeout-http-request"></a>

**`timeout http-request <timeout>`**

```haproxy
timeout http-request <timeout>
```

设置等待完整 HTTP 请求的最大允许时间

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

为提供拒绝服务（DoS）防护，可能需要降低接收完整 HTTP 请求的最大允许时间，而不会影响客户端超时设置。此举有助于防范已建立但无任何数据发送的连接。客户端超时无法有效防护此类滥用，因其为非活动超时机制，即攻击者若偶尔发送一个字符，超时将不会触发。而通过 HTTP 请求超时机制，无论客户端输入速度如何，只要请求未能在规定时间内完成，即会被中止。超时触发后，将向客户端发送 HTTP 408 响应以告知问题，并关闭连接。日志中将记录终止码 "cR"。部分较新浏览器对这一标准且有明确文档记录的行为存在兼容性问题，因此可能需要通过 "option http-ignore-probes" 或 "errorfile 408 /dev/null" 隐藏 408 状态码。更多详情请参见 [第 8.5 节](/zh/haproxy/configuration-logging/#section-8-5) 中对 "cR" 终止码的说明。

默认情况下，此超时仅适用于请求头部分，而不适用于任何数据。一旦接收到空行，该超时将不再生效。当与“option http-buffer-request”结合使用时，此超时也适用于请求体。在持久连接中，若未设置“timeout http-keep-alive”，该超时将在等待第二个请求时再次使用。

通常将该值设置为几秒即可，因为大多数客户端在建立连接后会立即发送完整请求。增加 3 秒或更多以覆盖 TCP 重传情况，仅此而已。在本地网络且无丢包的情况下，设置为极低值（例如 50 ms）通常可行。此举可防止用户通过 telnet 发送未经封装的 HTTP 请求。

如果未设置此参数，客户端超时仍会在接收请求的每个数据块之间生效。该参数应在前端设置以生效，除非前端处于 TCP 模式，此时将使用 HTTP 后端的超时设置。

另请参阅：“errorfile”、“http-ignore-probes”、“timeout http-keep-alive”和“timeout client”，以及“option http-buffer-request”。

<a id="entry-4-2-timeout-queue"></a>

**`timeout queue <timeout>`**

```haproxy
timeout queue <timeout>
```

设置连接槽位空闲前在队列中等待的最大时间

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

当服务器的 maxconn 限制达到时，连接将被置于队列中，该队列可以是服务器特定的，也可以是后端全局的。为避免无限期等待，对队列中等待的请求应用了超时机制。如果超时时间到达，认为该请求几乎不可能被处理，因此将被丢弃，并向客户端返回 503 错误。

“timeout queue” 语句用于设置请求在队列中等待的最大时间。若未指定，则使用后端连接超时（“timeout connect”）的值，以保持与旧版本的向后兼容性（旧版本不支持“timeout queue”参数）。

另请参阅：timeout connect。

<a id="entry-4-2-timeout-server"></a>

**`timeout server <timeout>`**

```haproxy
timeout server <timeout>
```

设置服务器端的最大不活动时间。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

空闲超时适用于服务器预期确认或发送数据的场景。在 HTTP 模式下，该超时在服务器响应的第一阶段尤为重要，即服务器必须发送头信息时，因为该值直接反映了服务器处理请求的耗时。为确定合适的取值，通常建议从可接受的最差响应时间开始，随后检查日志以观察响应时间分布情况，并据此调整该值。

默认情况下，该值以毫秒为单位指定，但若在数字后附加单位，也可使用其他单位，具体单位定义见本文档顶部。在 TCP 模式下（在 HTTP 模式下程度稍低），强烈建议客户端超时与服务器超时保持一致，以避免复杂情况带来的调试困难。无论预期的服务器响应时间如何，建议将超时时间设置为略高于 3 秒的倍数（例如最小 4 或 5 秒），以覆盖至少一次或多次 TCP 数据包丢失。若存在长生命周期流与短生命周期流混合的情况（例如 WebSocket 与 HTTP 混合），建议考虑使用“timeout tunnel”，该配置将覆盖“timeout client”和“timeout server”对隧道的设置。

此参数仅适用于后端，但可在“defaults”段中统一指定一次。
这实际上是一种避免遗漏的最简便解决方案。未指定超时将导致无限超时，这不被推荐。虽然此类用法被接受且可正常工作，但在启动时会报告警告，因为如果系统未配置超时，可能导致过期会话在系统中累积。

另请参阅：“timeout client” 和 “timeout tunnel”。

<a id="entry-4-2-timeout-server-fin"></a>

**`timeout server-fin <timeout>`**

```haproxy
timeout server-fin <timeout>
```

设置服务器端半关闭连接的不活动超时时间。

可用于以下上下文：tcp、http、log

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

当服务器在某一方向已关闭的情况下仍需确认或发送数据时，将应用不活动超时。此超时与“timeout server”不同，仅适用于单向关闭的连接。该设置特别有助于避免在远程服务器未正常断开时，使连接在 FIN_WAIT 状态下维持过长时间。此类问题在长连接（如 RDP 或 WebSocket）中尤为常见。请注意，当连接在某一方向关闭时，此超时可覆盖“timeout tunnel”。该设置仅出于完整性考虑提供，在大多数情况下无需使用。

此参数仅适用于后端，但可在“defaults”段中统一指定一次。默认情况下未设置，因此半关闭连接将使用其他超时设置（timeout.server 或 timeout.tunnel）。

另请参阅：“timeout client-fin”、“timeout server”和“timeout tunnel”。

<a id="entry-4-2-timeout-tarpit"></a>

**`timeout tarpit <timeout>`**

```haproxy
timeout tarpit <timeout>
```

设置被限制的连接将维持的时长

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<timeout> 是连接陷阱（tarpit）的持续时间，默认单位为毫秒；也可在数值后添加单位后缀，
          使用其他单位，详见本文开头的说明。
```

当使用 "http-request tarpit" 时，连接将保持打开状态且无任何活动，持续一段时间后关闭。"timeout tarpit" 定义了连接保持打开的时长。

默认情况下，该值以毫秒为单位指定，但若在数字后附加单位，则可使用任意其他单位，具体单位定义见本文档顶部。若未指定，则使用与后端连接超时（"timeout connect"）相同的值，以保持与旧版本的向后兼容性（旧版本无 "timeout tarpit" 参数）。

另请参阅：timeout connect。

<a id="entry-4-2-timeout-tunnel"></a>

**`timeout tunnel <timeout>`**

```haproxy
timeout tunnel <timeout>
```

设置隧道在客户端和服务器端的最大不活动时间。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

隧道超时适用于客户端与服务器之间建立双向连接，且连接在两个方向上均处于空闲状态的情况。一旦连接成为隧道，该超时将覆盖客户端和服务器的超时设置。在 TCP 中，当任一连接上不再有分析器附加时（例如，已接受 TCP 内容规则），即开始使用此超时。在 HTTP 中，当连接被升级时（例如，切换至 WebSocket 协议，或将 CONNECT 请求转发至代理），或在首次响应后未指定 keepalive/close 选项时，即开始使用此超时。

由于此超时通常与长连接配合使用，因此建议同时设置 "timeout client-fin"，以处理客户端突然从网络中断且未确认关闭，或发送关闭请求后不再确认待处理数据的情况。这种情况可能出现在存在防火墙的丢包网络中，可通过 FIN_WAIT 状态下会话数量大幅增加来检测。

默认情况下，该值以毫秒为单位指定，但若在数字后附加单位，也可使用其他单位，具体单位定义见本文档顶部。无论预期的正常空闲时间为何，建议将超时设置为略高于 3 秒的倍数（例如最小值为 4 秒或 5 秒），以覆盖至少一次或多次 TCP 数据包丢失的情况。

该参数仅适用于后端，但可在“defaults”段中统一指定一次。
实际上，这是避免遗漏的最简便解决方案之一。

示例：

```text
defaults http
    option http-server-close
    timeout connect 5s
    timeout client 30s
    timeout client-fin 30s
    timeout server 30s
    timeout tunnel  1h    # timeout to use with WebSocket and CONNECT
```

另请参阅：“timeout client”、“timeout client-fin”、“timeout server”。

<a id="entry-4-2-transparent"></a>

**`transparent (deprecated)`**

```haproxy
transparent (deprecated)
```

启用客户端透明代理

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| no \| yes \| yes

参数：无

该关键字的引入旨在为第 3 层负载均衡器提供第 7 层持久性。其原理是利用操作系统将来自远程地址的入站连接重定向至本地进程（此处为 HAProxy），并让该进程知晓最初请求的地址。启用此选项后，未携带 Cookie 的会话将被转发至入站请求的原始目标 IP 地址（该地址应与另一台设备的地址匹配），而携带 Cookie 的请求仍会被转发至相应的服务器。

"transparent" 关键字已弃用，请改用 "option transparent"。

请注意，与普遍认知相反，此选项并不会在建立连接时向服务器呈现客户端的 IP 地址。

另请参阅："option transparent"

<a id="entry-4-2-unique-id-format"></a>

**`unique-id-format <fmt>`**

```haproxy
unique-id-format <fmt>
```

为每个请求生成唯一的 ID。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| yes

参数：

```text
<fmt>   是自定义日志格式字符串（参见第 8.2.6 节）。
```

此关键字使用自定义日志格式为每个请求创建 ID。唯一 ID 有助于追踪请求在复杂基础设施多个组件间的流转过程。新创建的 ID 也可通过自定义日志格式字符串中的 %ID 别名进行记录。

格式应由组合后保证唯一的元素构成。
例如，若涉及多个 HAProxy 实例，可能需要包含节点名称。
通常需要记录入站连接的源地址和目标地址及端口。
请注意，由于多个请求可能通过同一连接执行，包含请求计数器有助于区分它们。
类似地，添加时间戳可防止计数器溢出。
记录进程 ID 可避免服务重启后发生冲突。

建议对多个字段使用十六进制表示法，因其可使字段更紧凑，并在日志中节省空间。

对于常规连接，使用前端中配置的格式生成唯一 ID。对于健康检查，当在 tcp-check 或 http-check 规则集中使用 "unique-id" 获取字段时，采用后端的格式。

示例：

```text
unique-id-format %{+X}o\ %ci:%cp_%fi:%fp_%Ts_%rt:%pid

将生成：

       7F000001:8296_7F00001E:1F90_4F7B0A69_0003:790A
```

另请参阅："unique-id-header"

<a id="entry-4-2-unique-id-header"></a>

**`unique-id-header <name>`**

```haproxy
unique-id-header <name>
```

在 HTTP 请求中添加唯一 ID 头。

可用于以下上下文：http

可出现在以下段中：defaults \| frontend \| listen \| backend yes \| yes \| yes \| no

参数：

```text
<name>   是头名称。
```

在发送至服务器的 HTTP 请求中添加一个 unique-id 头，使用 unique-id-format 格式。若 unique-id-format 不存在，则无法生效。

示例：

```text
    unique-id-format %{+X}o\ %ci:%cp_%fi:%fp_%Ts_%rt:%pid
    unique-id-header X-Unique-ID

    将生成：

       X-Unique-ID: 7F000001:8296_7F00001E:1F90_4F7B0A69_0003:790A

另请参阅： "unique-id-format"
```

<a id="entry-4-2-use-backend"></a>

**`use_backend <backend> [{if | unless} <condition>]`**

```haproxy
use_backend <backend> [{if | unless} <condition>]
```

若 ACL 条件匹配，则切换至指定后端；否则不切换。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| yes \| yes \| no

参数：

```text
<backend>   是有效后端或 "listen" 段的名称，或求值为后端名称的自定义日志格式
            （参见第 8.2.6 节的自定义日志格式）。

<condition> 是第 7 节所述的由 ACL 组成的条件。省略时，无条件应用该规则。
```

在执行内容切换时，连接会先到达前端，然后根据若干条件被分发至不同的后端。条件与后端之间的关联通过 "use_backend" 关键字描述。尽管该关键字通常用于 HTTP 处理，也可用于纯 TCP 场景，既可不依赖内容而使用无状态 ACL（例如源地址验证），也可与 "tcp-request" 规则结合，以等待部分有效载荷。

可以定义任意数量的 "use_backend" 规则。所有规则按声明顺序逐一评估，首个匹配的规则将指定后端。即使该后端被视为不可用，此规则依然生效。然而，若匹配的规则指向一个已禁用或未发布的后端，则该规则将被忽略，规则评估继续进行。

在第一种形式中，若满足条件，则使用该后端。在第二种形式中，若条件不满足，则使用该后端。若无有效条件，将使用以 "default_backend" 定义的默认后端，除非该后端已被禁用或未发布。若无可用地默认后端，则在“listen”段中使用同一段内的服务器，或在前端中不使用任何服务器，并返回 503 服务不可用响应。

请注意，可以从 TCP 前端切换至 HTTP 后端。在此情况下，要么前端已确认协议为 HTTP，后端处理将立即开始，要么后端将等待完整的 HTTP 请求到达。当前端必须在单一端口上解码多种协议（其中一种为 HTTP）时，此功能非常有用。

当 `<backend>` 为简单名称时，将在配置时解析，若指定的后端不存在，则报告错误。若 `<backend>` 为自定义日志格式，则配置时可能无法进行检查，因此后端名称将在运行时动态解析。若解析出的后端名称不对应任何有效后端，则不再评估其他规则，而是应用 default_backend 指令。请注意，使用动态后端名称时，强烈建议使用其他后端均不使用的前缀，以确保无法通过请求强制指定未经授权的后端。

值得注意的是，带有显式名称的 "use_backend" 规则用于检测前端与后端之间的关联，以计算后端的 "fullconn" 设置。动态名称无法执行此操作。

另请参阅："default_backend"、"tcp-request"、"fullconn"、"log-format" 以及关于 ACL 的 [第 7 节](/zh/haproxy/acls-and-samples/)。

<a id="entry-4-2-use-fcgi-app"></a>

**`use-fcgi-app <name>`**

```haproxy
use-fcgi-app <name>
```

定义后端所使用的 FastCGI 应用。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

参数：

```text
<name>    是要使用的 FastCGI 应用程序的名称。
```

有关 FastCGI 应用设置的详细信息，请参见 [第 10.1 节](/zh/haproxy/fastcgi/#section-10-1)。

<a id="entry-4-2-use-server"></a>

**`use-server <server> if <condition>`**

```haproxy
use-server <server> if <condition>
use-server <server> unless <condition>
```

仅在匹配基于 ACL 的条件时，才使用特定服务器。

可用于以下上下文：tcp、http

可出现在以下段中：defaults \| frontend \| listen \| backend no \| no \| yes \| yes

参数：

```text
<server>    是同一后端段内有效服务器的名称，或求值为服务器名称的自定义日志格式字符串
            （参见第 8.2.6 节）。

<condition> 是第 7 节所述的由 ACL 组成的条件。
```

默认情况下，到达后端的连接会根据配置的算法，在可用服务器之间进行负载均衡，除非请求中包含如 cookie 等持久性机制并被识别到。

有时需要将特定请求转发至某个特定服务器，而无需为该服务器声明专用的后端。这可以通过使用“use-server”规则实现。这些规则在“redirect”规则之后、评估 Cookie 之前进行处理，并优先于 Cookie 评估。可以定义任意数量的“use-server”规则。所有规则按声明顺序逐一评估，首个匹配的规则将指定目标服务器。

如果某条规则指定的服务器处于离线状态，且未使用“option persist”选项，也未验证任何“force-persist”规则，则该规则将被忽略，评估将继续执行后续规则，直至匹配到一条为止。

在第一种形式中，若满足条件，则使用该服务器。在第二种形式中，若条件不满足，则使用该服务器。若无任何条件有效，处理将继续，并根据其他持久性机制分配服务器。

请注意，即使匹配了某条规则，仍会执行 cookie 处理，但不会分配服务器。这使得带前缀的 cookie 可以去除其前缀。

"use-server" 语句在 HTTP 和 TCP 模式下均有效。这使其适用于基于内容的检测。例如，在使用具有隐式 TLS 的协议时，可根据 TLS SNI 字段在服务器池中选择服务器（另见 "req.ssl_sni"）。若这些服务器的权重设置为零，则它们将不会用于其他流量。

示例：

```shell
# intercept incoming TLS requests based on the SNI field
use-server www if { req.ssl_sni -i www.example.com }
server     www 192.168.0.1:443 weight 0
use-server mail if { req.ssl_sni -i mail.example.com }
server     mail 192.168.0.1:465 weight 0
use-server imap if { req.ssl_sni -i imap.example.com }
server     imap 192.168.0.1:993 weight 0
# all the rest is forwarded to this server
server  default 192.168.0.2:443 check
```

当 `<server>` 为简单名称时，会检查其是否存在于配置中的现有服务器列表中，若指定的服务器不存在，则报告错误。若为自定义日志格式，则在解析配置时不会执行检查；若运行时无法解析出有效的服务器名称，但 use-server 规则受 ACL 条件控制且返回 true，则不再应用其他 use-server 规则，并回退至负载均衡。

另请参阅："use_backend"、[第 5 节](/zh/haproxy/bind-and-server-options/) 中关于服务器的内容，以及[第 7 节](/zh/haproxy/acls-and-samples/) 中关于 ACL 的内容。

## 4.3. 动作关键字矩阵 {#section-4-3}

在请求或响应处理的各个阶段，会评估多个规则集，对于这些规则集中发现的每条规则，若满足可选条件，则可执行相应动作。

默认提供了大量动作，可用于修改内容、接受或阻断处理、更改内部状态等。也可在 Lua 中定义新动作（此时其名称将始终以 "lua." 为前缀）。

尽管历史上某些动作仅限于特定规则集使用，但如今许多动作可在多种规则集中使用。本节列出的内容将标明每种受支持的动作可在哪些规则集中使用，方法是勾选以下规则集对应的简写条目名称：

- QUIC Ini：该动作适用于“quic-initial”规则
- TCP RqCon：该动作适用于“tcp-request connection”规则
- TCP RqSes：该动作适用于“tcp-request session”规则
- TCP RqCnt：该动作适用于“tcp-request content”规则
- TCP RsCnt：该动作适用于“tcp-response content”规则
- HTTP Req：该动作适用于“http-request”规则
- HTTP Res：该动作适用于“http-response”规则
- HTTP Aft：该动作适用于“http-after-response”规则

相同的缩写在下文 [第 4.4 节](/zh/haproxy/proxies/#section-4-4) 的参考部分中同样使用。

```text
 关键字                QUIC: Ini   TCP: RqCon RqSes RqCnt RsCnt   HTTP: Req Res Aft
----------------------+-----------+-----------+-----+-----+------+----------+---+----
accept                         X           X     X     X     X            -   -   -
add-acl                        -           -     -     -     -            X   X   -
add-header                     -           -     -     -     -            X   X   X
add-headers-bin                -           -     -     -     -            X   X   X
allow                          -           -     -     -     -            X   X   X
attach-srv                     -           -     X     -     -            -   -   -
auth                           -           -     -     -     -            X   -   -
cache-store                    -           -     -     -     -            -   X   -
cache-use                      -           -     -     -     -            X   -   -
capture                        -           -     -     X     -            X   X   X
close                          -           -     -     -     X            -   -   -
del-acl                        -           -     -     -     -            X   X   -
del-header                     -           -     -     -     -            X   X   X
del-headers-bin                -           -     -     -     -            X   X   X
del-map                        -           -     -     -     -            X   X   X
deny                           -           -     -     -     -            X   X   -
dgram-drop                     X           -     -     -     -            -   -   -
disable-l7-retry               -           -     -     -     -            X   -   -
do-log                         X           X     X     X     X            X   X   X
do-resolve                     -           -     -     X     -            X   -   -
early-hint                     -           -     -     -     -            X   -   -
expect-netscaler-cip           -           X     -     -     -            -   -   -
expect-proxy layer4            -           X     -     -     -            -   -   -
normalize-uri                  -           -     -     -     -            X   -   -
pause                          -           -     -     -     -            X   X   -
redirect                       -           -     -     -     -            X   X   -
reject                         X           X     X     X     X            X   -   -
replace-header                 -           -     -     -     -            X   X   X
replace-path                   -           -     -     -     -            X   -   -
replace-pathq                  -           -     -     -     -            X   -   -
replace-uri                    -           -     -     -     -            X   -   -
replace-value                  -           -     -     -     -            X   X   X
return                         -           -     -     -     -            X   X   -
sc-add-gpc                     -           X     X     X     X            X   X   X
--keyword---------------QUIC--Ini---TCP--RqCon-RqSes-RqCnt-RsCnt---HTTP--Req-Res-Aft-sc-inc-gpc                     -           X     X     X     X            X   X   X
sc-inc-gpc0                    -           X     X     X     X            X   X   X
sc-inc-gpc1                    -           X     X     X     X            X   X   X
sc-set-gpt                     -           X     X     X     X            X   X   X
sc-set-gpt0                    -           X     X     X     X            X   X   X
send-retry                     X           -     -     -     -            -   -   -
send-spoe-group                -           -     -     X     X            X   X   -
set-bandwidth-limit            -           -     -     X     X            X   X   -
set-bc-mark                    -           -     -     X     -            X   -   -
set-bc-tos                     -           -     -     X     -            X   -   -
set-dst                        -           X     X     X     -            X   -   -
set-dst-port                   -           X     X     X     -            X   -   -
set-fc-mark                    -           X     X     X     X            X   X   -
set-fc-tos                     -           X     X     X     X            X   X   -
set-header                     -           -     -     -     -            X   X   X
set-headers-bin                -           -     -     -     -            X   X   X
set-log-level                  -           -     -     X     X            X   X   X
set-map                        -           -     -     -     -            X   X   X
set-mark (deprecated)          -           X     X     X     X            X   X   -
set-method                     -           -     -     -     -            X   -   -
set-nice                       -           -     -     X     X            X   X   -
set-path                       -           -     -     -     -            X   -   -
set-pathq                      -           -     -     -     -            X   -   -
set-priority-class             -           -     -     X     -            X   -   -
set-priority-offset            -           -     -     X     -            X   -   -
--keyword---------------QUIC--Ini---TCP--RqCon-RqSes-RqCnt-RsCnt---HTTP--Req-Res-Aft-set-query                      -           -     -     -     -            X   -   -
set-retries                    -           -     -     X     -            X   -   -
set-src                        -           X     X     X     -            X   -   -
set-src-port                   -           X     X     X     -            X   -   -
set-status                     -           -     -     -     -            -   X   X
set-timeout                    -           -     -     -     -            X   X   -
set-tos (deprecated)           -           X     X     X     X            X   X   -
set-uri                        -           -     -     -     -            X   -   -
set-var                        -           X     X     X     X            X   X   X
set-var-fmt                    -           X     X     X     X            X   X   X
silent-drop                    -           X     X     X     X            X   X   -
strict-mode                    -           -     -     -     -            X   X   X
switch-mode                    -           -     -     X     -            -   -   -
tarpit                         -           -     -     -     -            X   -   -
track-sc0                      -           X     X     X     -            X   X   -
track-sc1                      -           X     X     X     -            X   X   -
track-sc2                      -           X     X     X     -            X   X   -
unset-var                      -           X     X     X     X            X   X   X
use-service                    -           -     -     X     -            X   -   -
wait-for-body                  -           -     -     -     -            X   X   -
wait-for-handshake             -           -     -     -     -            X   -   -
--keyword---------------QUIC--Ini---TCP--RqCon-RqSes-RqCnt-RsCnt---HTTP--Req-Res-Aft-
```

## 4.4. 按字母顺序排序的动作参考 {#section-4-4}

本节详细描述了每个动作及其用法，采用与上文 [第 4.3 节](/zh/haproxy/proxies/#section-4-3) 所述规则集术语标记一致的规范。

<a id="entry-4-4-accept"></a>

**`accept`**

```haproxy
accept
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| X \| X \| X \| X
\| - \| - \| -

此动作停止规则的评估，并允许请求或响应通过检查。该动作为最终动作，即当前段中不再评估同一规则集中的其他规则。此动作与“allow”动作的区别仅在于历史兼容性：在 TCP 和 QUIC 规则中使用“accept”，在 HTTP 规则中使用“allow”。参见下方“allow”动作。

<a id="entry-4-4-add-acl"></a>

**`add-acl(<file-name>) <key fmt>`**

```haproxy
add-acl(<file-name>) <key fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

用于向 ACL 添加新条目。ACL 必须从文件加载（即使是一个空的占位文件）。要更新的 ACL 文件名需置于括号内传递。该指令接受一个参数：`<key fmt>`，其格式需遵循 [第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6) 中描述的自定义日志格式规则，用于收集新条目的内容。插入前会执行 ACL 查找，以避免重复（或更多）值。其功能等同于统计套接字中的“add acl”命令，但可通过 HTTP 请求触发。

<a id="entry-4-4-add-header"></a>

**`add-header <name> <fmt>`**

```haproxy
add-header <name> <fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

在指定的 `<name>` 头字段名后追加一个 HTTP 头，其值由 `<fmt>` 定义，遵循自定义日志格式规则（参见 [第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6)）。该规则特别适用于向服务器传递与连接相关的特定信息（例如客户端的 SSL 证书），或合并多个头为一个。该规则非最终规则，因此可以添加其他类似规则。请注意，头添加操作会立即执行，因此一条规则可重用前一条规则生成的头。

<a id="entry-4-4-add-headers-bin"></a>

**`add-headers-bin <expr> [ prefix <str> ]`**

```haproxy
add-headers-bin <expr> [ prefix <str> ]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

这是“add-header”动作的一种变体，其中头名称和值以 varint 编码的二进制字符串形式传递。有关 varint 格式的详情，请参阅 "req.hdrs_bin" 样本提取。当需要一次性设置多个头而无需预先知晓头名称时，此方法非常有用。请注意，这些头未经过 HTTP 解析器验证，可能导致发出无效消息，最严重情况下可能引发请求走私攻击。插入头的数量同样重要，因为其受 tune.http.maxhdr 限制。可选前缀仅对编码字符串中以 `<str>` 开头的头进行设置。

示例：

```shell
# This would reset the Accept/UA/Host headers to their initial values
http-request set-var(txn.oldheaders) req.hdrs_bin
http-request del-header Accept
http-request del-header User-Agent
http-request del-header Host
http-request add-headers-bin var(txn.oldheaders)

```

<a id="entry-4-4-allow"></a>

**`allow`**

```haproxy
allow
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

此动作停止规则的评估，并允许请求通过检查。该动作为最终动作，即当前段中不再评估同一规则集中的其他规则。此动作与“accept”动作的区别仅在于历史兼容性：TCP 规则使用“accept”，HTTP 规则使用“allow”。参见上方的“accept”动作。

<a id="entry-4-4-attach-srv"></a>

**`attach-srv <srv> [name <expr>] [ EXPERIMENTAL ]`**

```haproxy
attach-srv <srv> [name <expr>] [ EXPERIMENTAL ]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| X \| - \| -
\| - \| - \| -

在正确建立 HTTP/2 连接后，用于拦截连接。连接将被反转至后端侧，并插入到服务器 `<srv>` 的空闲连接池中。此功能仅可与地址为 'rhttp@' 的服务器配合使用。

连接将根据 `<expr>` 求值结果定义的名称插入到服务器空闲连接池中。该名称将用于匹配受 "pool-conn-name" 或 "sni" 参数约束的请求。详情请参见 "http-reuse"。

反向 HTTP 当前仍处于积极开发阶段。配置机制未来可能发生变化。因此，该功能在内部被标记为实验性，这意味着必须在本指令之前单独一行出现 "expose-experimental-directives" 指令。

请注意，一种非常相似但独立的协议正在开发中。详见 <https://www.ietf.org/archive/id/draft-bt-httpbis-reverse-http-00.html>。

<a id="entry-4-4-auth"></a>

**`auth [realm <realm>]`**

```haproxy
auth [realm <realm>]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

停止规则的评估，并立即返回 HTTP 401 或 407 错误码，以提示用户提交有效的用户名和密码。后续的“http-request”规则不再评估。支持可选的“realm”参数，用于设置随响应返回的认证域（通常为应用程序名称）。

使用对应代理的错误消息。可通过“errorfile”或“http-error”指令进行自定义。对于 401 响应，所有 WWW-Authenticate 头均被移除，并替换为一个全新的头，其中包含针对领域 "`<realm>`" 的基本认证挑战。对于 407 响应，同样操作适用于 Proxy-Authenticate 头。若错误消息不得更改，请考虑使用“http-request return”规则替代。

示例：

```text
acl auth_ok http_auth_group(L1) G1
http-request auth unless auth_ok

```

<a id="entry-4-4-cache-store"></a>

**`cache-store <name>`**

```haproxy
cache-store <name>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| - \| X \| -

将 HTTP 响应存储至缓存。响应头的存储在此步骤完成，这意味着可在响应存储前或后使用其他 http-response 动作来修改头。此动作负责缓存存储过滤器的设置。

请参阅 [第 6.2 节](/zh/haproxy/cache/#section-6-2) 了解缓存设置。

<a id="entry-4-4-cache-use"></a>

**`cache-use <name>`**

```haproxy
cache-use <name>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

尝试从缓存 `<name>` 中提供缓存对象。该指令也是存储缓存所必需的，因为它会计算缓存哈希值。若希望对存储和提供均使用相同条件，建议将该条件置于本指令之后。

请参阅 [第 6.2 节](/zh/haproxy/cache/#section-6-2) 了解缓存设置。

<a id="entry-4-4-capture"></a>

**`capture <sample> [ len <length> | id <id> ]`**

```haproxy
capture <sample> [ len <length> | id <id> ]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| X \| X

此规则从请求或响应缓冲区中捕获样本表达式 `<sample>`，并将其转换为最多 `<len>` 个字符的字符串。结果字符串将存储到下一个“捕获”槽位（请求或响应）中，因此可能与某些捕获的 HTTP 头并列出现。随后该字符串将自动出现在日志中，并可通过样本提取方法提取，用于填充头或其他用途。由于该长度将在整个流生命周期内为每次捕获分配内存，因此必须加以限制。请注意，该长度仅适用于 "http-request" 规则。此类槽位仅存在于声明它的段中，因此，若该规则位于同时作为另一前端的后端使用的 "listen" 段内，则该规则不会作用于来自该前端的流。请参阅 [第 7.3 节](/zh/haproxy/acls-and-samples/#section-7-3)（样本提取）、"capture request header" 和 "capture response header" 以获取更多信息。

如果使用关键字 "id" 代替 "len"，该动作会尝试将捕获的字符串存储到先前声明的捕获槽中。这在后端中运行捕获时非常有用。捕获槽 ID 可通过先前的指令 "http-request capture" 或使用 "declare capture" 关键字声明。

在后端中使用此动作时，请务必确认相关前端已具备所需的捕获槽位，否则该规则在运行时将被忽略。由于 HAProxy 具备在运行时动态解析后端名称的能力，此问题无法在配置解析阶段被检测到。

<a id="entry-4-4-close"></a>

**`close`**

```haproxy
close
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| X
\| - \| - \| -

此动作用于立即关闭与服务器的连接。后续不会再评估任何“tcp-response content”规则。该动作的主要用途是在应用协议预期需先经历较长时间超时后，强制完成客户端与服务器之间的连接交换。其目标是消除某些协议下占用大量服务器资源的空闲连接。

<a id="entry-4-4-del-acl"></a>

**`del-acl(<file-name>) <key fmt>`**

```haproxy
del-acl(<file-name>) <key fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

用于从 ACL 中删除条目。ACL 必须从文件加载（即使是一个空的虚拟文件）。要更新的 ACL 文件名需置于括号内传递。该指令接受一个参数：`<key fmt>`，其遵循 [第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6) 中定义的自定义日志格式规则，用于收集待删除条目的内容。此操作等效于通过统计套接字执行的 "del acl" 命令，但可通过 HTTP 请求或响应触发。

<a id="entry-4-4-del-header"></a>

**`del-header <name> [ -m <meth> ]`**

```haproxy
del-header <name> [ -m <meth> ]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

此操作会移除 HTTP 头字段名在 `<name>` 中指定的所有字段。`<meth>` 为匹配方法，应用于头名称。支持的匹配方法包括 "str"（精确匹配）、"beg"（前缀匹配）、"end"（后缀匹配）、"sub"（子串匹配）和 "reg"（正则匹配）。若未指定，则使用精确匹配方法。

<a id="entry-4-4-del-headers-bin"></a>

**`del-headers-bin <expr> [ -m <meth> ]`**

```haproxy
del-headers-bin <expr> [ -m <meth> ]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

此操作会移除所有名称在 `<expr>` 中指定的 HTTP 头。`<expr>` 必须返回一个以 varint 编码的二进制字符串，其中包含所有应被删除的头名称。编码方式及示例请参见 "add-headers-bin" 和 "set-headers-bin"。`<meth>` 为匹配方法，应用于所有头名称。支持的匹配方法包括 "str"（精确匹配）、"beg"（前缀匹配）、"end"（后缀匹配）和 "sub"（子串匹配）。由于运行时性能不可预测，不支持 "reg"（正则表达式匹配）。若未指定，默认使用精确匹配方法。

<a id="entry-4-4-del-map"></a>

**`del-map(<map-name>) <key fmt>`**

```haproxy
del-map(<map-name>) <key fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

用于从映射中删除条目。`<map-name>` 必须遵循 2.7 节所述的格式，关于映射和 ACL 的名称格式。要更新的映射名称需置于括号内。该指令接受一个参数：`<key fmt>`，其格式需符合[第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6)中自定义日志格式规则，用于收集待删除条目的内容。该指令接受一个参数：“文件名”。其功能等同于统计套接字中的“del map”命令，但可通过 HTTP 请求或响应触发。

<a id="entry-4-4-deny"></a>

**`deny [ { status | deny_status } <code> ] [ content-type <type> ]`**

```haproxy
deny [ { status | deny_status } <code> ] [ content-type <type> ]
     [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

       file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
     [ hdr `<name>` `<fmt>` ]*

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

此动作停止规则的评估，并立即拒绝请求或响应。默认情况下，对请求返回 HTTP 403 错误，对响应返回 502 错误，但可通过与“return”动作相同的语法自定义返回的响应。具体细节请参见下方“return”动作说明。为保持兼容性，当未定义参数，或仅定义 "deny_status" 时，隐含参数为 “default-errorfiles”。这意味着 “deny [deny_status `<status>`]” 是 “deny [status `<status>`] default-errorfiles” 的别名。该动作为最终动作，即当前段中同一规则集的后续规则不再被评估。有关高级语法，请参见“return”动作。

<a id="entry-4-4-dgram-drop"></a>

**`dgram-drop`**

```haproxy
dgram-drop
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| - \| - \| - \| -
\| - \| - \| -

此操作会静默忽略 QUIC 初始数据包的接收，否则该数据包将导致新的 QUIC 连接实例化及其 SSL 握手执行。

<a id="entry-4-4-disable-l7-retry"></a>

**`disable-l7-retry`**

```haproxy
disable-l7-retry
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

若请求因非连接失败以外的任何原因而失败，将禁用重试尝试。例如，这可用于确保 POST 请求在失败时不会被重试。

<a id="entry-4-4-do-log"></a>

**`do-log [profile <log_profile>]`**

```haproxy
do-log [profile <log_profile>]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| X \| X \| X \| X
\| X \| X \| X

此动作手动触发代理的日志输出。这意味着将考虑代理上的日志选项（包括“log-format”等格式化选项），但不会干扰代理在事务处理过程中自动产生的日志。

使用 "log-profile" 可以精确描述在每个可用上下文中执行该动作时日志的输出方式。即，在 "on" 关键字后跟随以下值之一：'quic-init'、'tcp-req-conn'、'tcp-req-sess'、'tcp-req-cont'、'tcp-res-cont'、'http-req'、'http-res'、'http-after-res'。

此外，使用 "%OG" 日志格式别名时，它们将被正确报告。

可选的 "profile" 参数可用于指定日志配置文件段名称，以替代默认应用于当前日志记录器的配置文件段，从而专门为此 do-log 动作指定日志配置文件。

示例：

```text
log-profile my-dft-prof
  on tcp-req-conn format "Connect: %ci"

log-profile my-local-prof
  on tcp-req-conn format "Local Connect: %ci"

frontend myfront
  log stdout format rfc5424 profile my-dft-prof local0
  log-format "log generated using proxy logformat, from '%OG'"
  acl local src 127.0.0.1
  # on connection use either log-profile from the logger (my-dft-prof) or
  # explicit my-local-prof if source ip is localhost
  tcp-request connection do-log if !local
  tcp-request connection do-log profile my-local-prof if local
  # on content use proxy logformat, since no override was specified
  # in my-dft-prof
  tcp-request content do-log
```

<a id="entry-4-4-do-resolve"></a>

**`do-resolve(<var>,<resolvers>[,ipv4|ipv6]) <expr>`**

```haproxy
do-resolve(<var>,<resolvers>[,ipv4|ipv6]) <expr>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

该动作对 `<expr>` 的输出结果执行 DNS 解析，并将结果存储至变量 `<var>`。解析过程使用 `<resolvers>` 指向的 DNS 解析器配置段。可选参数 'ipv4' 或 'ipv6' 用于指定解析偏好。另请参阅全局配置项 "dns-accept-family"，以强制限定使用特定地址族。

在执行 DNS 解析时，客户端连接将暂停，直至解析完成。若成功获取 IP 地址，则将其存储至 `<var>`。若发生任何错误，则 `<var>` 不会被设置。可使用此动作在运行时根据请求中获取的信息（例如 Host 头）发现服务器 IP 地址。若使用此动作查找服务器 IP 地址（通过 "set-dst" 动作），则后端中的服务器 IP 地址必须设置为 0.0.0.0。do-resolve 动作仅接受主机名参数，字符串中必须移除任何端口号。

示例：

```text
resolvers mydns
  nameserver local 127.0.0.53:53
  nameserver google 8.8.8.8:53
  timeout retry   1s
  hold valid 10s
  hold nx 3s
  hold other 3s
  hold obsolete 0s
  accepted_payload_size 8192

frontend fe
  bind 10.42.0.1:80
  http-request do-resolve(txn.myip,mydns,ipv4) hdr(Host),host_only
  http-request capture var(txn.myip) len 40

  # return 503 when the variable is not set,
  # which mean DNS resolution error
  use_backend b_503 unless { var(txn.myip) -m found }

  default_backend be

backend b_503
  # dummy backend used to return 503.
  # one can use the errorfile directive to send a nice
  # 503 error page to end users

backend be
  # rule to prevent HAProxy from reconnecting to services
  # on the local network (forged DNS name used to scan the network)
  http-request deny if { var(txn.myip) -m ip 127.0.0.0/8 10.0.0.0/8 }
  http-request set-dst var(txn.myip)
  server clear 0.0.0.0:0
```

请注意：务必设置“保护”规则，以确保 HAProxy 不会被用于扫描网络，或更糟的情况——自身形成循环...

<a id="entry-4-4-early-hint"></a>

**`early-hint <name> <fmt>`**

```haproxy
early-hint <name> <fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

在生成任何其他响应之前，用于构建 HTTP 103 Early Hints 响应。该指令将一个 HTTP 头字段附加到此响应中，头字段名称由 `<name>` 指定，其值由 `<fmt>` 定义，遵循自定义日志格式规则（参见 [第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6)）。此功能特别适用于向客户端传递 Link 头，以预加载渲染 HTML 文档所需的资源。

有关更多信息，请参阅 RFC 8297。

<a id="entry-4-4-expect-netscaler-cip-layer4"></a>

**`expect-netscaler-cip layer4`**

```haproxy
expect-netscaler-cip layer4
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| - \| - \| -
\| - \| - \| -

此配置使面向客户端的连接在从套接字读取任何字节之前接收 NetScaler 客户端 IP 插入协议头。这等效于在 "bind" 行上使用 "accept-netscaler-cip" 关键字，但使用 TCP 规则可仅通过 ACL 对特定 IP 地址范围接受 PROXY 协议。当来自公网主机的流量经过多层负载均衡器时，此方式较为便捷。

<a id="entry-4-4-expect-proxy-layer4"></a>

**`expect-proxy layer4`**

```haproxy
expect-proxy layer4
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| - \| - \| -
\| - \| - \| -

此配置使面向客户端的连接在从套接字读取任何字节之前接收 PROXY 协议头。这等效于在 "bind" 行上使用 "accept-proxy" 关键字，但使用 TCP 规则可仅对特定 IP 地址范围通过 ACL 接受 PROXY 协议。当来自公网主机的流量需经过多层负载均衡器时，该方式尤为方便。

<a id="entry-4-4-normalize-uri"></a>

**`normalize-uri <normalizer>`**

```haproxy
normalize-uri <normalizer>
normalize-uri fragment-encode
normalize-uri fragment-strip
normalize-uri path-merge-slashes
normalize-uri path-strip-dot
normalize-uri path-strip-dotdot [ full ]
normalize-uri percent-decode-unreserved [ strict ]
normalize-uri percent-to-uppercase [ strict ]
normalize-uri query-sort-by-name
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

对请求的 URI 执行规范化处理。

HAProxy 2.4 中的 URI 正常化功能目前作为实验性技术预览提供。因此，必须先启用全局指令 `expose-experimental-directives`，才能使用该功能。请注意，正常化器的行为可能会发生变化以修复潜在问题，这可能导致基础设施中请求处理出现异常。

每个归一化器处理一种类型的归一化，以实现对适用于所支持后端的归一化级别进行细粒度选择。

例如，“path-strip-dotdot” 正则化器对于直接将请求的 URI 映射到本地文件系统路径的静态文件服务器可能很有用。然而，它可能会破坏期望路径中包含特定段数的 API 的路由。

请注意，某些规范化器对格式错误的 URI 可能导致不安全的转换。也有可能，即使每个规范化器单独使用时都是安全的，但不当组合后仍可能导致不安全的转换。

例如，“percent-decode-unreserved” 正则化器在处理包含裸露百分号的损坏 URI 时，可能导致意外结果。一个典型的损坏 URI 是 "/%%36%36"，其解码后变为 "/%66"，而该结果等价于 "/f"。通过指定 "strict" 选项，对这类损坏 URI 的请求将被安全地拒绝。

以下可用的规范化器包括：

- fragment-encode: 将 "#" 编码为 "%23"。

应优先使用“fragment-strip”归一化器，除非已知存在无法正确编码路径组件中“#”符号的异常客户端。

示例：

  - /#foo -> /%23foo

- fragment-strip：移除 URI 的“片段”组件。

根据 RFC 3986#3.5，URI 的“片段”组件不应被发送，而应由用户代理在获取资源后进行处理。

此规范化器应优先应用，以确保片段不会被解释为请求路径组件的一部分。

示例：

  - /#foo -> /

- path-strip-dot: 删除 "path" 组件中的 "/./" 段（RFC 3986#6.2.2.3）。

包含百分号编码点号（"%2E"）的段落将不会被识别。如需避免此情况，请先使用 "percent-decode-unreserved" 正则化器。

示例：

  - /. -> /
  - /./bar/ -> /bar/
  - /a/./a -> /a/a
  - /.well-known/ -> /.well-known/（不变）

- path-strip-dotdot：规范化“path”组件中的“/../”段（RFC 3986#6.2.2.3）。

这会将尝试访问父目录的段与前一个段合并。

空段落不会获得特殊处理。若不希望如此，请先使用“merge-slashes”归一化器。

包含百分号编码点号（"%2E"）的段落将不会被识别。如需避免此情况，请先使用 "percent-decode-unreserved" 正则化器。

示例：

  - /foo/../ -> /
  - /foo/../bar/ -> /bar/
  - /foo/bar/../ -> /foo/
  - /../bar/ -> /../bar/
  - /bar/../../ -> /../
  - /foo//../ -> /foo/
  - /foo/%2E%2E/ -> /foo/%2E%2E/

如果指定了 "full" 选项，则开头的 "../" 也会被移除：

示例：

  - /../bar/ -> /bar/
  - /bar/../../ -> /

- path-merge-slashes：将“path”组件内的相邻斜杠合并为单个斜杠。

示例：

  - // -> /
  - /foo//bar -> /foo/bar

- percent-decode-unreserved：将未保留的百分号编码字符解码为其对应的普通字符表示（RFC 3986#6.2.2.2）。

未保留字符集包括所有字母、所有数字、“-”、"."、"\_" 以及“~”。

示例：

  - /%61dmin -\> /admin
  - /foo%3Fbar=baz -\> /foo%3Fbar=baz（不变）
  - /%%36%36 -\> /%66（不安全）
  - /%ZZ -\> /%ZZ

如果指定了“strict”选项，则无效的序列将导致返回 HTTP 400 错误请求。

示例：

  - /%%36%36 -> HTTP 400
  - /%ZZ -> HTTP 400

- percent-to-uppercase：将百分号编码序列中的字母转为大写（RFC 3986#6.2.2.1）。

示例：

  - /%6f -> /%6F
  - /%zz -> /%zz

如果指定了“strict”选项，则无效的序列将导致返回 HTTP 400 错误请求。

示例：

  - /%zz -> HTTP 400

- query-sort-by-name：按参数名称对查询字符串参数进行排序。参数假定以“&”分隔。名称较短的参数排在名称较长的参数之前，相同参数名称保持其相对顺序。

示例：

  - /?c=3&a=1&b=2 -> /?a=1&b=2&c=3
  - /?aaa=3&a=1&aa=2 -> /?a=1&aa=2&aaa=3
  - /?a=3&b=4&a=1&b=5&a=2 -> /?a=3&a=1&a=2&b=4&b=5

<a id="entry-4-4-pause"></a>

**`pause { <timeout> | <expr> }`**

```haproxy
pause { <timeout> | <expr> }
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

此操作将暂停指定毫秒数的消息分析。超时可指定为毫秒，或在数字后附加单位符号（如秒、分钟等），具体单位用法请参见本文档顶部说明。也可编写一个表达式，其结果必须为一个数值，并将该数值解释为以毫秒为单位的超时。若表达式求值失败，或返回无效值，则该动作被忽略，继续执行后续评估。

此动作可用于调试目的。但也可根据特定条件用于减缓部分客户端的处理速度。例如，可通过“track-sc”规则追踪客户端，当其请求速率过高时，实施限速。

<a id="entry-4-4-redirect"></a>

**`redirect <rule>`**

```haproxy
redirect <rule>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

此动作根据重定向规则执行 HTTP 重定向。其行为与“redirect”语句完全相同，但会插入一条在其他“http-request”或“http-response”规则中间处理的重定向规则，且这些规则使用自定义日志格式。对于响应，仅允许“location”类型的重定向。此外，当在响应过程中执行重定向时，服务器到 HAProxy 的数据传输将被中断，因此无法向客户端转发任何有效载荷。这可能导致部分 HTTP/1 连接被关闭。此动作为最终动作，即当前段中同一规则集的后续规则不再被评估。有关规则语法，请参见“redirect”关键字。

<a id="entry-4-4-reject"></a>

**`reject`**

```haproxy
reject
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| X \| X \| X \| X
\| X \| - \| -

这会停止规则的评估，并立即关闭连接，且不发送任何响应。对于 HTTP 规则，其行为类似于 "tcp-request content reject" 规则。在 HTTP/2 连接上强制立即关闭连接时，此操作可能有用。

在 "tcp-request connection" 规则中，被拒绝的连接甚至不会形成会话，因此在统计信息中被单独计入“被拒绝的连接”。这些连接不会被计入会话速率限制，也不会被记录日志。原因在于，此类规则仅应用于过滤极高连接速率的情况，例如大规模 DDoS 攻击期间所遇到的连接速率。在这些极端条件下，仅记录每个事件这一简单操作就可能导致系统崩溃，并显著降低过滤能力。若确实需要日志记录，则应改用 "tcp-request content" 规则，因为 "tcp-request session" 规则同样不会记录日志。

在“tcp-response content”规则中使用时，服务器连接将被关闭，响应将被中止。通常用于防止敏感信息泄露，通常在结合使用“wait-for-body”动作检查内容后执行。

此动作也可用于 "quic-initial" 规则。新建立的 QUIC 连接将立即关闭，且不执行任何 SSL 握手处理，客户端将通过 CONNECTION_REFUSED 错误码收到通知。

<a id="entry-4-4-replace-header"></a>

**`replace-header <name> <match-regex> <replace-fmt>`**

```haproxy
replace-header <name> <match-regex> <replace-fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

匹配所有出现的头字段 `<name>` 的值与 `<match-regex>`。匹配过程区分大小写。匹配到的值将被完全替换为 `<replace-fmt>`。`<replace-fmt>` 中允许使用格式字符，其作用方式与 "http-request add-header" 中的 `<fmt>` 参数相同。支持使用反斜杠（&#92;）后接数字的标准反向引用。

此动作作用于整行头，无论其包含多少个值。因此，它非常适合处理值中天然包含逗号的头，例如 If-Modified-Since 或 Set-Cookie。对于包含逗号分隔值列表的头，如 Accept 或 Cache-Control，应使用“replace-value”动作进行处理。另请参阅“replace-value”动作。

示例：

```shell
http-request replace-header Cookie foo=([^;]*);(.*) foo=\1;ip=%bi;\2

# applied to:
Cookie: foo=foobar; expires=Tue, 14-Jun-2016 01:40:45 GMT;

# outputs:
Cookie: foo=foobar;ip=192.168.1.20; expires=Tue, 14-Jun-2016 01:40:45 GMT;

# assuming the backend IP is 192.168.1.20

http-request replace-header User-Agent curl foo

# applied to:
User-Agent: curl/7.47.0

# outputs:
User-Agent: foo
```

示例：

```shell
http-response replace-header Set-Cookie (C=[^;]*);(.*) \1;ip=%bi;\2

# applied to:
Set-Cookie: C=1; expires=Tue, 14-Jun-2016 01:40:45 GMT

# outputs:
Set-Cookie: C=1;ip=192.168.1.20; expires=Tue, 14-Jun-2016 01:40:45 GMT

# assuming the backend IP is 192.168.1.20.

```

<a id="entry-4-4-replace-path"></a>

**`replace-path <match-regex> <replace-fmt>`**

```haproxy
replace-path <match-regex> <replace-fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

这与 "replace-header" 的工作方式类似，但其作用对象为请求的路径组件，而非头字段。路径组件从可选的协议+授权信息后的第一个 "/" 开始，到问号前结束。因此，替换操作不会修改协议、授权信息和查询字符串。

请注意，正则表达式在评估时可能比某些 ACL 更耗费资源，因此在极少情况下，可通过添加条件来避免执行评估，以提升性能。

示例：

```shell
# prefix /foo: turn /bar?q=1 into /foo/bar?q=1:
http-request replace-path (.*) /foo\1

# strip /foo: turn /foo/bar?q=1 into /bar?q=1
http-request replace-path /foo/(.*) /\1
# or more efficient if only some requests match:
http-request replace-path /foo/(.*) /\1 if { url_beg /foo/ }

```

<a id="entry-4-4-replace-pathq"></a>

**`replace-pathq <match-regex> <replace-fmt>`**

```haproxy
replace-pathq <match-regex> <replace-fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

这与“http-request replace-path”效果相同，不同之处在于，若存在查询字符串，则路径中会包含该查询字符串。因此，路径和查询字符串均会被替换。

示例：

```shell
# suffix /foo: turn /bar?q=1 into /bar/foo?q=1:
http-request replace-pathq ([^?]*)(\?(.*))? \1/foo\2

```

<a id="entry-4-4-replace-uri"></a>

**`replace-uri <match-regex> <replace-fmt>`**

```haproxy
replace-uri <match-regex> <replace-fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

其功能类似于 "replace-header"，但作用于请求的 URI 部分，而非请求头。URI 部分可能包含可选的方案、授权信息或查询字符串。这些均被视为与匹配值相关的部分。

请注意，正则表达式在评估时可能比某些 ACL 更耗费资源，因此在极少情况下，可通过添加条件来避免执行评估，以提升性能。

请注意：在 HTTP/1.x 中，浏览器发送的绝大多数请求使用“源形式”，其与“绝对形式”的区别在于 URI 部分不包含方案或权威信息。绝大多数仅通过代理发送的请求、手工构造的请求以及某些应用程序生成的请求才会使用绝对形式。因此，在 HTTP/1.x 中，以“/”开头的规则通常可以正常工作。但在 HTTP/2 中，客户端被建议仅发送绝对 URI，这类 URI 的格式与 HTTP/1 客户端与代理通信时使用的格式一致。因此，当某些仅部分替换 URI 的规则在 HTTP/1 中有效时，可能在 HTTP/2 中失效。应将规则调整为可选地匹配方案和权威信息，或改用 replace-path。

示例：

```shell
# rewrite all "http" absolute requests to "https":
http-request replace-uri ^http://(.*) https://\1

# prefix /foo: turn /bar?q=1 into /foo/bar?q=1:
http-request replace-uri ([^/:]*://[^/]*)?(.*) \1/foo\2

```

<a id="entry-4-4-replace-value"></a>

**`replace-value <name> <match-regex> <replace-fmt>`**

```haproxy
replace-value <name> <match-regex> <replace-fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

这与 "replace-header" 的行为类似，但会将正则表达式与头字段中每个以逗号分隔的值 `<name>` 进行匹配，而非整个头字段。此功能适用于允许携带多个值的所有头字段。例如 Accept 请求头，或请求或响应中的 Cache-Control 头。

示例：

```shell
http-request replace-value X-Forwarded-For ^192\.168\.(.*)$ 172.16.\1

# applied to:
X-Forwarded-For: 192.168.10.1, 192.168.13.24, 10.0.0.37

# outputs:
X-Forwarded-For: 172.16.10.1, 172.16.13.24, 10.0.0.37
```

示例：

```shell
http-after-response replace-value Cache-control ^public$ private

# applied to:
Cache-Control: max-age=3600, public

# outputs:
Cache-Control: max-age=3600, private

```

<a id="entry-4-4-return"></a>

**`return [ status <code> ] [ content-type <type> ]`**

```haproxy
return [ status <code> ] [ content-type <type> ]
       [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

         file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
       [ hdr `<name>` `<fmt>` ]*

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

这会停止规则的评估，并立即返回响应。默认使用的响应状态码为 200。可选地，可通过 "status" 指定状态码。响应的 Content-Type 也可作为 "content-type" 的参数指定。最后，可定义响应内容本身。响应可以是完整的 HTTP 响应，指定要使用的错误文件，也可以是响应负载，指定要使用的文件或字符串。创建响应时遵循以下规则：

- 若未定义错误文件或要使用的负载内容，则返回一个虚拟响应。仅考虑 "status" 参数。其值可以是范围 [200, 599] 内的任意状态码。若指定 "content-type" 参数，将被忽略。

- 若设置了 "default-errorfiles" 参数，则使用代理的错误文件。若定义了 "status" 参数，其值必须为 HAProxy 支持的 HTTP 状态码之一（200、400、403、404、405、408、410、413、414、425、429、431、500、501、502、503 或 504）。若存在 "content-type" 参数，将被忽略。

- 若定义了特定的 errorfile，通过 "errorfile" 参数指定，将返回对应文件中的完整 HTTP 响应。仅考虑 "status" 参数。其值必须为 HAProxy 支持的 HTTP 状态码之一（200、400、403、404、405、408、410、413、414、425、429、431、500、501、502、503 或 504）。若存在 "content-type" 参数，将被忽略。

- 若定义了 http-errors 段，并包含 "errorfiles" 参数，则返回指定 http-errors 段中对应的文件，该文件包含完整的 HTTP 响应。仅考虑 "status" 参数。其值必须为 HAProxy 支持的状态码之一（200、400、403、404、405、408、410、413、414、425、429、431、500、501、502、503 或 504）。若存在 "content-type" 参数，将被忽略。

- 若指定 "file" 或 "lf-file" 参数，则文件内容将用作响应负载。若文件非空，其内容类型必须作为 "content-type" 参数指定；否则，任何 "content-type" 参数均被忽略。使用 "lf-file" 参数时，文件内容将按自定义日志格式解析（参见 [第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6)）。使用 "file" 参数时，内容被视为原始数据。

- 若指定 "string" 或 "lf-string" 参数，则使用定义的字符串作为响应负载。必须始终将 content-type 作为 "content-type" 的参数进行设置。使用 "lf-string" 参数时，字符串将按自定义日志格式进行解析（参见 [第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6)）。使用 "string" 参数时，视为原始字符串。

当响应不基于 errorfile 时，可以使用 "hdr" 参数向响应中附加 HTTP 头字段。否则，所有 "hdr" 参数均被忽略。每个参数的头名称由 `<name>` 指定，其值由 `<fmt>` 定义，该值需遵循 [第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6)中描述的自定义日志格式规则。

请注意，生成的响应必须小于缓冲区大小。为避免任何警告，当加载 errorfile 或原始文件时，用于头重写预留的缓冲区空间也必须为空。

此动作为最终动作，即当前段中不再评估同一规则集中的其他规则。

示例：

```text
http-request return errorfile /etc/haproxy/errorfiles/200.http \
    if { path /ping }

http-request return content-type image/x-icon file /var/www/favicon.ico  \
    if { path /favicon.ico }

http-request return status 403 content-type text/plain    \
    lf-string "Access denied. IP %[src] is blacklisted."  \
    if { src -f /etc/haproxy/blacklist.lst }

```

<a id="entry-4-4-sc-add-gpc"></a>

**`sc-add-gpc(<idx>,<sc-id>) { <int> | <expr> }`**

```haproxy
sc-add-gpc(<idx>,<sc-id>) { <int> | <expr> }
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

此动作将与 `<sc-id>` 指定的粘性计数器关联的数组中索引 `<idx>` 处的通用计数器（GPC）值，增加 `<int>` 的整数值或表达式 `<expr>` 的整数计算结果。整数和表达式均限于无符号 32 位值。若发生错误，此动作静默失败，后续动作的评估继续进行。`<idx>` 为 0 至 99 之间的整数，`<sc-id>` 为 0 至 2 之间的整数。若该索引处未存储 GPC 值，此动作也静默失败。即使值为零，表中的条目也会被刷新。'gpc_rate' 会自动调整以反映 GPC 值的平均增长速率。

此动作仅适用于 'gpc' 和 'gpc_rate' 数组数据类型（不适用于旧版的 'gpc0'、'gpc1'、'gpc0_rate' 及 'gpc1_rate' 数据类型）。旧版数据类型无对应函数，但如果值始终为 1，请参阅 'sc-inc-gpc()'、'sc-inc-gpc0()' 和 'sc-inc-gpc1()'。无法执行减操作，但可使用 'sc-set-gpt()' 在通用标签中存储精确值。

此动作的主要用途是统计评分或总量（例如，服务器或 WAF 报告的每个源 IP 的估算风险等级、上传的总字节数等）。

<a id="entry-4-4-sc-inc-gpc"></a>

**`sc-inc-gpc(<idx>,<sc-id>)`**

```haproxy
sc-inc-gpc(<idx>,<sc-id>)
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

此动作会将与 `<sc-id>` 指定的粘性计数器关联的数组中索引 `<idx>` 处的通用计数器（GPC）值加一。若发生错误，此动作静默失败，动作评估继续进行。`<idx>` 为 0 至 99 之间的整数，`<sc-id>` 为 0 至 2 之间的整数。若该索引处未存储 GPC，则此动作同样静默失败。此动作仅适用于 'gpc' 和 'gpc_rate' 数据类型（不适用于旧版 'gpc0'、'gpc1'、'gpc0_rate' 及 'gpc1_rate' 数据类型）。

<a id="entry-4-4-sc-inc-gpc0"></a>

**`sc-inc-gpc0(<sc-id>)`**

```haproxy
sc-inc-gpc0(<sc-id>)
sc-inc-gpc1(<sc-id>)
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

此动作根据 `<sc-id>` 指定的粘性计数器，递增 GPC0 或 GPC1 计数器。若发生错误，此动作静默失败，动作的评估将继续进行。

<a id="entry-4-4-sc-set-gpt"></a>

**`sc-set-gpt(<idx>,<sc-id>) { <int> | <expr> }`**

```haproxy
sc-set-gpt(<idx>,<sc-id>) { <int> | <expr> }
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

此动作将位于与 `<sc-id>` 指定的粘性计数器关联的数组中索引 `<idx>` 处的 32 位无符号 GPT 设置为 `<int>`/`<expr>` 的值。预期结果为布尔值。

若发生错误，该动作将静默失败，动作评估将继续进行。`<idx>` 为 0 至 99 之间的整数，`<sc-id>` 为 0 至 2 之间的整数。若该索引处未存储 GPT，同样会静默失败。

此动作仅适用于 'gpt' 数组数据类型（不适用于旧版 'gpt0' 数据类型）。

<a id="entry-4-4-sc-set-gpt0"></a>

**`sc-set-gpt0(<sc-id>) { <int> | <expr> }`**

```haproxy
sc-set-gpt0(<sc-id>) { <int> | <expr> }
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

此动作根据由 `<sc-id>` 指定的粘性计数器以及 `<int>`/`<expr>` 的值，设置 32 位无符号 GPT0 标签。预期结果为布尔值。若发生错误，此动作将静默失败，动作的评估将继续进行。此动作是 "sc-set-gpt(0,`<sc-id>`)" 的别名。另请参阅 "sc-set-gpt" 动作。

<a id="entry-4-4-send-retry"></a>

**`send-retry`**

```haproxy
send-retry
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| - \| - \| - \| -
\| - \| - \| -

此动作强制在收到客户端 Initial 数据包（无令牌）时发送重试（Retry）响应。此举有助于确保在实例化任何连接元素并开始握手前，客户端地址已通过验证。

<a id="entry-4-4-send-spoe-group"></a>

**`send-spoe-group <engine-name> <group-name>`**

```haproxy
send-spoe-group <engine-name> <group-name>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| -

此动作用于触发发送一组 SPOE 消息。为此，必须定义用于发送消息的 SPOE 引擎以及要发送的 SPOE 组。当然，SPOE 引擎必须指向一个已存在的 SPOE 过滤器。若在 SPOE 过滤器行中未提供引擎名称，则必须使用 SPOE 代理名称。

参数：

```text
<engine-name>  SPOE 引擎名称。

<group-name>   引擎配置中指定的 SPOE 组名称。
```

<a id="entry-4-4-set-bandwidth-limit"></a>

**`set-bandwidth-limit <name> [limit {<expr> | <size>}] [period {<expr> | <time>}]`**

```haproxy
set-bandwidth-limit <name> [limit {<expr> | <size>}] [period {<expr> | <time>}]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| -

本动作用于启用带宽限制过滤器 `<name>`，具体在上传或下载方向上生效，取决于过滤器类型。仅当 `<name>` 指向每流带宽限制过滤器时，方可自定义限制值和周期。执行 set-bandwidth-limit 规则时，会先将过滤器的所有设置重置为默认值，然后再启用该过滤器。因此，若对同一过滤器执行多个 "set-bandwidth-limit" 动作，仅最后一个生效。同一流上可启用多个带宽限制过滤器。

请注意，此动作不能在 defaults 段中使用，因为带宽限制过滤器无法在 defaults 段中定义。此外，仅限制 HTTP 负载传输，HTTP 头不计入限制。

参数：

```text
<expr>  是标准 HAProxy 表达式，由样本提取后接若干转换器构成，结果转换为整数。
        对 "limit" 参数，结果解释为字节大小；对 "period" 参数，结果解释为毫秒持续时间。

<size>  是数值，遵循 HAProxy 大小格式，以字节表示。

<time>  是数值，遵循 HAProxy 时间格式，以毫秒表示。
```

示例：

```text
http-request set-bandwidth-limit global-limit
http-request set-bandwidth-limit my-limit limit 1m period 10s
```

请参阅 [第 9.7 节](/zh/haproxy/filters/#section-9-7) 了解带宽限制过滤器的配置方法。

<a id="entry-4-4-set-bc-mark"></a>

**`set-bc-mark { <mark> | <expr> }`**

```haproxy
set-bc-mark { <mark> | <expr> }
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

用于在支持该功能的平台上，将 Netfilter/IPFW MARK 设置为后端连接（发送至服务器的所有数据包）的值 `<mark>` 或 `<expr>`。该值为无符号 32 位整数，可通过 Netfilter/IPFW 匹配，也可通过路由表匹配或使用 DTrace 监控数据包。`<mark>` 可以采用十进制或十六进制格式表示（以 "0x" 为前缀）。或者，也可使用 `<expr>`：其为标准 HAProxy 表达式，由一个样本提取操作后接若干转换器组成，必须解析为整数类型。该动作可用于强制特定数据包走不同路径（例如，为大批量下载选择成本更低的网络路径）。此功能在 Linux 内核 2.6.32 及以上版本中可用，需具备管理员权限，同时在 FreeBSD 和 OpenBSD 上也支持。标记将在后端/服务器连接的整个持续时间内生效（从连接建立到关闭）。

<a id="entry-4-4-set-bc-tos"></a>

**`set-bc-tos { <tos> | <expr> }`**

```haproxy
set-bc-tos { <tos> | <expr> }
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

用于设置后端连接（发送至服务器的所有数据包）的 TOS 或 DSCP 字段值为 `<tos>` 或 `<expr>` 所指定的值，仅在支持该功能的平台上生效。该值表示 IP TOS 字段的全部 8 位。请注意，DSCP 或 TOS 仅使用其中的高 6 位，低 2 位始终为 0。或者，也可使用 `<expr>`：其为标准 HAProxy 表达式，由一个样本提取操作后接若干转换器构成，必须解析为整数类型。该动作可用于根据请求中的某些信息调整内部路由器的路由行为。TOS 将在后端/服务器连接的整个持续时间内生效（从连接建立到关闭）。

有关更多信息，请参见 RFC 2474、2597、3260 和 4594。

<a id="entry-4-4-set-dst"></a>

**`set-dst <expr>`**

```haproxy
set-dst <expr>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

用于将目标 IP 地址设置为指定表达式的值。当 HAProxy 前置代理重写了目标 IP，但通过 HTTP 头提供了正确的 IP 时，此功能非常有用；或当需要出于隐私考虑隐藏 IP 地址时。若要连接到新的地址/端口，请在后端中将服务器地址设为 `0.0.0.0:0`。

参数：

```text
<expr>  是标准 HAProxy 表达式，由样本提取后接若干转换器构成。
```

示例：

```text
http-request set-dst hdr(x-dst)
http-request set-dst dst,ipmask(24)
```

在可能的情况下，set-dst 会保留原始目标端口，只要地址族允许；否则，目标端口将被设为 0。

<a id="entry-4-4-set-dst-port"></a>

**`set-dst-port <expr>`**

```haproxy
set-dst-port <expr>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

用于将目标端口地址设置为指定表达式的值。若要连接到新的地址/端口，请在后端中将服务器地址设为 '0.0.0.0:0'。

参数：

```text
<expr>  是标准 HAProxy 表达式，由样本提取后接若干转换器构成。
```

示例：

```text
http-request set-dst-port hdr(x-port)
http-request set-dst-port int(4000)
```

在可能的情况下，set-dst-port 会保留原始目标地址，只要地址族支持端口；否则，它会在重写端口前将目标地址强制转换为 IPv4 "0.0.0.0"。

<a id="entry-4-4-set-fc-mark"></a>

**`set-fc-mark { <mark> | <expr> }`**

```haproxy
set-fc-mark { <mark> | <expr> }
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| -

用于在支持该功能的平台上，将发送至客户端的所有数据包的 Netfilter/IPFW MARK 设置为传入的值 `<mark>` 或 `<expr>`。该值为无符号 32 位整数，可被 netfilter/ipfw 匹配，也可通过路由表进行匹配，或通过 DTrace 监控数据包。`<mark>` 可以采用十进制或十六进制格式表示（以 "0x" 为前缀）。或者，也可使用 `<expr>`：其为标准 HAProxy 表达式，由一个样本提取操作后接若干转换器组成，且必须解析为整数类型。该动作可用于强制特定数据包走不同的路由（例如，为大批量下载选择成本更低的网络路径）。此功能在 Linux 内核 2.6.32 及以上版本中可用，需管理员权限；在 FreeBSD 和 OpenBSD 上同样适用。

<a id="entry-4-4-set-fc-tos"></a>

**`set-fc-tos { <tos | <expr> }`**

```haproxy
set-fc-tos { <tos | <expr> }
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| -

用于将发送至客户端的数据包的 TOS 或 DSCP 字段值设置为传入的 `<tos>` 或 `<expr>` 值，适用于支持该功能的平台。该值表示 IP TOS 字段的全部 8 位。请注意，DSCP 或 TOS 仅使用其中的 6 个高位，而两个低位始终为 0。或者，也可使用 `<expr>`：它是一个标准的 HAProxy 表达式，由一个 sample-fetch 后接若干转换器组成，且必须解析为整数类型。该动作可用于根据请求中的某些信息调整边界路由器的路由行为。

有关更多信息，请参见 RFC 2474、2597、3260 和 4594。

<a id="entry-4-4-set-header"></a>

**`set-header <name> <fmt>`**

```haproxy
set-header <name> <fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

此动作与“add-header”动作功能相同，不同之处在于，若该头已存在，则会先将其移除。
当向服务器传递安全信息时，该头必须不受外部用户篡改，或用于强制设置某些响应头（如“Server”），以隐藏外部信息，此时此动作尤为有用。请注意，新值在移除操作前已计算完成，因此可将新值与现有头合并。

示例：

```text
http-request set-header X-Haproxy-Current-Date %T
http-request set-header X-SSL                  %[ssl_fc]
http-request set-header X-SSL-Session_ID       %[ssl_fc_session_id,hex]
http-request set-header X-SSL-Client-Verify    %[ssl_c_verify]
http-request set-header X-SSL-Client-DN        %{+Q}[ssl_c_s_dn]
http-request set-header X-SSL-Client-CN        %{+Q}[ssl_c_s_dn(cn)]
http-request set-header X-SSL-Issuer           %{+Q}[ssl_c_i_dn]
http-request set-header X-SSL-Client-NotBefore %{+Q}[ssl_c_notbefore]
http-request set-header X-SSL-Client-NotAfter  %{+Q}[ssl_c_notafter]
```

<a id="entry-4-4-set-headers-bin"></a>

**`set-headers-bin <expr> [ prefix <str> ]`**

```haproxy
set-headers-bin <expr> [ prefix <str> ]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

这是“set-header”动作的一种变体，其中头名称和值以 varint 编码的二进制字符串形式传递。请参阅 "req.hdrs_bin" 样本提取关于 varint 格式的说明。当需要一次性设置多个头而无需预先知晓头名称时，此方法非常有用。请注意，这些头未经过 HTTP 解析器验证，可能导致发出无效消息，最严重情况下可能引发请求走私攻击。插入头的数量同样重要，因为其受 tune.http.maxhdr 限制。可选前缀仅会设置编码字符串中以 `<str>` 开头的头。

示例：

```shell
# This would reset the Accept/UA/Host headers to their initial values
http-request set-var(txn.oldheaders) req.hdrs_bin
http-request del-header Accept
http-request del-header User-Agent
http-request del-header Host
http-request set-headers-bin var(txn.oldheaders)

```

<a id="entry-4-4-set-log-level"></a>

**`set-log-level <level>`**

```haproxy
set-log-level <level>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| X

当满足特定条件时，用于更改当前请求的日志级别。有效级别包括 8 个 syslog 级别（参见“log”关键字），以及特殊级别“silent”，该级别将禁用此请求的日志记录。该规则非最终规则，因此最后一个匹配的规则生效。此规则可用于禁用来自其他设备的健康检查。

<a id="entry-4-4-set-map"></a>

**`set-map(<map-name>) <key fmt> <value fmt>`**

```haproxy
set-map(<map-name>) <key fmt> <value fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

用于向映射中添加新条目。`<map-name>` 必须遵循 2.7 段中描述的名称格式，关于映射和 ACL 的名称格式。要更新的 MAP 名称置于括号之间。该指令接受两个参数：`<key fmt>`，其格式遵循自定义日志格式规则，如[第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6)所述，用于收集映射键；以及 `<value fmt>`，同样遵循自定义日志格式规则，用于收集新条目的内容。插入前会先执行映射查找，以避免重复（或更多）值。此操作等效于通过统计信息套接字执行的“set map”命令，但可通过 HTTP 请求触发。

<a id="entry-4-4-set-mark"></a>

**`set-mark <mark> (deprecated)`**

```haproxy
set-mark <mark> (deprecated)
```

这是 "set-fc-mark" 的别名（应改用后者）。

<a id="entry-4-4-set-method"></a>

**`set-method <fmt>`**

```haproxy
set-method <fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

使用格式字符串 `<fmt>` 的求值结果重写请求方法。除非有极少数合理原因，否则不应执行此操作，因为这更可能造成破坏而非修复问题。

<a id="entry-4-4-set-nice"></a>

**`set-nice <nice>`**

```haproxy
set-nice <nice>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| -

设置当前正在处理的请求/响应的“nice”优先级。该设置仅对同时处理的其他请求产生影响。默认值为 0，除非通过 “bind” 行上的 “nice” 设置进行了修改。允许的取值范围为 -1024..1024.。数值越高，请求越“友好”（优先级越低）；数值越低，请求相对于其他请求的优先级越高。该设置可用于提升某些请求的处理速度，或降低非重要请求的优先级。未经事先试验直接使用此设置，可能导致显著的性能下降。

<a id="entry-4-4-set-path"></a>

**`set-path <fmt>`**

```haproxy
set-path <fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

    使用格式化字符串 `<fmt>` 的求值结果改写请求路径。查询字符串（如果
    存在）保持不变。如果在路径之前发现方案和授权部分，它们同样保持不变。
    如果请求没有路径（"*"），则用该格式替换。例如，这可用于在路径前面
    添加目录组件。另请参阅 "http-request set-query" 和 "http-request
    set-uri"。

示例：

```shell
# prepend the host name before the path
http-request set-path /%[hdr(host)]%[path]

```

<a id="entry-4-4-set-pathq"></a>

**`set-pathq <fmt>`**

```haproxy
set-pathq <fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

这与“http-request set-path”效果相同，不同之处在于查询字符串也会被重写。可以使用此指令移除查询字符串，包括问号（使用“http-request set-query”无法实现）。

<a id="entry-4-4-set-priority-class"></a>

**`set-priority-class <expr>`**

```haproxy
set-priority-class <expr>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

用于设置当前请求的队列优先级类别。该值必须为一个样本表达式，其结果需为 -2047..2047 范围内的整数。超出此范围的结果将被截断。优先级类别决定队列中请求的处理顺序，数值越低优先级越高。

<a id="entry-4-4-set-priority-offset"></a>

**`set-priority-offset <expr>`**

```haproxy
set-priority-offset <expr>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

用于设置当前请求的队列优先级时间戳偏移量。该值必须为一个样本表达式，其结果需为介于 -524287..524287 范围内的整数。超出此范围的结果将被截断。当请求进入队列时，其排序顺序首先按优先级类别，其次按当前时间戳减去指定偏移量（单位为毫秒）后的值确定。数值越小，优先级越高。请注意，所记录的时间戳仅具备足够精度以区分 524,287ms（8m44s287ms）内的差异。若请求在队列中等待时间过长，导致调整后的时间戳超过该值，将被错误识别为最高优先级。因此，务必设置 "timeout queue" 为一个合适的值，确保其与偏移量之和不超过此限制。

<a id="entry-4-4-set-query"></a>

**`set-query <fmt>`**

```haproxy
set-query <fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

此操作将请求的查询字符串（位于首个问号“?”之后的部分）替换为格式字符串 `<fmt>` 的求值结果。问号之前的部分保持不变。若请求中未包含问号且新值非空，则在 URI 末尾添加问号，后接新值。若原请求中已存在问号，则即使新值为空，问号也不会被移除。此功能可用于向查询字符串中添加或移除参数。

另请参阅 “http-request set-query” 和 “http-request set-uri”。

示例：

```shell
# replace "%3D" with "=" in the query string
http-request set-query %[query,regsub(%3D,=,g)]

```

<a id="entry-4-4-set-retries"></a>

**`set-retries <int> | <epxr>`**

```haproxy
set-retries <int> | <epxr>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

此动作仅覆盖当前流指定的“retries”值。其值可以是整数，范围为 [0, 100]，也可以是返回整数且范围在 [0, 100] 内的表达式。

请注意，此动作仅在后端侧有效，因此该规则仅适用于具备后端能力的代理。在“defaults”段中不允许使用此规则。当该动作用于监听器时，其评估上下文为前端。因此，仅当流未通过 use-backend 规则等路由至其他后端时，重试次数才会被保留。否则，将采用所选后端的默认重试次数。

示例：

```text
tcp-request content set-retries 3
http-request set-retries var(txn.retries)
```

<a id="entry-4-4-set-src"></a>

**`set-src <expr>`**

```haproxy
set-src <expr>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

用于将源 IP 地址设置为指定表达式的值。当 HAProxy 前方的代理重写了源 IP，但通过 HTTP 头提供了正确的 IP 时，此功能非常有用；或当你希望出于隐私保护目的隐藏源 IP 时。后续所有对 "src" 获取操作均返回该值（参见示例）。

参数：

```text
<expr>  是标准 HAProxy 表达式，由样本提取后接若干转换器构成。
```

另请参阅“option forwardfor”。

示例：

```shell
http-request set-src hdr(x-forwarded-for)
http-request set-src src,ipmask(24)

# After the masking this will track connections
# based on the IP address with the last byte zeroed out.
http-request track-sc0 src
```

在可能的情况下，set-src 会保留原始源端口，只要地址族允许；否则，源端口将被设为 0。

<a id="entry-4-4-set-src-port"></a>

**`set-src-port <expr>`**

```haproxy
set-src-port <expr>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

用于将源端口地址设置为指定表达式的值。

参数：

```text
<expr>  是标准 HAProxy 表达式，由样本提取后接若干转换器构成。
```

示例：

```text
http-request set-src-port hdr(x-port)
http-request set-src-port int(4000)
```

当可能时，set-src-port 会保留原始源地址，前提是地址族支持端口；否则，它会在重写端口前将源地址强制转换为 IPv4 "0.0.0.0"。

<a id="entry-4-4-set-status"></a>

**`set-status <status> [reason <str>]`**

```haproxy
set-status <status> [reason <str>]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| - \| X \| X

将响应状态码替换为 `<status>`，该值必须为 100 至 999 之间的整数。
可选地，可提供由 `<str>` 定义的自定义原因文本，或使用指定代码的默认原因作为回退。请注意，原因字符串仅存在于 HTTP/1.x 中，其他协议版本将忽略它。

示例：

```shell
# return "431 Request Header Fields Too Large"
http-response set-status 431
# return "503 Slow Down", custom reason
http-response set-status 503 reason "Slow Down".

```

<a id="entry-4-4-set-timeout"></a>

**`set-timeout { client | connect | queue | server | tarpit | tunnel } { <timeout> | <expr> }`**

```haproxy
set-timeout { client | connect | queue | server | tarpit | tunnel } { <timeout> | <expr> }
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

此动作仅覆盖当前流的指定“client”、“connect”、“queue”、“server”、“tarpit”或“tunnel”超时。更改某一超时不会影响其他任何超时，即使它们在配置解析过程中相互继承（参见最后一个示例）。超时可指定为毫秒，或在数字后附加单位（如“s”、“m”等），具体单位用法请参见本文档顶部说明。也可编写表达式，其结果必须为一个以毫秒为单位的数值。

请注意，connect、queue、server 和 tunnel 超时仅在后端侧有效，因此该规则仅适用于具备后端能力的代理。同理，client 超时仅在前端侧有效。tarpit 超时对两侧均可用。超时值必须非空，才能获得预期结果。当动作用于监听器时，其在前端上下文中进行评估。因此，仅当流未通过 use-backend 规则等路由至其他后端时，自定义的后端侧超时值才会被保留。否则，将采用所选后端的默认值。

示例：

```text
http-request set-timeout tunnel 5s
http-request set-timeout server req.hdr(host),map_int(host.lst)
```

示例：

```text
http-response set-timeout tunnel 5s
http-response set-timeout server res.hdr(X-Refresh-Seconds),mul(1000)
```

示例：

```text
defaults
  # This will set both tarpit and queue timeout to 5s as they are not
  # defined
  timeout connect 5s
  timeout client 30s
  timeout server 30s

listen foo
  # This will only change the connect timeout to 10s without affecting
  # queue or tarpit timeouts
  http-request set-timeout connect 10s
```

<a id="entry-4-4-set-tos"></a>

**`set-tos <tos> (deprecated)`**

```haproxy
set-tos <tos> (deprecated)
```

这是 "set-fc-tos" 的别名（应改用后者）。

<a id="entry-4-4-set-uri"></a>

**`set-uri <fmt>`**

```haproxy
set-uri <fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

此操作使用格式字符串 `<fmt>` 的计算结果重写请求 URI。协议、授权信息、路径和查询字符串将同时被替换。可用于重写代理前端的主机名，或对 URI 执行复杂修改，例如在路径与查询字符串之间移动部分内容。若设置绝对 URI，将原样发送至 HTTP/1.1 服务器。若非期望行为，应分别设置主机、路径和/或查询字符串。参见“http-request set-path”和“http-request set-query”。

<a id="entry-4-4-set-var"></a>

**`set-var(<var-name>[,<cond>...]) <expr>`**

```haproxy
set-var(<var-name>[,<cond>...]) <expr>
set-var-fmt(<var-name>[,<cond>...]) <fmt>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

用于设置变量的内容。变量在行内声明。

参数：

```text
<var-name>   是变量名称。不能设置父流的变量。详情见第 2.8 节的变量说明。

 <cond>      是一组条件，必须全部为真才会实际设置变量（例如 "ifnotempty"、"ifgt" 等）。
             所有可用条件见 set-var 转换器的说明。

 <expr>      是标准 HAProxy 表达式，由样本提取后接若干转换器构成。

 <fmt>       是以自定义日志格式规则表示的值（参见第 8.2.6 节的自定义日志格式）。
```

所有作用域均可用于 HTTP 规则，但规则集若无法访问内容（如 "tcp-request connection" 和 "tcp-request session"），则仅可使用作用域 "proc" 和 "sess"。

示例：

```text
http-request set-var(req.my_var) req.fhdr(user-agent),lower
http-request set-var-fmt(txn.from) %[src]:%[src_port]

```

<a id="entry-4-4-silent-drop"></a>

**`silent-drop [ rst-ttl <ttl> ]`**

```haproxy
silent-drop [ rst-ttl <ttl> ]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| -

这会停止规则的评估，并通过依赖系统的手段突然使面向客户端的连接消失，以尽量避免通知客户端。调用时若未指定 rst-ttl 参数，将尝试使用 TCP_REPAIR 防止向客户端发送任何 FIN 或 RST 数据包。若失败（主要由于权限不足），则退回到发送 TTL 为 1 的 RST 数据包。

客户端仍会看到已建立的连接，而 HAProxy 上并无实际连接，从而节省资源。然而，位于 HAProxy 与客户端之间的有状态设备（如防火墙、代理、负载均衡器）也会在其会话表中保持该连接。

可选的 rst-ttl 可更改此行为：TCP_REPAIR 不再使用，而是发送一个 TTL 可配置的 RST 数据包。当设置为合理值时，该 RST 数据包会穿过本地基础设施，清除防火墙及其他系统中的连接，但在到达客户端前消失。此后客户端发出的后续数据包将被前端设备直接丢弃。此类本地 RST 保护本地资源，但不保护客户端。除非完全理解其后果，否则不得使用。

<a id="entry-4-4-strict-mode"></a>

**`strict-mode { on | off }`**

```haproxy
strict-mode { on | off }
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

启用或禁用后续规则的严格重写模式。该设置不影响其之前的规则，且仅适用于对请求执行重写的规则。启用严格模式后，任何重写失败都会触发内部错误；否则，此类错误将被静默忽略。严格重写模式的目的是使部分重写可选，而其他重写则必须执行以继续请求处理。

默认情况下，严格重写模式已启用。当规则集评估结束时，其值也会被重置。例如，如果在前端更改了该模式，HAProxy 开始评估后端规则时将恢复默认模式。

<a id="entry-4-4-switch-mode-http"></a>

**`switch-mode http [ proto <name> ]`**

```haproxy
switch-mode http [ proto <name> ]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| - \| - \| -

用于执行连接升级的动作。目前仅支持 HTTP 升级。协议可选指定。该动作仅适用于具备前端能力的代理。连接升级会立即执行，后续不会评估“tcp-request content”规则。建议优先使用此方法，而非依赖后端模式的隐式升级方式。使用该方法时，可在前端中设置 HTTP 指令而无需警告。若执行了 HTTP 升级，这些指令将有条件地被评估。但必须仍选择一个 HTTP 后端。目前仍不支持将 HTTP 连接（无论是否已升级）路由至 TCP 服务器。

有关 HTTP 升级的更多详情，请参见 [第 4 节](/zh/haproxy/proxies/) 中的代理相关内容。

<a id="entry-4-4-tarpit"></a>

**`tarpit [ { status | deny_status } <code>] [content-type <type>]`**

```haproxy
tarpit [ { status | deny_status } <code>] [content-type <type>]
       [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

           file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
       [ hdr `<name>` `<fmt>` ]*

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

此规则会停止规则的进一步评估，并立即阻止请求，且不响应，延迟时间由 "timeout tarpit" 或 "timeout connect" 指定，若前者未设置则使用后者。延迟结束后，若客户端仍保持连接，则返回响应，以避免客户端怀疑已被陷井捕获。日志将报告标志 "PT"。陷井规则的目标是在攻击期间，针对并发请求数受限的机器人进行减速。该规则对非常简单的机器人极为有效，相比 "deny" 规则可显著降低防火墙的负载。但面对“正确”开发的机器人时，可能适得其反，迫使 HAProxy 和前端防火墙支持极高的并发连接数。默认情况下返回 HTTP 错误 500。但可通过与 "http-request return" 规则相同的语法自定义响应。详见 "http-request return"。

为保持兼容性，当未定义参数，或仅定义 "deny_status" 时，将隐式使用参数 "default-errorfiles"。这意味着 "http-request tarpit [deny_status `<status>`]" 是 "http-request tarpit [status `<status>`] default-errorfiles" 的别名。后续不再评估其他 "http-request" 规则。参见 "http-request return" 和 "http-request silent-drop"。

<a id="entry-4-4-track-sc0"></a>

**`track-sc0 <key> [table <table>]`**

```haproxy
track-sc0 <key> [table <table>]
track-sc1 <key> [table <table>]
track-sc2 <key> [table <table>]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| X \| -

此选项启用对当前请求的粘性计数器进行跟踪。这些规则不会停止评估，也不会更改默认动作。同一连接可同时跟踪的计数器数量由全局 "tune.stick-counters" 设置决定，若在构建时设置，则其值为 MAX_SESS_STKCTR（在 HAProxy -vv 中报告），否则默认值为 3，因此 track-sc 的数值范围为 0 至 (tune.stick-counters-1)。首个执行的 "track-sc0" 规则启用指定表的计数器作为第一组。首个执行的 "track-sc1" 规则启用指定表的计数器作为第二组。首个执行的 "track-sc2" 规则启用指定表的计数器作为第三组。建议将第一组计数器用于前端级计数，第二组用于后端级计数。但这仅为指导建议，所有组均可在任意位置使用。

参数：

```text
<key>   是必需的参数，是第 7.3 节所述的样本表达式规则，描述从入站连接、请求或响应中
        分析、提取并组合哪些元素，进而选择要更新计数器的表条目。

<table> 是可选的表，用于替代默认表，即当前代理中声明的 stick-table。
        此键的所有匹配和更新操作均在该表中计数，直至会话结束。
```

一旦执行了 "track-sc\*" 规则，便会查找该键对应的表项。若未找到，则为该键分配一个表项。随后，在会话的整个生命周期内，该表项的指针将被保留，并且每当会话的计数器更新时，该表项的计数器都会尽可能频繁地同步更新，且在会话结束时也会系统性地更新。计数器仅对跟踪开始后发生的事件进行更新。例外情况是，连接计数器和请求计数器会系统性地更新，以确保其反映有用信息。

如果条目跟踪并发连接计数器，则只要条目被跟踪，该连接即被计入，且在此期间条目不会过期。与仅检查键值相比，跟踪计数器还能带来性能优势，因为所有使用该计数器的 ACL 检查仅需执行一次表查找。

<a id="entry-4-4-unset-var"></a>

**`unset-var(<var-name>)`**

```haproxy
unset-var(<var-name>)
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

用于清除变量。有关 `<var-name>` 的详细信息，请参阅 "set-var" 动作。

示例：

```text
http-request unset-var(req.my_var)

```

<a id="entry-4-4-use-service"></a>

**`use-service <service-name>`**

```haproxy
use-service <service-name>
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

该动作根据其所在规则集的配置，执行相应的 TCP 或 HTTP 服务以响应请求。该规则为最终规则，即在同一规则集中不再评估后续规则。

服务可以选择发送任意有效的响应，也可以在不发送任何响应的情况下立即关闭连接。对于 HTTP 服务，有效的响应必须包含有效的 HTTP 响应。在原生服务之外，例如针对 HTTP 服务的 Prometheus 导出器，可以使用 Lua 编写自定义的 TCP 和 HTTP 服务。

参数：

```text
<service-name>  是必需的参数，指定要调用的服务。
```

示例：

```text
http-request use-service prometheus-exporter if { path /metrics }

```

<a id="entry-4-4-wait-for-body-time"></a>

**`wait-for-body time <time> [ at-least <bytes> ] [use-large-buffer]`**

```haproxy
wait-for-body time <time> [ at-least <bytes> ] [use-large-buffer]
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

这将延迟请求或响应的处理，直至满足以下任一条件：

- 完整的请求体已接收，此时处理流程正常进行。
- 已接收 `<bytes>` 字节，且提供了 "at-least" 参数，同时 `<bytes>` 非零，此时处理流程正常进行。
- 请求缓冲区已满，此时处理流程正常进行。该缓冲区的大小由 "tune.bufsize" 选项决定。
- 请求等待时间已超过 `<time>` 毫秒。此时 HAProxy 将向客户端返回 408 “请求超时” 错误并停止处理请求。请注意，若其他任一条件先发生，即使尚未接收完整请求体，此超时也不会触发。

"use-large-buffer" 选项可设置为在常规缓冲区不足以存储消息体时分配一个大缓冲区。若要使用，必须定义 "tune.bufsize.large" 全局选项。

此动作可作为 "option http-buffer-request" 的替代方案。

参数：

```text
<time>    是必需的参数，指定等待消息体的最长时间，遵循 HAProxy 时间格式，以毫秒表示。

<bytes>   是可选参数，指定停止等待前必须接收的最小负载大小，遵循 HAProxy 大小格式，以字节表示。
          值为 0（默认值）表示不限制。
```

示例：

```text
http-request wait-for-body time 1s at-least 1k if METH_POST
```

另请参阅："option http-buffer-request" 和 "tune.bufsize.large"

<a id="entry-4-4-wait-for-handshake"></a>

**`wait-for-handshake`**

```haproxy
wait-for-handshake
```

适用范围： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

这将延迟请求的处理，直到完成 SSL 握手。此举主要用于在确认早期数据有效之前延迟其处理。
