---
title: "12. 其他配置段"
linkTitle: "12. 其他配置段"
weight: 230
description: "跟踪、用户、邮件发送器、错误、环形缓冲区、证书、ACME、全局健康检查"
icon: fa-solid fa-ellipsis
module: [HAPROXY]
categories: [参考]
aliases:
  - /haproxy/configuration/other-sections/
  - /docs/haproxy/configuration/other-sections/
  - /haproxy/other-sections/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 12"
---

下述配置段较少使用，通常仅支持少量参数。它们之间不存在隐式关联。所有段均通过单一关键字启动。在 "global" 段之前禁止出现任何此类段。部分段的支持可能受构建选项限制（例如与 SSL 相关的任何功能）。

## 12.1. 跟踪 {#section-12-1}

为调试目的，可激活 HAProxy 子系统上的追踪功能。该功能将输出特定子系统的调试消息，是诊断问题的强力工具。可通过 CLI 动态配置追踪。也可在配置文件中通过专用 "traces" 段预先定义部分设置。有关追踪的更多详情，请参阅管理指南。它仍然是用于复杂调试会话的开发者工具。其输出相当冗长，且有一定开销，因此使用时应谨慎。并且由于它是开发者工具，本段不保证向后兼容性。

<a id="entry-12-1-traces"></a>

**`traces`**

```haproxy
traces
```

开始一个新的 traces 段。可使用一个或多个 "traces" 段。所有指令按声明顺序求值，后声明的指令会覆盖先前的指令。

<a id="entry-12-1-trace"></a>

**`trace <source> <args...>`**

```haproxy
trace <source> <args...>
```

用于配置 "trace" 子系统。其中每一项均可在管理手册中找到，并遵循完全相同的语法。"trace" 命令所产生的任何输出，均会在本段的解析阶段发出。大多数情况下，这些输出为错误和警告信息，但某些不完整的命令可能会列出允许的选择项。该命令并非用于常规使用，通常仅在复杂调试会话中由开发者建议使用。请注意，根据追踪级别和详细程度，启用追踪可能会严重降低整体性能。有关语句语法的详细信息，请参阅管理手册。

示例：

```text
ring buf1
  size 10485760 # 10MB
  format timed
  backing-file /tmp/h1.traces

ring buf2
  size 10485760 # 10MB
  format timed
  backing-file /tmp/h2.traces

traces
  trace h1 sink buf1 level developer verbosity complete start now
  trace h2 sink buf1 level developer verbosity complete start now
```

## 12.2. 用户列表 {#section-12-2}

可以控制对前端、后端、listen 段以及 HTTP 统计信息的访问，仅允许经过身份认证和授权的用户访问。为此，必须至少创建一个用户列表，并定义用户。

<a id="entry-12-2-userlist"></a>

**`userlist <listname>`**

```haproxy
userlist <listname>
```

创建名为 `<listname>` 的新用户列表。可使用多个独立的用户列表，以分别存储不同客户的认证与授权数据。

<a id="entry-12-2-group"></a>

**`group <groupname> [users <user>,<user>,(...)]`**

```haproxy
group <groupname> [users <user>,<user>,(...)]
```

将组 `<groupname>` 添加到当前用户列表中。也可通过在 "users" 关键字后使用以逗号分隔的用户名列表，将用户附加到该组。

<a id="entry-12-2-user"></a>

**`user <username> [password|insecure-password <password>]`**

```haproxy
user <username> [password|insecure-password <password>]
                [groups <group>,<group>,(...)]
```

将用户 `<username>` 添加至当前用户列表。可使用加密（安全）或非加密（不安全）密码。加密密码通过 crypt(3) 函数进行评估，具体支持的算法取决于系统的功能，例如基于现代 Glibc 的 Linux 系统支持 MD5、SHA-256、SHA-512，以及经典的基于 DES 的密码加密方法。

请注意：使用加密密码可能导致显著增加的 CPU 使用率，具体取决于请求数量以及所使用的算法。对于任何哈希变体，每个请求的密码都必须在与配置文件中指定的值进行比较之前，通过所选算法进行处理。当前大多数算法均故意设计为计算成本较高，以抵御暴力破解攻击。它们并非仅对明文密码进行一次加盐哈希，而是重复数千次。这可能迅速成为 HAProxy 整体 CPU 消耗的主要因素，甚至可能导致应用程序崩溃！

为降低哈希函数的高 CPU 使用率，一种方法是减少哈希函数（SHA 系列算法）的迭代轮数，或在算法支持的情况下降低 "cost" 值。

需要注意，使用 musl（例如 Alpine Linux）实现时，计算哈希值的性能通常低于其 glibc 对应实现，因此也建议考虑此因素。

所有密码均被视为普通参数，因此受 [第 2.2 节](/zh/docs/haproxy/configuration-basics/#section-2-2) 引用与转义规则约束。建议对密码使用单引号。

示例：

```text
userlist L1
  group G1 users tiger,scott
  group G2 users xdb,scott

  user tiger password $6$k6y3o.eP$JlKBx9za9667qe4(...)xHSwRv6J.C0/D7cV91
  user scott insecure-password 'elgato'
  user xdb insecure-password 'hello'

userlist L2
  group G1
  group G2

  user tiger password $6$k6y3o.eP$JlKBx(...)xHSwRv6J.C0/D7cV91 groups G1
  user scott insecure-password 'elgato' groups G1,G2
  user xdb insecure-password 'hello' groups G2
```

请注意，两个列表在功能上完全相同。

## 12.3. 邮件发送器 {#section-12-3}

当服务器状态发生变化时，可发送电子邮件警报。若已配置邮件警报，将向 mailers 段中配置的每个邮件发送器发送邮件。邮件通过 Lua 发送（参见 examples/lua/mailers.lua）。

<a id="entry-12-3-mailers"></a>

**`mailers <mailersect>`**

```haproxy
mailers <mailersect>
```

创建一个名为 `<mailersect>` 的新邮件发送器列表。该列表为独立配置段，可被一个或多个代理引用。

<a id="entry-12-3-mailer"></a>

**`mailer <mailername> <ip>:<port>`**

```haproxy
mailer <mailername> <ip>:<port>
```

在 mailers 段中定义一个邮件发送器。

示例：

```text
global
    # mailers.lua file as provided in the git repository
    # adjust path as needed
    lua-load examples/lua/mailers.lua

mailers mymailers
    mailer smtp1 192.168.0.1:587
    mailer smtp2 192.168.0.2:587

backend mybackend
    mode tcp
    balance roundrobin

    email-alert mailers mymailers
    email-alert from test1@horms.org
    email-alert to test2@horms.org

    server srv1 192.168.0.30:80
    server srv2 192.168.0.31:80
```

<a id="entry-12-3-timeout-mail"></a>

**`timeout mail <time>`**

```haproxy
timeout mail <time>
```

定义建立邮件/连接并将其发送至邮件服务器所需的可用时间。若未定义，默认值为 10 秒。为确保初始 TCP 握手期间至少可发送两个 SYN-ACK 数据包，建议将此值保持在 4 秒以上。

示例：

```text
mailers mymailers
    timeout mail 20s
    mailer smtp1 192.168.0.1:587
```

## 12.4. HTTP 错误 {#section-12-4}

可以全局声明多个 HTTP 错误组，后续可在任意代理段中导入。同一组可被多次引用，且可完全或部分导入。

<a id="entry-12-4-http-errors"></a>

**`http-errors <name>`**

```haproxy
http-errors <name>
```

创建一个名为 `<name>` 的新 http-errors 组。该组为独立段，可被一个或多个代理通过名称引用。

<a id="entry-12-4-errorfile"></a>

**`errorfile <code> <file>`**

```haproxy
errorfile <code> <file>
```

将文件内容与 HTTP 错误码关联

参数：

```text
<code>    是 HTTP 状态码。目前 HAProxy 可生成的状态码为
          200、400、401、403、404、405、407、408、410、425、429、500、501、502、503 和 504。

<file>    指定包含完整 HTTP 响应的文件。建议遵循常见做法，在文件名末尾添加 ".http"，
          避免将响应与 HTML 错误页面混淆；还应使用绝对路径，因为文件在执行 chroot 之前读取。
```

请参阅 "errorfile" 关键字在 [第 4 节](/zh/docs/haproxy/proxies/) 中的说明以获取详细信息。

示例：

```text
http-errors website-1
    errorfile 400 /etc/haproxy/errorfiles/site1/400.http
    errorfile 404 /etc/haproxy/errorfiles/site1/404.http
    errorfile 408 /dev/null  # work around Chrome pre-connect bug

http-errors website-2
    errorfile 400 /etc/haproxy/errorfiles/site2/400.http
    errorfile 404 /etc/haproxy/errorfiles/site2/404.http
    errorfile 408 /dev/null  # work around Chrome pre-connect bug
```

## 12.5. 环形缓冲区 {#section-12-5}

可以全局声明环形缓冲区，用作日志服务器或追踪目标。

<a id="entry-12-5-ring"></a>

**`ring <ringname>`**

```haproxy
ring <ringname>
```

创建一个名为 `<ringname>` 的环形缓冲区。

<a id="entry-12-5-backing-file"></a>

**`backing-file <path>`**

```haproxy
backing-file <path>
```

使用内存映射文件替代常规内存分配来存储环形缓冲区。这在无需通过慢速客户端连接 CLI 的情况下，可用于收集用于事后分析的追踪数据或日志。新写入的内容将自动覆盖旧内容，确保始终可获取最新数据。写入环形缓冲区的内容将在进程停止后在该文件中可见（大多数情况下甚至会很快可见，但由于写入并非同步，并无此类保证）。

当使用此选项时，总存储区域将减少“struct ring”所占的大小，该结构从区域起始位置开始，用于恢复区域内容。文件将以起始用户的所有权创建，权限模式为 0600，并且大小由 "size" 指令配置。在指令解析时（即使在配置检查期间），任何已存在的非空文件将首先被重命名为附加后缀 ".bak"，任何先前存在的带有后缀 ".bak" 的文件将被删除。这确保了进程的即时重载或重启不会清除宝贵的调试信息，并为管理员留出时间发现此新生成的 ".bak" 文件，必要时可将其归档。因此，在崩溃后，由 `<path>` 指定的文件将包含最新信息；若服务重启，则“`<path>`.bak”文件将包含该信息。这意味着所需的总存储容量将是环形缓冲区大小的两倍。文件轮转失败将被静默忽略，因此将文件置于无写权限的目录中即可避免生成备份文件（如无需该功能）。

警告：使用此功能存在稳定性与安全隐患。首先，将环形缓冲区（ring）备份到慢速设备（例如物理硬盘）可能导致访问时出现明显延迟，若过多线程竞争访问，甚至可能引发系统崩溃。其次，外部进程修改该区域可能导致 HAProxy 进程崩溃，或导致其自身内存被追踪数据覆盖。第三，若文件系统在环形缓冲区之前已满，向环形缓冲区写入数据可能引发进程崩溃。

环形缓冲区中的信息采用结构化格式，无法直接通过文本编辑器读取（尽管其中大部分内容看起来几乎无法阅读）。该文件的输出仅适用于开发者。

<a id="entry-12-5-description"></a>

**`description <text>`**

```haproxy
description <text>
```

描述为环形缓冲区的可选描述字符串，将在 CLI 中显示。默认情况下，`<name>` 被复用以填充此字段。

<a id="entry-12-5-format"></a>

**`format <format>`**

```haproxy
format <format>
```

用于将事件存储到环形缓冲区的格式。

参数：

```text
<format> 是生成 syslog 消息时使用的日志格式，可为以下值之一：

  iso     仅包含 ISO 日期及其后的文本，省略 PID、进程名称和系统名称，适用于本地日志服务器。

  local   类似 rfc3164 syslog 消息格式，但去除主机名字段。这是默认值。
          注意："log-send-hostname" 选项会将默认值切换为 rfc3164。

  raw     仅包含文本，省略级别、PID、日期、时间、进程名称和系统名称。
          适用于容器或开发环境，此时严重程度仅取决于使用的文件描述符（stdout/stderr）。
          这是默认值。

  rfc3164 RFC3164 syslog 消息格式。
          (https://tools.ietf.org/html/rfc3164)

  rfc5424 RFC5424 syslog 消息格式。
          (https://tools.ietf.org/html/rfc5424)

  short   仅包含尖括号内的级别，例如 '<3>'，以及其后的文本。
          省略 PID、日期、时间、进程名称和系统名称，适用于本地日志服务器。
          此格式兼容 systemd 日志记录器。

 priority 仅包含尖括号内的级别与 syslog facility 之和，例如 '<63>'，以及其后的文本。
          省略 PID、日期、时间、进程名称和系统名称，适用于本地日志服务器。

  timed   仅包含尖括号内的级别，例如 '<3>'，以及其后的 ISO 日期和文本。
          省略 PID、进程名称和系统名称，适用于本地日志服务器。
```

<a id="entry-12-5-maxlen"></a>

**`maxlen <length>`**

```haproxy
maxlen <length>
```

存储于环形缓冲区中的事件消息的最大长度，包括格式化头。若事件消息长度超过 `<length>`，将被截断至该长度。

<a id="entry-12-5-server"></a>

**`server <name> <address> [param*]`**

```haproxy
server <name> <address> [param*]
```

用于配置一个 syslog TCP 服务器，以将环形缓冲区中的消息转发出去。此功能支持 5.2 段中列出的所有 "server" 参数。其中部分参数对 "ring" 段不适用。重要提示：向环形缓冲区添加多个服务器并无实际意义，因为所有服务器将收到环形缓冲区内容的完全相同副本，环形缓冲区的推进速度将受限于最慢的服务器。若某一服务器无响应，将导致旧消息无法被清除，甚至可能阻塞新消息插入环形缓冲区。向多个服务器发送消息的正确方式是为每个日志服务器配置独立的环形缓冲区，而非将多个服务器绑定至同一环形缓冲区。请注意，特定的服务器指令 "log-proto" 用于设置消息发送所使用的协议。

<a id="entry-12-5-size"></a>

**`size <size>`**

```haproxy
size <size>
```

这是可选的环形缓冲区大小，单位为字节。默认值设为 BUFSIZE。

<a id="entry-12-5-timeout-connect"></a>

**`timeout connect <timeout>`**

```haproxy
timeout connect <timeout>
```

设置连接尝试连接服务器时等待成功的最长时间。

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

<a id="entry-12-5-timeout-server"></a>

**`timeout server <timeout>`**

```haproxy
timeout server <timeout>
```

设置输出缓冲区中待处理数据的最大停留时间。

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

示例：

```text
global
    log ring@myring local7

ring myring
    description "My local buffer"
    format rfc5424
    maxlen 1200
    size 32764
    timeout connect 5s
    timeout server 10s
    server mysyslogsrv 127.0.0.1:6514 log-proto octet-count
```

## 12.6. 日志转发 {#section-12-6}

可以声明一个或多个日志转发段，HAProxy 会将所有接收到的日志消息转发至日志服务器列表。

<a id="entry-12-6-log-forward"></a>

**`log-forward <name>`**

```haproxy
log-forward <name>
```

创建一个标识为 `<name>` 的新日志转发代理。

<a id="entry-12-6-backlog"></a>

**`backlog <conns>`**

```haproxy
backlog <conns>
```

向系统提供关于连接接收时期望的监听队列大小的提示。

<a id="entry-12-6-bind"></a>

**`bind <addr> [param*]`**

```haproxy
bind <addr> [param*]
```

用于配置流日志监听器以接收待转发的消息。此功能支持 5.1 小节中列出的 "bind" 参数，包括与 ssl 相关的参数，但某些语句如 "alpn" 对于通过 TCP 传输的 syslog 协议可能不适用。这些监听器支持 rfc-6587 中定义的“八位组计数”（Octet Counting）和“非透明成帧”（Non-Transparent-Framing）模式。

<a id="entry-12-6-dgram-bind"></a>

**`dgram-bind <addr> [param*]`**

```haproxy
dgram-bind <addr> [param*]
```

用于配置一个数据报日志监听器，以接收需转发的消息。地址必须采用 IPv4 或 IPv6 格式，后接端口。此配置支持 5.1 小节中部分 "bind" 参数，其中 "interface"、"namespace" 或 "transparent" 有效，其余参数在 UDP/syslog 场景下被视为无关，将被静默忽略。

<a id="entry-12-6-log-global"></a>

**`log global`**

```haproxy
log global
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    <facility> [<level> [<minlevel>]]
```

用于配置目标日志服务器。有关代理的更多详细信息，请参见代理文档。若未指定日志格式，HAProxy 将尝试保留传入日志的格式。配置的 facility 会被忽略，除非传入消息中未包含 facility，而输出格式中该字段为必填项。若输入格式中无时间戳，但输出格式中存在该字段，HAProxy 将使用本地日期。

示例：

```text
global
   log stderr format iso local7

ring myring
    description "My local buffer"
    format rfc5424
    maxlen 1200
    size 32764
    timeout connect 5s
    timeout server 10s
    # syslog tcp server
    server mysyslogsrv 127.0.0.1:514 log-proto octet-count

log-forward sylog-loadb
    dgram-bind 127.0.0.1:1514
    bind 127.0.0.1:1514
    # all messages on stderr
    log global
    # all messages on local tcp syslog server
    log ring@myring local0
    # load balance messages on 4 udp syslog servers
    log 127.0.0.1:10001 sample 1:4 local0
    log 127.0.0.1:10002 sample 2:4 local0
    log 127.0.0.1:10003 sample 3:4 local0
    log 127.0.0.1:10004 sample 4:4 local0
```

<a id="entry-12-6-maxconn"></a>

**`maxconn <conns>`**

```haproxy
maxconn <conns>
```

设定日志转发器上并发连接数的上限。默认值为 10。

<a id="entry-12-6-timeout-client"></a>

**`timeout client <timeout>`**

```haproxy
timeout client <timeout>
```

设置客户端侧的最大不活动时间。

<a id="entry-12-6-option-assume-rfc6587-ntf"></a>

**`option assume-rfc6587-ntf`**

```haproxy
option assume-rfc6587-ntf
```

强制 HAProxy 始终将传入的 TCP 日志流视为使用非透明帧格式。此选项简化了帧格式逻辑，并确保消息处理的一致性，尤其在处理格式不正确的起始字符时尤为有用。

<a id="entry-12-6-option-dont-parse-log"></a>

**`option dont-parse-log`**

```haproxy
option dont-parse-log
```

启用 HAProxy 以中继 syslog 消息，而不尝试解析和重构消息内容，适用于转发可能不符合传统格式的消息。此选项应与目标日志端点上的 format raw 设置配合使用，以确保原始消息内容得以保留。

<a id="entry-12-6-option-host"></a>

**`option host { replace | fill | keep | append }`**

```haproxy
option host { replace | fill | keep | append }
```

设置在日志转发段中，针对出站 rfc3164 或 rfc5424 消息的 syslog 主机名字段所应采用的主机策略。

      replace 若输入消息的主机名字段已包含值，则将其替换为发送方的源 IP 地址。
              若输入消息的主机名字段不包含值（即：输入 rfc5424 消息为 '-'，
              或 rfc3164/rfc5424 消息不合规），则使用发送方的源 IP 地址作为
              主机名字段。

      fill    若输入消息的主机名字段已包含值，则保留该值。
              若输入消息的主机名字段不包含值（即：输入 rfc5424 消息为 '-'，
              或 rfc3164/rfc5424 消息不合规），则使用发送方的源 IP 地址作为
              主机名字段。
              （此为默认值）

      keep    若输入消息的主机名字段已包含值，则保留该值。
              若输入消息的主机名字段不包含值，则将其设为 'localhost'
              （rfc3164）或 '-'（rfc5424）。

      append  若输入消息的主机名字段已包含值，则在其后附加一个逗号，后接发送
              方的 IP 地址。
              若输入消息的主机名字段不包含值，则使用发送方的源 IP 地址。

对于上述所有选项，若发送方的源 IP 地址不可用（例如：UNIX/ABNS 套接字），则结果策略为 "keep"。

请注意，此选项仅对 rfc3164 或 rfc5424 目标日志格式有效。其他日志格式下设置该选项将无明显效果。

## 12.7. 证书存储 {#section-12-7}

HAProxy 使用内部存储机制来加载和存储配置中使用的证书。
该存储可通过使用 "crt-store" 段进行配置。它允许配置证书定义以及应加载到其中的文件。证书定义必须在配置中其他位置使用之前先声明。

crt-store [`<name>`]

"crt-store" 接受一个可选的名称参数。若指定名称，则该存储中的每个证书必须使用 "@`<name>`/`<crt>`" 或 "@`<name>`/`<alias>`" 进行引用。

证书存储中的文件也可通过 CLI 动态更新。参见管理指南中 [第 9.3 节](/zh/docs/haproxy/statistics-and-monitoring/#section-9-3) 的 "set ssl cert"。

以下关键字在 "crt-store" 段中受支持：

- crt-base
- key-base
- load

<a id="entry-12-7-crt-base"></a>

**`crt-base <dir>`**

```haproxy
crt-base <dir>
```

指定在使用 "crt" 指令采用相对路径时获取 SSL 证书的默认目录。指定的绝对位置优先生效，并忽略 "crt-base"。在 crt-store 中使用时，全局段的 crt-base 将被忽略。

<a id="entry-12-7-key-base"></a>

**`key-base <dir>`**

```haproxy
key-base <dir>
```

指定在使用 "key" 指令采用相对路径时获取 SSL 私钥的默认目录。指定的绝对位置优先生效，并忽略 "key-base"。在 crt-store 中使用时，全局段的 key-base 将被忽略。

<a id="entry-12-7-load"></a>

**`load [crt <filename>] [param*]`**

```haproxy
load [crt <filename>] [param*]
```

在证书存储中加载 SSL 文件。参数列表请参见 “12.7.1. 加载选项”段

示例：

```text
crt-store
    load crt "site1.crt" key "site1.key" ocsp "site1.ocsp" alias "site1"
    load crt "site2.crt" key "site2.key"

frontend in2
    bind *:443 ssl crt "@/site1" crt "site2.crt"

crt-store web
    crt-base /etc/ssl/certs/
    key-base /etc/ssl/private/
    load crt "site3.crt" alias "site3"
    load crt "site4.crt" key "site4.key"

frontend in2
    bind *:443 ssl crt "@/site1" crt "site2.crt"  crt "@web/site3" crt "@web/site4.crt"
```

### 12.7.1. 加载选项 {#section-12-7-1}

在证书存储中加载 SSL 文件。load 关键字可接受多个参数，具体如下所示。这些关键字也可在 crt-list 中使用。

<a id="entry-12-7-1-crt"></a>

**`crt <filename>`**

```haproxy
crt <filename>
```

此参数为必填项，用于加载一个 PEM 文件，其中必须包含公开证书，也可包含中间证书和私钥。若该文件中未提供私钥，则可使用 "key" 关键字指定私钥。

<a id="entry-12-7-1-acme"></a>

**`acme <string>`**

```haproxy
acme <string>
```

此选项用于为指定证书配置 ACME 协议。此功能为实验性特性，需在全局段中包含 "expose-experimental-directives" 关键字。

在 crt-store 中使用 "acme" 关键字时，可无需磁盘上已存在的证书即启动。此时将使用临时密钥对，直至 ACME 证书生成。此行为仅适用于 crt-store，若未先声明 crt-store，仅通过 crt-list 行或 ssl-f-use 行无法实现相同效果。

另请参见 [第 12.8 节](/zh/docs/haproxy/other-sections/#section-12-8)（"ACME"）以及本段中的 "domains"。

<a id="entry-12-7-1-alias"></a>

**`alias <string>`**

```haproxy
alias <string>
```

可选参数。允许使用别名命名证书，以便在配置中通过该别名引用。在配置的其他位置调用别名时，必须以 @/ 为前缀。

<a id="entry-12-7-1-domains"></a>

**`domains <string>`**

```haproxy
domains <string>
```

配置用于 ACME 证书的域名列表。列表中的第一个域名将用作 CN。域名之间以逗号分隔。

另请参见 [第 12.8 节](/zh/docs/haproxy/other-sections/#section-12-8)（"ACME"）以及本段中的 "acme"。

示例：

```text
load crt "example.com.pem" acme LE domains "bar.example.com,foo.example.com"
```

<a id="entry-12-7-1-ips"></a>

**`ips <string>`**

```haproxy
ips <string>
```

配置将作为 IP SAN 包含在 ACME 证书中的 IP 地址列表。IP 地址以逗号分隔。

生成包含 IP 地址的证书可能需要使用 "shortlived" profile。

另请参见本节中的 [第 12.8 节](/zh/docs/haproxy/other-sections/#section-12-8)（"ACME"）、"acme" 及 "domains"。

示例：

```text
load crt "server.pem" acme LE ips "192.0.2.1,2001:db8::1"
```

<a id="entry-12-7-1-key"></a>

**`key <filename>`**

```haproxy
key <filename>
```

该参数为可选。加载以 PEM 格式编码的私钥。如果已通过 "crt" 定义了私钥，则将覆盖原有设置。

<a id="entry-12-7-1-ocsp"></a>

**`ocsp <filename>`**

```haproxy
ocsp <filename>
```

该参数为可选参数，用于加载以 DER 格式编码的 OCSP 响应。可通过 CLI 更新。

<a id="entry-12-7-1-issuer"></a>

**`issuer <filename>`**

```haproxy
issuer <filename>
```

此参数为可选。以 PEM 格式加载 OCSP 发行者证书。为确定 OCSP 响应适用于哪个证书，必须提供发行者证书。如果在 "crt" 文件中未找到发行者证书，可使用此参数从文件加载。

<a id="entry-12-7-1-sctl"></a>

**`sctl <filename>`**

```haproxy
sctl <filename>
```

此参数为可选。已启用对证书透明度（RFC6962）TLS 扩展的支持。
文件必须包含符合 RFC 描述的有效签名证书时间戳列表。文件将被解析以检查基本语法，但不会验证签名。

<a id="entry-12-7-1-ocsp-update"></a>

**`ocsp-update [ off | on ]`**

```haproxy
ocsp-update [ off | on ]
```

当设置为 'on' 时，启用自动 OCSP 响应更新；否则，禁用该功能。其默认值为 'off'。可在 bind 语句中通过 crt-store 配置或使用全局选项 "tune.ocsp-update.mode" 来启用 OCSP 自动更新。若某个证书在多个 crt-list 中使用，且这些列表中 'ocsp-update' 的设置值不同，则会引发错误。同理，若证书在 bind 语句中继承全局选项，但在 crt-list 中显式设置了不兼容的 'ocsp-update' 选项，同样会引发错误。

示例：

以下是使用 crt-list 启用该功能的配置示例：

haproxy.cfg:

```text
frontend fe
    bind :443 ssl crt-list haproxy.list
```

haproxy.list:

```text
server_cert.pem [ocsp-update on] foo.bar
```

以下是使用 crt-store 启用该功能的配置示例：

haproxy.cfg:

```text
crt-store
  load crt foobar.pem ocsp-update on

frontend fe
    bind :443 ssl crt foobar.pem
```

当该选项设置为 'on' 时，若在前端证书中发现 OCSP URI，系统将尝试获取 OCSP 响应。此模式的唯一限制是，必须已知证书颁发者信息，才能构建 OCSP certid。每个 OCSP 响应至少每小时更新一次，若某 OCSP 响应的过期时间早于该一小时限制，则更新频率将更高。为避免对过期时间极短或根本无“Next Update”字段的响应进行过于频繁的更新，仍会保留最少 5 分钟的更新间隔。由于存在此硬性限制，请注意，当自动更新设置为 'on' 时，初始化期间加载的任何 OCSP 响应将在至少 5 分钟内不会被更新，即使其过期时间早于 now+5m。这通常不会造成太大困扰，因为 OCSP 响应在初始化加载时必须处于有效状态（其过期时间必须在将来），因此该响应在初始化后极短时间内过期的可能性极低。另一方面，若某证书指定了 OCSP URI 但未提供 OCSP 响应，将该证书的此选项设置为 'on'，可确保在初始化后立即自动获取 OCSP 响应。默认的最小和最大延迟（分别为 5 分钟和 1 小时）可通过 "ocsp-update.maxdelay" 和 "ocsp-update.mindelay" 全局选项进行配置。

每当 OCSP 响应由自动更新任务更新，或在调用 "update ssl ocsp-response" CLI 命令后，都会生成一条专用日志行。该日志行遵循专用格式，包含以下头信息 "`<OCSP-UPDATE>`"，后接特定的 OCSP 相关信息：- 对应前端证书的路径 - 数值型更新状态 - 文本型更新状态 - 该响应的更新失败次数 - 该响应的更新成功次数。有关完整的错误码和错误消息列表，请参见 "show ssl ocsp-updates" CLI 命令。无论相关 OCSP 响应更新成功或失败，均会发出此日志行。OCSP 请求/响应通过一个设置了 dontlog-normal 选项的 http_client 实例发送和接收，若发生错误（例如无法访问 OCSP 响应方），则使用常规 HTTP 日志格式。若发生此类错误，将伴随 "regular" OCSP 日志行，发出另一条包含 HTTP 相关信息的日志行（该日志行的文本状态很可能为 "HTTP error"）。但若发生纯粹的 HTTP 错误（例如无法访问 OCSP 响应方），则会额外发出一条遵循常规 HTTP 日志格式的日志行。以下是两条此类日志行的示例，首先为成功的 OCSP 更新日志行，随后为 HTTP 错误的示例，包含两条不同的日志行（为便于阅读，行已拆分，URL 已缩短）：

```text
<133>Mar  6 11:16:53 haproxy[14872]: <OCSP-UPDATE> /path_to_cert/foo.pem 1 \
        "Update successful" 0 1

<133>Mar  6 11:18:55 haproxy[14872]: <OCSP-UPDATE> /path_to_cert/bar.pem 2 \
        "HTTP error" 1 0
<133>Mar  6 11:18:55 haproxy[14872]: -:- [06/Mar/2023:11:18:52.200] \
        <OCSP-UPDATE> -/- 2/0/-1/-1/3009 503 217 - - SC-- 0/0/0/0/3 0/0 {} \
        "GET http://127.0.0.1:12345/MEMwQT HTTP/1.1"
```

故障排查：使用 Let's Encrypt 证书时常见的错误是：DNS 解析返回 IPv6 地址，而系统没有有效的出站 IPv6 路由。在此情况下，可以创建相应的路由，或在全局段中设置 "httpclient.resolvers.prefer ipv4" 选项。若出现 "OCSP response check failure" 错误，应检查所提供的颁发者证书是否有效。在 "generic" 错误消息之后，括号内可能还会显示更精确的错误信息。该情况可能出现在 "OCSP response check failure" 或 "Error during insertion" 错误中。

<a id="entry-12-7-1-jwt"></a>

**`jwt [ off | on ]`**

```haproxy
jwt [ off | on ]
```

允许通过 "jwt_verify_cert"、"jwt_decrypt_cert" 或 "jwt_decrypt" 转换器在设置为 'on' 时，使用该证书进行 JWT 验证或解密。其默认值为 'off'。

当为某个证书设置 'on' 时，CLI 命令 "del ssl cert" 将无法执行。要删除证书，该证书必须未被使用，无论是用于 SSL 握手还是 JWT 验证。

此选项可通过 CLI 命令 "add ssl jwt" 和 "del ssl jwt" 在运行时更改。另请参见 "show ssl jwt" CLI 命令。

<a id="entry-12-7-1-generate-dummy"></a>

**`generate-dummy [ off | on ]`**

```haproxy
generate-dummy [ off | on ]
```

在设置为 'on' 时，允许在解析时生成私钥及其自签名证书。这在测试阶段未持有证书时可能有用。此时，可使用 "keytype"、"bits" 和 "curves" 自定义私钥。未使用时，默认值为 'off'。（另见 "keytype"、"bits" 和 "curves"）。

<a id="entry-12-7-1-keytype"></a>

**`keytype [ RSA | ECDSA ]`**

```haproxy
keytype [ RSA | ECDSA ]
```

允许在解析时选择用于生成自签名证书的私钥类型。当此证书的 "generate-dummy" 设置为 'on' 时，即为这种情况。未使用时，默认值为 'RSA'。（另请参见 "generate-dummy"）。

<a id="entry-12-7-1-bits"></a>

**`bits <number>`**

```haproxy
bits <number>
```

配置当 "generate-dummy" 设置为 'on' 且 "keytype" 设置为 'RSA' 时生成 RSA 自签名证书的位数。未使用时，默认值为 2048。（另请参见 "generate-dummy"）。

<a id="entry-12-7-1-curves"></a>

**`curves <string>`**

```haproxy
curves <string>
```

当 "generate-dummy" 设置为 'on' 且 "keytype" 设置为 'ECDSA' 时，配置此自签名证书的曲线。默认值为 'P-384'。

## 12.8. ACME {#section-12-8}

acme `<name>`

ACME 协议可通过 "acme" 段进行配置。该段需指定一个 "`<name>`" 参数，用于将证书与该段关联。

本节允许将 HAProxy 配置为 ACMEv2 客户端。此功能为实验性，因此 "expose-experimental-directives" 必须位于 global 段中，方可使用。

HAProxy 官方 wiki 上提供了相关指南：
<https://github.com/haproxy/wiki/wiki/ACME:--native-haproxy>

当前限制：<a id="entry-12-8-the-feature-is"></a>

**`- 此功能仅支持 http-01、dns-01 或 dns-persist-01 验证`**

```haproxy
- 此功能仅支持 http-01、dns-01 或 dns-persist-01 验证
```

目前，http-01 完全由 HAProxy 处理，但 dns-01 和 dns-persist-01 需要通过 dataplaneAPI 或其他第三方工具与 DNS 提供商 API 通信。dns-persist-01 仅需设置一次 TXT 记录，因此可手动设置而无需使用工具。
<a id="entry-12-8-it-is-possible"></a>

**`- 可以在磁盘上没有现有证书的情况下启动。为此`**

```haproxy
- 可以在磁盘上没有现有证书的情况下启动。为此
```

因此，证书必须配置在 crt-store 中。在 crt-store 中使用 "acme" 关键字时，将在 ACME 证书生成前临时使用一对密钥。
<a id="entry-12-8-the-current-haproxy"></a>

**`- HAProxy 当前采用非阻塞架构，访问磁盘`**

```haproxy
- HAProxy 当前采用非阻塞架构，访问磁盘
```

在配置加载后不应执行此操作，因为这可能导致事件循环被阻塞，从而阻塞同一线程上的流量。这意味着由 HAProxy 生成的证书和密钥需通过统计信息套接字上的 "dump ssl cert" 命令从 HAProxy 外部转储。可以使用 dataplaneAPI 或 admin/cli/ 目录中提供的 haproxy-dump-certs 脚本自动化证书转储。

ACME 调度器在 HAProxy 启动时启动，它将遍历所有证书，并在 notAfter 时间超过当前时间加上 (notAfter - notBefore) / 12 或 7 天（若 notBefore 未定义）时，启动 ACME 证书续期任务。调度器随后将休眠，并在 12 小时后唤醒。可以使用命令 "acme renew" 手动启动续期任务。详见管理指南中的 "acme status"。

以下关键字可在 ACME 段中使用：

<a id="entry-12-8-account-key"></a>

**`account-key <filename>`**

```haproxy
account-key <filename>
```

配置账户密钥的路径。在启动 HAProxy 之前，必须先生成密钥。若未使用 account 关键字，acme 段将尝试使用文件名 "`<name>`.account.key" 加载文件。如果该文件不存在，HAProxy 将根据 acme 段中的参数生成一个密钥。

也可以使用 OpenSSL 手动生成 RSA 私钥：

```text
openssl genrsa -out account.key 2048
```

或一个 ecdsa 类型的：

```text
openssl ecparam -name secp384r1 -genkey -noout -out account.key
```

<a id="entry-12-8-acme-vars"></a>

**`acme-vars <string>`**

```haproxy
acme-vars <string>
```

通过 "dpapi" 接收端（sink）向外部 DNS 配置工具（例如 dataplaneAPI）传递任意变量。语义由工具具体决定；请参阅所用 DNS 配置工具文档。

该关键字仅在挑战类型为 "dns-01" 或 "dns-persist-01" 时才有意义。

另请参阅："challenge"、"provider-name"

<a id="entry-12-8-bits"></a>

**`bits <number>`**

```haproxy
bits <number>
```

配置生成 RSA 证书时使用的位数。默认值为 2048。若机器性能不足，设置过高的值可能触发警告。（此值可通过 "warn-blocked-traffic-after" 配置，但过长的阻断时间可能触发看门狗机制。）

<a id="entry-12-8-challenge"></a>

**`challenge <string>`**

```haproxy
challenge <string>
```

指定一个挑战类型作为参数，必须为 http-01、dns-01 或 dns-persist-01。若未使用，则默认为 http-01。

dns-persist-01 实现了 draft-ietf-acme-dns-persist。与 dns-01 不同，它在 "\_validation-persist.`<domain>`" 处使用一个静态 TXT 记录，该记录仅设置一次，后续续订过程中不会更改。该记录必须包含账户 URI，以及一个可选的策略。此挑战类型在每次续订时无需对 DNS 提供商 API 进行写入访问。

<a id="entry-12-8-challenge-ready"></a>

**`challenge-ready <value>[,<value>]*`**

```haproxy
challenge-ready <value>[,<value>]*
```

配置在通知 ACME 服务器 dns-01 挑战已就绪、可被验证之前必须满足的条件。接受的取值如下：

```text
cli  - 等待操作者在主进程 CLI 或统计信息套接字上执行
       "acme challenge_ready <crt> domain <domain>" CLI 命令来通知已就绪。
       这样，外部 DNS 配置工具可在 HAProxy 继续处理之前确认 TXT 记录已设置。

dns  - 使用配置的 "default" resolvers 段解析 "_acme-challenge.<domain>" 的 TXT 记录，
       进行 DNS 预检查，而非查询权威名称服务器。仅当 TXT 记录与预期令牌匹配时才提交验证。
       因此结果可能受到解析器级别的 DNS 缓存影响。解析尝试之间的延迟由 "dns-delay" 控制。
       此选项独立于 CLI 命令，不需要人工介入。

       对于 dns-01，解析 "_acme-challenge.<domain>" 的 TXT 记录，且其内容必须与预期令牌匹配。
       对于 dns-persist-01，解析 "_validation-persist.<domain>" 的 TXT 记录，仅检查其是否存在。

delay - 在继续处理之前先等待 "dns-delay" 指定的时间。
        未使用 "dns" 时，延迟结束后提交验证。
        与 "dns" 组合时，在开始 DNS 预检查之前先等待这段时间。

none - 不设置就绪条件；不等待任何外部确认，立即向 ACME 服务器提交验证。
       此选项不能与其他选项组合使用。
```

多个值可使用逗号组合。当指定多个条件时，HAProxy 按以下顺序处理：首先等待 CLI 确认（"cli"），然后应用初始延迟（"delay"），最后执行 DNS 预检查（"dns"）。

此选项仅与 dns-01 和 dns-persist-01 挑战类型兼容。

当 "challenge" 设置为 "dns-01" 且未配置此选项时，默认值为 "cli"。

当 "challenge" 设置为 "dns-persist-01" 且未配置此选项时，默认值为 "dns,delay"。

当 "challenge" 设置为 "dns-persist-01" 时，将在评估 challenge-ready 条件之前始终执行一次初始的机会性 DNS 检查。由于 "\_validation-persist.`<domain>`" TXT 记录在续订期间仅设置一次且不会更改，HAProxy 会在续订时检查该记录是否已存在。如果所有域名的检查均成功，挑战将立即提交，跳过 challenge-ready 流程（cli、delay、dns）。如果检查失败，HAProxy 将回退到正常的 challenge-ready 流程。

示例：

```shell
# Wait for CLI confirmation, then verify DNS propagation
challenge-ready cli,dns
```

<a id="entry-12-8-contact"></a>

**`contact <string>`**

```haproxy
contact <string>
```

与证书颁发机构（CA）中的账户密钥相关联的联系邮箱。

<a id="entry-12-8-curves"></a>

**`curves <string>`**

```haproxy
curves <string>
```

使用 ECDSA 密钥类型时，用于配置曲线。默认值为 P-384。

<a id="entry-12-8-directory"></a>

**`directory <string>`**

```haproxy
directory <string>
```

该关键字用于配置本 acme 段所使用 CA 的目录 URL。由于不存在默认 URL，此关键字为必填项。

示例：

```text
directory https://acme-staging-v02.api.letsencrypt.org/directory
```

<a id="entry-12-8-dns-delay"></a>

**`dns-delay <time>`**

```haproxy
dns-delay <time>
```

配置 "challenge-ready" 条件 "delay" 和 "dns" 所使用的延迟时间。该值为以 HAProxy 时间格式表示的时间（例如 "5m"、"300s"）。默认值为 30 秒。

其作用取决于所使用的 "challenge-ready" 条件：

```text
delay     - 延迟结束后提交验证，不进行任何 DNS 预检查。

dns       - 两次连续 DNS 解析尝试之间的延迟。首次探测立即执行，不进行初始等待。

dns+delay - 首次 DNS 解析尝试之前的初始等待，以及后续重试之间的延迟。
```

请注意，解析过程通过配置的 "default" 解析器段进行，而非权威域名服务器。因此，结果仍可能受解析器层级 DNS 缓存的影响。

<a id="entry-12-8-dns-timeout"></a>

**`dns-timeout <time>`**

```haproxy
dns-timeout <time>
```

当 "challenge-ready" 包含 "dns" 时，配置在中止挑战前允许成功解析 TXT 记录的最大时间。该值为以 HAProxy 时间格式表示的时间（例如 "10m"、"600s"）。默认值为 600 秒。

超时从首次 DNS 解析尝试触发时开始计算（在初始 "dns-delay" 之后）。若下一次解析尝试将在超时结束后才触发，则挑战将因错误而中止。此机制可防止 DNS 传播失败时出现无限重试循环。

参见："dns-delay"

<a id="entry-12-8-keytype"></a>

**`keytype <string>`**

```haproxy
keytype <string>
```

配置将生成的密钥类型。值可以是 "RSA" 或 "ECDSA"。还可以为 ECDSA 配置 "curves"，并为 RSA 配置 "bits"。默认情况下生成 EC384 密钥。

<a id="entry-12-8-map"></a>

**`map <map>`**

```haproxy
map <map>
```

配置用于存储令牌（键）和指纹（值）的映射，该映射在使用多个账户时有助于响应挑战。ACME 任务将在验证挑战前添加条目，并在任务结束时移除这些条目。

<a id="entry-12-8-profile"></a>

**`profile <string>`**

```haproxy
profile <string>
```

通过在 newOrder 请求中包含 "profile" 字段，向证书颁发机构（CA）请求特定的证书配置文件。此功能实现 draft-ietf-acme-profiles 规范。

profile 名称是因 CA 而异的短标识符（例如 "classic"、"shortlived"）。设置后，profile 名称将在 newOrder JSON 负载中原样发送。若不支持该 profile，CA 可选择忽略请求或返回错误。未设置时，不包含 profile 字段，CA 将使用其默认颁发策略。

请参阅 <https://letsencrypt.org/docs/profiles/> 了解 Let's Encrypt 配置文件。

示例：

```shell
# Request short-lived certificates
profile shortlived
```

<a id="entry-12-8-provider-name"></a>

**`provider-name <string>`**

```haproxy
provider-name <string>
```

通过 "dpapi" 接收端向外部 DNS 配置工具（例如 dataplaneAPI）传递 DNS 服务商名称。可接受的值因工具而异；请参阅所用 DNS 配置工具文档。

该关键字仅在挑战类型为 "dns-01" 或 "dns-persist-01" 时才有意义。

另请参阅："challenge"、"acme-vars"

<a id="entry-12-8-reuse-key"></a>

**`reuse-key { on | off }`**

```haproxy
reuse-key { on | off }
```

若设置为 "on"，HAProxy 将不会生成新的私钥，而是保留之前的私钥。启用此选项时，建议定期手动重新生成密钥，以实现私钥轮换。

当使用大于 2048 位的 RSA 密钥时，该选项可能有用，因为生成这些密钥可能耗时较长，且可能拖慢执行该操作的单个线程。

在使用 ACME 服务器的缓存时，复用同一密钥可能很有用，它有助于获取与当前密钥对应的有效证书。

默认设置为 "off"。

示例：

```text
global
    expose-experimental-directives
    httpclient.resolvers.prefer ipv4

frontend in
    bind *:80
    bind *:443 ssl
    http-request return status 200 content-type text/plain lf-string "%[path,field(-1,/)].%[path,field(-1,/),map(virt@acme)]\n" if { path_beg '/.well-known/acme-challenge/' }
    ssl-f-use crt "foo.example.com.pem.rsa"   acme LE1 domains "foo.example.com.pem,bar.example.com"
    ssl-f-use crt "foo.example.com.pem.ecdsa" acme LE2 domains "foo.example.com.pem,bar.example.com"

acme LE1
    directory https://acme-staging-v02.api.letsencrypt.org/directory
    account-key /etc/haproxy/letsencrypt.account.key
    contact john.doe@example.com
    challenge http-01
    keytype RSA
    bits 2048
    map virt@acme

acme LE2
    directory https://acme-staging-v02.api.letsencrypt.org/directory
    account-key /etc/haproxy/letsencrypt.account.key
    contact john.doe@example.com
    challenge http-01
    keytype ECDSA
    curves P-384
    map virt@acme
```

<a id="entry-12-8-eab-key-id"></a>

**`eab-key-id <filename>`**

```haproxy
eab-key-id <filename>
```

配置 EAB 密钥 ID 文件的路径。凭据由证书颁发机构（CA）提供，必须在启动 HAProxy 之前放置于指定路径。该凭据仅在账户创建时使用。

该文件必须包含一个纯 ASCII 字符串。

EAB 凭据仅在初始 ACME 账户创建期间需要，之后可从配置中移除，或通过清空文件移除。空文件将被静默忽略。空白字符不被忽略，除非是末尾的换行符。

另请参阅："eab-mac-key"、"eab-mac-alg"

<a id="entry-12-8-eab-mac-key"></a>

**`eab-mac-key <filename>`**

```haproxy
eab-mac-key <filename>
```

配置 EAB MAC 密钥文件的路径。凭据由 CA 提供，必须在启动 HAProxy 之前放置于指定路径。该凭据仅在账户创建时使用。

文件必须包含一个经过 base64url 编码的 MAC 密钥。

EAB 凭据仅在初始 ACME 账户创建期间需要，之后可从配置中移除，或通过清空文件移除。空文件将被静默忽略。空白字符不被忽略，除非是末尾的换行符。

另请参阅："eab-key-id"、"eab-mac-alg"

<a id="entry-12-8-eab-mac-alg"></a>

**`eab-mac-alg { HS256 | HS384 | HS512 }`**

```haproxy
eab-mac-alg { HS256 | HS384 | HS512 }
```

配置用于 EAB 签名的 MAC 算法。默认值为 HS256。EAB MAC 密钥必须足够大以支持指定的 MAC 算法。并非所有 CA 均支持 HS256 以外的算法。

另请参阅："eab-key-id"、"eab-mac-key"

## 12.9. 健康检查 {#section-12-9}

可以全局声明多个健康检查，这些健康检查可在整个配置中由所有服务器使用，从而覆盖本地代理配置。

<a id="entry-12-9-healthcheck"></a>

**`healthcheck <name>`**

```haproxy
healthcheck <name>
```

创建一个名为 `<name>` 的新健康检查。该名称必须唯一。应在服务器行中使用此名称来引用特定的健康检查段。

<a id="entry-12-9-type"></a>

**`type <type>`**

```haproxy
type <type>
```

定义健康检查类型。此参数为必填项。支持以下类型的健康检查：

    * tcp-check
    * httpchk
    * ssl-hello-chk
    * smtpchk
    * pgsql-check
    * redis-check
    * mysql-check
    * ldap-check
    * spop-check

每种类型使用的参数（如有）与对应代理的选项相同。例如，可为 "httpchk" 类型指定方法、URI 等：

示例：

```text
   healthcheck my-http-check
type httpchk GET /health HTTP/1.1 %[srv_name]
```

另请参阅：`option tcp-check`、`option httpchk`、`option ssl-hello-chk`、`option smtpchk`、`option mysql-check`、`option pgsql-check`、`option redis-check`、`option ldap-check` 和 `option spop-check`

<a id="entry-12-9-http-check-comment"></a>

**`http-check comment <string>`**

```haproxy
http-check comment <string>
http-check connect [default] [port <expr>] [addr <ip>] [send-proxy]
                   [via-socks4] [ssl] [sni <sni>] [alpn <alpn>] [linger]
                   [proto <name>] [comment <msg>]
http-check disable-on-404
http-check expect [min-recv <int>] [comment <msg>]
                  [ok-status <st>] [error-status <st>] [tout-status <st>]
                  [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                  [!] <match> <pattern>
http-check send [meth <method>] [{ uri <uri> | uri-lf <fmt> }>] [ver <version>]
                [hdr <name> <fmt>]* [{ body <string> | body-lf <fmt> }]
                [comment <msg>]
http-check send-state
http-check set-var(<var-name>[,<cond>...]) <expr>
http-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
http-check unset-var(<var-name>)
```

为 "httpchk" 健康检查添加特定的 http-check 规则。使用与对应代理指令相同的语法。详情请参阅相应代理的文档。

<a id="entry-12-9-tcp-check-comment"></a>

**`tcp-check comment <string>`**

```haproxy
tcp-check comment <string>
tcp-check connect [default] [port <expr>] [addr <ip>] [send-proxy] [via-socks4]
                  [ssl] [sni <sni>] [alpn <alpn>] [linger]
                  [proto <name>] [comment <msg>]
tcp-check expect [min-recv <int>] [comment <msg>]
                 [ok-status <st>] [error-status <st>] [tout-status <st>]
                 [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                 [!] <match> <pattern>
tcp-check send <data> [comment <msg>]
tcp-check send-lf <fmt> [comment <msg>]
tcp-check send-binary <hexstring> [comment <msg>]
tcp-check send-binary-lf <hexfmt> [comment <msg>]
tcp-check set-var(<var-name>[,<cond>...]) <expr>
tcp-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
tcp-check unset-var(<var-name>)
```

为 "tcp-check" 健康检查添加特定的 tcp-check 规则。使用与对应代理指令相同的语法。详情请参阅对应代理的文档。
