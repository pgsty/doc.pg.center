---
title: "10. FastCGI 应用程序"
linkTitle: "10. FastCGI"
weight: 210
description: "FastCGI 应用配置、参数、示例及限制"
icon: fa-solid fa-bolt
module: [HAPROXY]
categories: [参考]
aliases:
  - /haproxy/configuration/fastcgi/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 10"
---

HAProxy 可以向 Responder FastCGI 应用发送 HTTP 请求。此功能自 HAProxy 2.1 版本起引入。为此，必须将服务器配置为使用 FastCGI 协议（在服务器行中使用关键字 "proto fcgi"），且后端管理这些服务器时，必须配置并使用一个 FastCGI 应用（在代理段中使用关键字 "use-fcgi-app"）。可以定义多个 FastCGI 应用，但每个后端在同一时间只能使用其中一个。

HAProxy 实现了 FastCGI 规范中针对 Responder 应用的所有功能。特别是，它能够在单一连接上复用多个请求。

## 10.1. 配置 {#section-10-1}



### 10.1.1. fcgi-app 段 {#section-10-1-1}

<a id="entry-10-1-1-fcgi-app"></a>

**`fcgi-app <name>`**

```haproxy
fcgi-app <name>
```

声明一个名为 `<name>` 的 FastCGI 应用。要使配置有效，至少必须定义文档根目录。

<a id="entry-10-1-1-acl"></a>

**`acl <aclname> <criterion> [flags] [operator] <value> ...`**

```haproxy
acl <aclname> <criterion> [flags] [operator] <value> ...
```

声明或完成访问控制列表。

请参阅 [第 4.2 节](/zh/haproxy/proxies/#section-4-2) 中的 "acl" 关键字以及 [第 7 节](/zh/haproxy/acls-and-samples/) 的 ACL 使用说明了解详情。为 FastCGI 应用定义的 ACL 为私有，无法被任何其他应用或代理使用。同理，任何其他段中定义的 ACL 也无法被 FastCGI 应用使用。但预定义的 ACL 可用。

<a id="entry-10-1-1-docroot"></a>

**`docroot <path>`**

```haproxy
docroot <path>
```

定义远程主机上的文档根目录。`<path>` 将用于构建 FastCGI 参数 SCRIPT_FILENAME 和 PATH_TRANSLATED 的默认值。此项为必选设置。

<a id="entry-10-1-1-index"></a>

**`index <script-name>`**

```haproxy
index <script-name>
```

定义在以斜杠 ("/") 结尾的 URI 后附加的脚本名称，用于设置 FastCGI 参数 SCRIPT_NAME 的默认值。此项为可选设置。

示例：

```text
index index.php
```

<a id="entry-10-1-1-log-stderr-global"></a>

**`log-stderr global`**

```haproxy
log-stderr global
log-stderr <target> [len <length>] [format <format>]
    [sample <ranges>:<sample_size>] <facility> [<level> [<minlevel>]]
```

启用记录 FastCGI 应用程序报告的 STDERR 消息。

请参阅 [第 4.2 节](/zh/haproxy/proxies/#section-4-2) 中的 "log" 关键字了解详情。该设置为可选。默认情况下，忽略 STDERR 消息。

<a id="entry-10-1-1-pass-header"></a>

**`pass-header <name> [ { if | unless } <condition> ]`**

```haproxy
pass-header <name> [ { if | unless } <condition> ]
```

指定将传递给 FastCGI 应用程序的请求头名称。可选地，其后可跟一个基于 ACL 的条件，此时仅当该条件为真时才进行评估。

大多数请求头已可供 FastCGI 应用程序使用，且均以 "HTTP\_" 为前缀。因此，该指令仅用于传递那些被有意省略的头。当前，头 "Authorization"、"Proxy-Authorization" 以及逐跳头被省略。

请注意，头 "Content-type" 和 "Content-length" 永远不会传递给 FastCGI 应用程序，因为它们已转换为参数。

<a id="entry-10-1-1-path-info"></a>

**`path-info <regex>`**

```haproxy
path-info <regex>
```

定义一个正则表达式，用于从 URL 解码后的路径中提取脚本名和路径信息。
因此，`<regex>` 可能包含两个捕获：第一个用于捕获脚本名，第二个用于捕获路径信息。第一个捕获为必选，第二个为可选。通过这种方式，可以从路径中提取脚本名，同时忽略路径信息。此设置为可选。若未定义，则不对路径执行匹配，且 FastCGI 参数 PATH_INFO 和 PATH_TRANSLATED 不会被填充。

出于安全考虑，当定义了此正则表达式时，路径在经过 URL 解码后禁止包含换行符和空字符。此限制的原因在于，否则匹配将始终失败（由于 HAProxy 中正则表达式执行方式的限制）。因此，若在 URL 解码后的路径中发现这两个字符之一，将向客户端返回错误。此处遵循最小惊讶原则。

示例：

```text
path-info ^(/.+\.php)(/.*)?$ # both script-name and path-info may be set
path-info ^(/.+\.php)        # the path-info is ignored
```

<a id="entry-10-1-1-option-get-values"></a>

**`option get-values`**

```haproxy
option get-values
no option get-values
```

启用或禁用获取连接管理相关变量。

HAProxy 可在建立连接时发送记录 FCGI_GET_VALUES，以获取以下变量的值：

    * FCGI_MAX_REQS     此应用程序将接受的最大并发请求数。

    * FCGI_MPXS_CONNS   若此应用程序不对连接进行多路复用，则为
                        "0"；否则为 "1"。

部分 FastCGI 应用程序不支持此功能。部分应用程序在发送响应后立即关闭连接。因此，默认情况下，此选项处于禁用状态。

请注意，FastCGI 应用程序接受的最大并发请求数是一个连接级变量。它仅限制每个连接的流数量。若需对应用的全局负载进行限制，必须设置服务器参数 "maxconn" 和 "pool-max-conn"。此外，若应用不支持连接多路复用，则最大并发请求数将自动设为 1。

<a id="entry-10-1-1-option-keep-conn"></a>

**`option keep-conn`**

```haproxy
option keep-conn
no option keep-conn
```

指示 FastCGI 应用程序在发送响应后是否保持连接打开。

若禁用，FastCGI 应用程序在响应此请求后关闭连接。默认情况下，此选项已启用。

<a id="entry-10-1-1-option-max-reqs"></a>

**`option max-reqs <reqs>`**

```haproxy
option max-reqs <reqs>
```

定义该应用程序将接受的最大并发请求数。

该选项可在连接建立期间获取变量 FCGI_MAX_REQS 时被覆盖。此外，若应用程序不支持连接复用，该选项将被忽略。默认值为 1。

<a id="entry-10-1-1-option-mpxs-conns"></a>

**`option mpxs-conns`**

```haproxy
option mpxs-conns
no option mpxs-conns
```

启用或禁用连接复用支持。

该选项可在连接建立期间获取变量 FCGI_MPXS_CONNS 时被覆盖。默认情况下已禁用。

<a id="entry-10-1-1-set-param"></a>

**`set-param <name> <fmt> [ { if | unless } <condition> ]`**

```haproxy
set-param <name> <fmt> [ { if | unless } <condition> ]
```

设置应传递给该应用的 FastCGI 参数。其值由 `<fmt>` 定义，必须遵循自定义日志格式规则（参见 [第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6) “自定义日志格式”）。可选地，其后可跟一个基于 ACL 的条件，此时仅当该条件为真时才进行评估。

使用该指令，可以覆盖默认 FastCGI 参数的值。若值被计算为空字符串，则忽略该规则。这些指令按声明顺序进行评估。

示例：

```shell
# PHP only, required if PHP was built with --enable-force-cgi-redirect
set-param REDIRECT_STATUS 200

set-param PHP_AUTH_DIGEST %[req.hdr(Authorization)]
```

### 10.1.2. 代理段 {#section-10-1-2}

use-fcgi-app `<name>` 为后端指定要使用的 FastCGI 应用。

参数：

```text
<name>    是要使用的 FastCGI 应用程序的名称。
```

该关键字仅适用于具备后端功能且至少包含一个 FastCGI 服务器的 HTTP 代理。尽管 FastCGI 服务器可与 HTTP 服务器混合使用，但除非有充分理由，否则不建议如此操作（详见 [第 10.3 节](/zh/haproxy/fastcgi/#section-10-3) 中关于限制的详细说明）。每个后端在同一时间只能定义一个应用程序。

请注意，一旦后端引用了 FastCGI 应用，根据配置情况，即使请求未发送至 FastCGI 服务器，也可能执行部分处理。用于设置参数或向应用传递头的规则将被评估。

### 10.1.3. 示例 {#section-10-1-3}

```haproxy
frontend front-http
    mode http
    bind *:80

    use_backend back-dynamic if { path_reg ^/.+\.php(/.*)?$ }
    default_backend back-static

backend back-static
    mode http
    server www A.B.C.D:80

backend back-dynamic
    mode http
    use-fcgi-app php-fpm
    server php-fpm A.B.C.D:9000 proto fcgi

fcgi-app php-fpm
    log-stderr global
    option keep-conn

    docroot /var/www/my-app
    index index.php
    path-info ^(/.+\.php)(/.*)?$
```

## 10.2. 默认参数 {#section-10-2}

Responder FastCGI 应用程序的目的与 CGI/1.1 程序相同。在 CGI/1.1 规范（RFC3875）中，必须向脚本传递若干变量。因此，HAProxy 会设置这些变量以及 FastCGI 应用常用的其他一些变量。所有这些变量均可被覆盖，但需谨慎操作。

```text
  +-------------------+-----------------------------------------------------+
  | AUTH_TYPE         | 表示 HAProxy 用于认证用户的机制（若有）。              |
  |                   | 目前仅支持 BASIC 认证机制。                         |
  +-------------------+-----------------------------------------------------+
  | CONTENT_LENGTH    | 包含请求所附消息体的大小。仅已知大小的请求被视为有效， |
  |                   | 并发送给应用程序。                                  |
  +-------------------+-----------------------------------------------------+
  | CONTENT_TYPE      | 包含请求所附消息体的类型。此参数可能未设置。           |
  +-------------------+-----------------------------------------------------+
  | DOCUMENT_ROOT     | 包含远程主机上执行脚本所在的文档根目录，              |
  |                   | 由应用程序的配置定义。                              |
  +-------------------+-----------------------------------------------------+
  | GATEWAY_INTERFACE | 包含 HAProxy 与 FastCGI 应用程序通信所用的 CGI 方言。 |
  |                   | 具体设置为 "CGI/1.1"。                              |
  +-------------------+-----------------------------------------------------+
  | PATH_INFO         | 包含 URI 路径中标识脚本本身的部分之后的路径层级。     |
  |                   | 必须定义 "path-info" 指令才能设置此参数。            |
  +-------------------+-----------------------------------------------------+
  | PATH_TRANSLATED   | 若设置了 PATH_INFO，则为其转换后的版本，              |
  |                   | 由 DOCUMENT_ROOT 与 PATH_INFO 拼接而成。            |
  |                   | 若未设置 PATH_INFO，此参数也不设置。                 |
  +-------------------+-----------------------------------------------------+
  | QUERY_STRING      | 包含请求的查询字符串。此参数可能未设置。              |
  +-------------------+-----------------------------------------------------+
  | REMOTE_ADDR       | 包含发送请求的客户端的网络地址。                    |
  +-------------------+-----------------------------------------------------+
  | REMOTE_USER       | 包含客户端在用户认证过程中提供的用户标识字符串。     |
  +-------------------+-----------------------------------------------------+
  | REQUEST_METHOD    | 包含脚本处理请求时应使用的方法。                    |
  +-------------------+-----------------------------------------------------+
  | REQUEST_URI       | 包含请求的 URI。                                   |
  +-------------------+-----------------------------------------------------+
  | SCRIPT_FILENAME   | 包含脚本的绝对路径名，                              |
  |                   | 由 DOCUMENT_ROOT 与 SCRIPT_NAME 拼接而成。          |
  +-------------------+-----------------------------------------------------+
  | SCRIPT_NAME       | 包含脚本名称。若定义 "path-info" 指令，则为 URI 路径 |
  |                   | 层级中的第一部分，截止到脚本名称；否则为整个 URI 路径。 |
  +-------------------+-----------------------------------------------------+
  | SERVER_NAME       | 包含客户端请求所指向的服务器主机名称。               |
  |                   | 若已定义 "Host" 头，则为该头的值；                  |
  |                   | 否则为客户端侧连接的目标地址。                      |
  +-------------------+-----------------------------------------------------+
  | SERVER_PORT       | 包含客户端侧连接的目标 TCP 端口，即客户端连接的端口。 |
  +-------------------+-----------------------------------------------------+
  | SERVER_PROTOCOL   | 包含请求所用的协议。                               |
  +-------------------+-----------------------------------------------------+
  | SERVER_SOFTWARE   | 包含字符串 "HAProxy" 及其后的当前 HAProxy 版本。      |
  +-------------------+-----------------------------------------------------+
  | HTTPS             | 若通过 HTTPS 协议请求脚本，则设置为非空值（"on"）。  |
  +-------------------+-----------------------------------------------------+
```

## 10.3. 限制 {#section-10-3}

当前实现存在一些限制。第一个限制涉及某些请求头在传递给 FastCGI 应用程序时的隐藏方式。这一过程发生在后端侧的请求头分析阶段，即在连接建立之前。此时，HAProxy 知道后端使用的是 FastCGI 应用程序，但尚无法确定该请求是否将被路由至 FastCGI 服务器。为隐藏请求头，HAProxy 会直接从 HTX 消息中移除这些头。因此，若请求最终被路由至 HTTP 服务器，该服务器将无法看到这些头。出于此原因，不建议在同一后端中混合使用 FastCGI 服务器和 HTTP 服务器。

同样地，规则 "set-param" 和 "pass-header" 在请求头分析阶段进行评估。因此，即使请求最终被转发至 HTTP 服务器，评估操作也始终执行。

关于规则 "set-param"，当应用规则时，会向 HTX 消息中添加一个伪头。
因此，与 HTTP 头重写类似，若缓冲区已满，操作可能失败。
规则 "set-param" 将与规则 "http-request" 竞争资源。

最后，所有 FastCGI 参数和 HTTP 头均被发送到同一条 FCGI_PARAM 记录中。该记录的编码必须一次性完成，否则将返回处理错误。这意味着记录 FCGI_PARAM 在编码后，其大小不得超过缓冲区容量。但此处无需预留空间。
