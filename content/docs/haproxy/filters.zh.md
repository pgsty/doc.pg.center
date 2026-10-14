---
title: "9. 支持的过滤器"
linkTitle: "9. 过滤器"
weight: 200
description: "跟踪、压缩、SPOE、缓存、FastCGI、OpenTracing 以及带宽过滤器"
icon: fa-solid fa-layer-group
module: [HAPROXY]
categories: [参考]
aliases:
  - /haproxy/configuration/filters/
  - /docs/haproxy/configuration/filters/
  - /haproxy/filters/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 9"
---

以下是官方支持的过滤器及其所接受的参数列表。根据编译选项的不同，部分过滤器可能不可用。可用过滤器列表会在 haproxy -vv 中报告。

另请参见："filter"

## 9.1. 跟踪 {#section-9-1}

filter trace [name `<name>`] [random-forwarding] [max-fwd `<max>`] [hexdump]

参数：

```text
<name>               是在消息中报告的任意名称。未提供名称时使用 "TRACE"。

<quiet>              禁止输出跟踪消息。

<random-forwarding>  启用已解析数据的随机转发。默认情况下，此过滤器转发此前已解析的全部数据；
                     使用此参数时，仅转发其中随机数量的数据。

<max>                是每次可转发的最大数据量。"max-fwd" 选项可与随机转发组合使用。
                     <max> 必须为正整数。0 表示不限制。

<hexdump>             转储转发给服务器和客户端的全部数据。
```

此过滤器可作为开发新过滤器的基础。它定义了所有回调函数，并在标准错误流（stderr）中输出有用信息，供所有回调函数参考。该过滤器可用于调试其他过滤器的活动，或简单地用于排查 HAProxy 的运行状态。

使用 `<random-parsing>` 和/或 `<random-forwarding>` 参数是测试过滤器行为的有效方法，该过滤器用于解析客户端与服务器之间交换的数据，并通过在处理过程中引入延迟来实现。

## 9.2. HTTP 压缩 {#section-9-2}

filter comp-req

启用根据 "compression" 设置显式尝试压缩 HTTP 请求的过滤器。
隐式设置 "compression direction request"。

filter comp-res

启用根据 "compression" 设置显式尝试压缩 HTTP 响应的过滤器。
隐式设置 "compression direction response"

filter compression（已弃用）

用于向后兼容的别名，其功能等同于同时启用 "comp-req" 和 "comp-res" 过滤器。必须使用 "compression" 关键字来配置相应行为：

在 HAProxy 1.7 中，HTTP 压缩已移入过滤器模块。仍需使用 "compression" 关键字来启用和配置 HTTP 压缩。当未使用其他过滤器时，仅此一项已足够。当与缓存或 fcgi-app 启用时，同样仅此一项已足够。此时，压缩始终在响应存储至缓存后执行。但当同一监听器/前端/后端启用至少一个除缓存或 fcgi-app 以外的过滤器时，必须显式使用过滤器行来启用 HTTP 压缩。了解过滤器的评估顺序十分重要。

另请参阅："compression"、[第 9.4 节](/zh/docs/haproxy/filters/#section-9-4) 关于缓存过滤器，以及 [第 9.5 节](/zh/docs/haproxy/filters/#section-9-5) 关于 fcgi-app 过滤器。

## 9.3. 流处理卸载引擎（SPOE） {#section-9-3}

filter spoe [engine `<name>`] config `<file>`

参数：

```text
<name>      是用于在配置文件中查找对应作用域的引擎名称。未提供时解析整个文件。

<file>      是引擎配置文件的路径。该文件可包含多个引擎的配置；此时每部分必须位于各自的作用域中。
```

流处理卸载引擎（SPOE）是一种与外部组件通信的过滤器。它允许在分层应用中将部分流的特定处理任务卸载至外部组件。这些外部组件及其与之交换的信息主要通过专用配置文件进行配置。此外，还需在 HAProxy 配置中定义专用后端。

SPOE 通过自研的二进制协议——流处理卸载协议（Stream Processing Offload Protocol，SPOP），与外部组件通信。

当 SPOE 在流中使用时，会启动一个专用流来处理与外部组件的通信。主流是该 "SPOE" 流的父流。这意味着可以从 "SPOE" 流中获取主流的变量。有关变量的详细信息，请参见 [第 2.8 节](/zh/docs/haproxy/configuration-basics/#section-2-8)。

有关 SPOE 配置和 SPOP 规范的全部信息，请参见 "doc/SPOE.txt"。

## 9.4. 缓存 {#section-9-4}

filter cache `<name>`

参数：

```text
<name>      是此过滤器使用的缓存段的名称。
```

缓存通过过滤器存储可缓存的响应。必须使用 HTTP 规则 "cache-store" 和 "cache-use" 来定义缓存的使用方式和时机。默认情况下，相应的过滤器会隐式定义。当仅使用 fcgi-app 或压缩过滤器时，无需额外配置即可满足需求。在此情况下，压缩过滤器始终在缓存过滤器之后执行。但当同一监听器/前端/后端使用了除压缩或 fcgi-app 以外的其他过滤器时，必须显式添加过滤器行以使用缓存。了解过滤器的评估顺序十分重要。

有关更多信息，请参见：[第 9.2 节](/zh/docs/haproxy/filters/#section-9-2) 关于压缩过滤器，[第 9.5 节](/zh/docs/haproxy/filters/#section-9-5) 关于 fcgi-app 过滤器，以及 [第 6 节](/zh/docs/haproxy/cache/) 关于缓存。

## 9.5. Fcgi-app {#section-9-5}

filter fcgi-app `<name>`

参数：

```text
<name>      是此过滤器使用的 fcgi-app 段的名称。
```

FastCGI 应用程序使用过滤器对请求路径上的所有自定义参数进行评估，并对响应路径上的头进行处理。`<name>` 必须引用一个已存在的 fcgi-app 段。应使用指令 "use-fcgi-app" 来定义所使用的应用程序。默认情况下，相应的过滤器会隐式定义。当仅使用缓存或压缩过滤器时，此方式已足够。但当同一后端使用至少一个除压缩或缓存以外的其他过滤器时，必须显式使用过滤器行指定 fcgi-app。这一点对于了解过滤器的评估顺序至关重要。

另请参阅："use-fcgi-app"、[第 9.2 节](/zh/docs/haproxy/filters/#section-9-2) 关于压缩过滤器，[第 9.4 节](/zh/docs/haproxy/filters/#section-9-4) 关于缓存过滤器，以及 [第 10 节](/zh/docs/haproxy/fastcgi/) 关于 FastCGI 应用。

## 9.6. OpenTracing {#section-9-6}

OpenTracing 过滤器为在 HAProxy 中使用分布式追踪提供了原生支持。通过向受支持的追踪器（如 Datadog、Jaeger、Lightstep 和 Zipkin）之一发送符合 OpenTracing 规范的请求，即可启用该功能。请注意：所列追踪器不按优先级排序，而是按字母顺序排列。

此功能仅在 HAProxy 编译时启用 USE_OT=1 时才可用。

通过在 HAProxy 配置中显式指定，可激活 OpenTracing 过滤器。
若未执行此操作，OpenTracing 过滤器将完全不参与 HAProxy 的工作。

filter opentracing [id `<id>`] config `<file>`

参数：

```text
<id>        是用于在配置文件中查找对应作用域的 OpenTracing 过滤器 ID。
            未指定过滤器 ID 时默认使用 'ot-filter'。若配置文件未指定作用域，
            则该配置适用于所有已定义的 OpenTracing 过滤器。

<file>      是 OpenTracing 配置文件的路径。同一文件可同时包含多个 OpenTracing 过滤器的配置。
            此时，可不定义作用域，让同一配置适用于所有过滤器；也可为每个过滤器分别定义作用域。
```

有关过滤器操作、配置和使用的更详细文档，请参见 addons/ot 目录。

请注意：由于 OpenTracing 本身已不再由其作者维护或支持，因此不建议在新设计中使用 OpenTracing 过滤器。OpenTracing 将在 3.3 版本中弃用，并在 3.5 版本中移除。自 3.4 版本起，已提供基于 OpenTelemetry 的替代过滤器，完整的构建说明目前位于：

```text
https://github.com/haproxytech/haproxy-opentelemetry/
```

## 9.7. 带宽限制 {#section-9-7}

```haproxy
filter bwlim-in  <name> default-limit <size> default-period <time> [min-size <sz>]
filter bwlim-out <name> default-limit <size> default-period <time> [min-size <sz>]
filter bwlim-in  <name> limit <size> key <pattern> [table <table>] [min-size <sz>]
filter bwlim-out <name> limit <size> key <pattern> [table <table>] [min-size <sz>]
```

参数：

```text
<name>      是过滤器名称，'set-bandwidth-limit' 动作通过此名称引用特定的带宽限制过滤器。

<size>      是一个周期内可转发的最大字节数。逐流和共享带宽限制过滤器均必须指定此值。
            该值遵循 HAProxy 大小格式，以字节表示。

<pattern>   是第 7.3 节所述的样本表达式规则，描述需要分析、提取、组合的元素，
            并据此选择要更新计数器的表条目。仅共享带宽限制过滤器必须指定此项。

<table>     是可选的表，用于替代默认表，即当前代理中声明的 stick-table。
            此项仅可用于共享带宽限制过滤器。

<time>      是计算带宽限制速率所用的默认时间周期。此项仅可用于逐流带宽限制过滤器。
            该值遵循 HAProxy 时间格式，以毫秒表示。

<min-size>  是可选的单个流每次转发的最小字节数，最后一个数据包可小于此值。
            此项可用于逐流和共享带宽限制过滤器。该值遵循 HAProxy 大小格式，以字节表示。
```

带宽限制过滤器应用于限制流级别的数据转发速度。由此延伸，此类过滤器可限制资源所消耗的网络带宽。可同时使用多个带宽限制过滤器。例如，可为每个源地址设置限制，以确保客户端不会占用全部网络带宽，从而影响其他客户端；同时，也可为每个流设置限制，以便对单个客户端的多个连接进行公平处理。

这些过滤器的定义顺序至关重要。如果在一个流上启用了多个带宽过滤器，过滤将按照其定义顺序依次应用。其他过滤器的定义顺序同样重要。例如，根据 HTTP 压缩过滤器定义在带宽限制过滤器之前或之后，限制将作用于压缩后的载荷或不作用于压缩后的载荷。缓存过滤器的情况亦是如此。

有两种带宽限制过滤器。第一种强制执行默认限制，且按流应用。第二种使用粘性表，强制执行一个在共享同一表项的所有流之间均分的限制。

此外，对于特定过滤器，根据所使用的过滤器关键字，限制可应用于从客户端接收并转发至服务器的入站数据，或应用于从服务器接收并发送至客户端的出站数据。若需对入站数据施加限制，必须使用 "bwlim-in" 关键字。若需对出站数据施加限制，必须使用 "bwlim-out" 关键字。在两种情况下，带宽限制均在流级别上应用于转发的数据。

带宽限制在流级别应用，而非连接级别。对于多路复用协议（H2、H3 和 FastCGI），同一连接内的不同流可具有不同的限制。

对于基于流的带宽限制过滤器，必须定义默认周期和默认限制。如其名称所示，这些是用于设置流带宽限制速率的默认值。然而，对于此类过滤器（仅限此类），当使用 TCP/HTTP 的 "set-bandwidth-limit" 动作启用过滤器时，可通过样本表达式重新定义这些值。

对于共享带宽限制过滤器，根据其应用于入站或出站数据，所使用的粘性表必须存储相应的字节速率信息。
必须存储 "bytes_in_rate(`<period>`)" 计数器以限制入站数据，
必须使用 "bytes_out_rate(`<period>`)" 计数器以限制出站数据。

最后，可以为特定流设置带宽限制过滤器每次可转发的最小字节数。此举旨在避免转发过少的数据，以降低 CPU 使用率。该值必须谨慎设定。若设置过低，可能增加 CPU 使用率；若设置过高，则可能增加延迟。该值与所设定的带宽限制密切相关。若其值过于接近带宽限制，为避免超出限制，可能产生短暂停顿，因为单次消耗的字节数过多。该值高度依赖于过滤器配置。一个较好的做法是，从约 2 个 TCP MSS（通常为 2896 字节）开始，经若干次试验后进行调整。

示例：

```text
frontend http
    bind *:80
    mode http

    # If this filter is enabled, the stream will share the download limit
    # of 10m/s with all other streams with the same source address.
    filter bwlim-out limit-by-src key src table limit-by-src limit 10m

    # If this filter is enabled, the stream will be limited to download at 1m/s,
    # independently of all other streams.
    filter bwlim-out limit-by-strm default-limit 1m default-period 1s

    # Limit all streams to 1m/s (the default limit) and those accessing the
    # internal API to 100k/s. Limit each source address to 10m/s. The shared
    # limit is applied first. Both are limiting the download rate.
    http-request set-bandwidth-limit limit-by-strm
    http-request set-bandwidth-limit limit-by-strm limit 100k if { path_beg /internal }
    http-request set-bandwidth-limit limit-by-src
    ...

backend limit-by-src
    # The stickiness table used by <limit-by-src> filter
    stick-table type ip size 1m expire 3600s store bytes_out_rate(1s)
```

另请参见："tcp-request content set-bandwidth-limit"、"tcp-response content set-bandwidth-limit"、"http-request set-bandwidth-limit" 和 "http-response set-bandwidth-limit"。
