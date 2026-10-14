---
title: "1. Quick Reminder About HTTP"
linkTitle: "1. HTTP Fundamentals"
weight: 120
description: "HTTP transactions, requests, responses, headers, and protocol terminology"
icon: fa-solid fa-globe
module: [HAPROXY]
categories: [Concept]
aliases:
  - /haproxy/configuration/http-fundamentals/
  - /haproxy/configuration/
  - /docs/haproxy/configuration/http-fundamentals/
  - /docs/haproxy/configuration/
  - /haproxy/http-fundamentals/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 1"
---

This document covers the configuration language as implemented in the version specified above. It
does not provide any hints, examples, or advice. For such documentation, please refer to the
Reference Manual or the Architecture Manual. The numbered chapters are ordered in the flat HAProxy sidebar for direct navigation.

When HAProxy is running in HTTP mode, both the request and the response are fully analyzed and
indexed, thus it becomes possible to build matching criteria on almost anything found in the
contents.

However, it is important to understand how HTTP requests and responses are formed, and how HAProxy
decomposes them. It will then become easier to write correct rules and to debug existing
configurations.

First, HTTP is standardized by a series of RFC that HAProxy follows as closely as possible:

- RFC 9110: HTTP Semantics (explains the meaning of protocol elements)
- RFC 9111: HTTP Caching (explains the rules to follow for an HTTP cache)
- RFC 9112: HTTP/1.1 (representation, interoperability rules, security)
- RFC 9113: HTTP/2 (representation, interoperability rules, security)
- RFC 9114: HTTP/3 (representation, interoperability rules, security)

In addition to these, RFC 8999 to 9002 specify the QUIC transport layer used by the HTTP/3 protocol.

## 1.1. The HTTP transaction model {#section-1-1}

The HTTP protocol is transaction-driven. This means that each request will lead to one and only one
response. Originally, with version 1.0 of the protocol, there was a single request per connection: a
TCP connection is established from the client to the server, a request is sent by the client over
the connection, the server responds, and the connection is closed. A new request then involves a new
connection:

```text
[CON1] [REQ1] ... [RESP1] [CLO1] [CON2] [REQ2] ... [RESP2] [CLO2] ...
```

In this mode, often called the "HTTP close" mode, there are as many connection establishments as
there are HTTP transactions. Since the connection is closed by the server after the response, the
client does not need to know the content length, it considers that the response is complete when the
connection closes. This also means that if some responses are truncated due to network errors, the
client could mistakenly think a response was complete, and this used to cause truncated images to be
rendered on screen sometimes.

Due to the transactional nature of the protocol, it was possible to improve it to avoid closing a
connection between two subsequent transactions. In this mode however, it is mandatory that the
server indicates the content length for each response so that the client does not wait indefinitely.
For this, a special header is used: "Content-length". This mode is called the "keep-alive" mode, and
arrived with HTTP/1.1 (some HTTP/1.0 agents support it), and connections that are reused between
requests are called "persistent connections":

```text
[CON] [REQ1] ... [RESP1] [REQ2] ... [RESP2] [CLO] ...
```

Its advantages are a reduced latency between transactions, less processing power required on the
server side, and the ability to detect a truncated response. It is generally faster than the close
mode, but not always because some clients often limit their concurrent connections to a smaller
value, and this compensates less for poor network connectivity. Also, some servers have to keep the
connection alive for a long time waiting for a possible new request and may experience a high memory
usage due to the high number of connections, and closing too fast may break some requests that
arrived at the moment the connection was closed.

In this mode, the response size needs to be known upfront so that's not always possible with
dynamically generated or compressed contents. For this reason another mode was implemented, the
"chunked mode", where instead of announcing the size of the whole size at once, the sender only
advertises the size of the next "chunk" of response it already has in a buffer, and can terminate at
any moment with a zero-sized chunk. In this mode, the Content-Length header is not used.

Another improvement in the communications is the pipelining mode. It still uses keep-alive, but the
client does not wait for the first response to send the second request. This is useful for fetching
large number of images composing a page:

```text
[CON] [REQ1] [REQ2] ... [RESP1] [RESP2] [CLO] ...
```

This can obviously have a tremendous benefit on performance because the network latency is
eliminated between subsequent requests. Many HTTP agents do not correctly support pipelining since
there is no way to associate a response with the corresponding request in HTTP. For this reason, it
is mandatory for the server to reply in the exact same order as the requests were received. In
practice, after several attempts by various clients to deploy it, it has been totally abandoned for
its lack of reliability on certain servers. But it is mandatory for servers to support it.

The next improvement is the multiplexed mode, as implemented in HTTP/2 and HTTP/3. In this mode,
multiple transactions (i.e. request-response pairs) are transmitted in parallel over a single
connection, and they all progress at their own speed, independent from each other. With multiplexed
protocols, a new notion of "stream" was introduced, to represent these parallel communications
happening over the same connection. Each stream is generally assigned a unique identifier for a
given connection, that is used by both endpoints to know where to deliver the data. It is fairly
common for clients to start many (up to 100, sometimes more) streams in parallel over a same
connection, and let the server sort them out and respond in any order depending on what response is
available. The main benefit of the multiplexed mode is that it significantly reduces the number of
round trips, and speeds up page loading time over high latency networks. It is sometimes visible on
sites using many images, where all images appear to load in parallel.

These protocols have also improved their efficiency by adopting some mechanisms to compress header
fields in order to reduce the number of bytes on the wire, so that without the appropriate tools,
they are not realistically manipulable by hand nor readable to the naked eye like HTTP/1 was. For
this reason, various examples of HTTP messages continue to be represented in literature (including
this document) using the HTTP/1 syntax even for newer versions of the protocol.

HTTP/2 suffers from some design limitations, such as packet losses affecting all streams at once,
and if a client takes too much time to retrieve an object (e.g. needs to store it on disk), it may
slow down its retrieval and make it impossible during this time to access the data that is pending
behind it. This is called "head of line blocking" or "HoL blocking" or sometimes just "HoL".

HTTP/3 is implemented over QUIC, itself implemented over UDP. QUIC solves the head of line blocking
at the transport level by means of independently handled streams. Indeed, when experiencing loss, an
impacted stream does not affect the other streams, and all of them can be accessed in parallel. QUIC
also provides connection migration support but currently haproxy does not support it.

By default HAProxy operates in keep-alive mode with regards to persistent connections: for each
connection it processes each request and response, and leaves the connection idle on both sides
between the end of a response and the start of a new request. When it receives HTTP/2 connections
from a client, it processes all the requests in parallel and leaves the connection idling, waiting
for new requests, just as if it was a keep-alive HTTP connection.

HAProxy essentially supports 3 connection modes:

- keep alive : all requests and responses are processed, and the client facing and server facing
  connections are kept alive for new requests. This is the default and suits the modern web and
  modern protocols (HTTP/2 and HTTP/3).

- server close : the server-facing connection is closed after the response.

- close : the connection is actively closed after end of response on both sides.

In addition to this, by default, the server-facing connection is reusable by any request from any
client, as mandated by the HTTP protocol specification, so any information pertaining to a specific
client has to be passed along with each request if needed (e.g. client's source address etc). When
HTTP/2 is used with a server, by default HAProxy will dedicate this connection to the same client to
avoid the risk of head of line blocking between clients.

## 1.2. Terminology {#section-1-2}

Inside HAProxy, the terminology has evolved a bit over the ages to follow the evolutions of the HTTP
protocol and its usages. While originally there was no significant difference between a connection,
a session, a stream or a transaction, these ones clarified over time to match closely what exists in
the modern versions of the HTTP protocol, though some terms remain visible in the configuration or
the command line interface for the purpose of historical compatibility.

Here are some definitions that apply to the current version of HAProxy:

- connection: a connection is a single, bidiractional communication channel between a remote agent
  (client or server) and haproxy, at the lowest level possible. Usually it corresponds to a TCP
  socket established between a pair of IP and ports. On the client-facing side, connections are the
  very first entities that are instantiated when a client connects to haproxy, and rules applying at
  the connection level are the earliest ones that apply.

- session: a session adds some context information associated with a connection. This includes and
  information specific to the transport layer (e.g. TLS keys etc), or variables. This term has long
  been used inside HAProxy to denote end-to-end HTTP/1.0 communications between two ends, and as
  such it remains visible in the name of certain CLI commands or statistics, despite representing
  streams nowadays, but the help messages and descriptions try to make this unambiguous. It is still
  valid when it comes to network-level terminology (e.g. TCP sessions inside the operating systems,
  or TCP sessions across a firewall), or for non-HTTP user-level applications (e.g. a telnet session
  or an SSH session). It must not be confused with "application sessions" that are used to store a
  full user context in a cookie and require to be sent to the same server.

- stream: a stream exactly corresponds to an end-to-end bidirectional communication at the
  application level, where analysis and transformations may be applied. In HTTP, it contains a
  single request and its associated response, and is instantiated by the arrival of the request and
  is finished with the end of delivery of the response. In this context there is a 1:1 relation
  between such a stream and the stream of a multiplexed protocol. In TCP communications there is a
  single stream per connection.

- transaction: a transaction is only a pair of a request and the associated response. The term was
  used in conjunction with sessions before the streams but nowadays there is a 1:1 relation between
  a transaction and a stream. It is essentially visible in the variables' scope "txn" which is valid
  during the whole transaction, hence the stream.

- request: it designates the traffic flowing from the client to the server. It is mainly used for
  HTTP to indicate where operations are performed. This term also exists for TCP operations to
  indicate where data are processed. Requests often appear in counters as a unit of traffic or
  activity. They do not always imply a response (e.g. due to errors), but since there is no
  spontaneous responses without requests, requests remain a relevant metric of the overall activity.
  In TCP there are as many requests as connections.

- response: this designates the traffic flowing from the server to the client, or sometimes from
  HAProxy to the client, when HAProxy produces the response itself (e.g. an HTTP redirect).

- service: this generally indicates some internal processing in HAProxy that does not require a
  server, such as the stats page, the cache, or some Lua code to implement a small application. A
  service usually reads a request, performs some operations and produces a response.

## 1.3. HTTP request {#section-1-3}

First, let's consider this HTTP request:

```text
Line     Contents
number
   1     GET /serv/login.php?lang=en&profile=2 HTTP/1.1
   2     Host: www.mydomain.com
   3     User-agent: my small browser
   4     Accept: image/jpeg, image/gif
   5     Accept: image/png
```

### 1.3.1. The Request line {#section-1-3-1}

Line 1 is the "request line". It is always composed of 3 fields:

- a METHOD : GET
- a URI : /serv/login.php?lang=en&profile=2
- a version tag: HTTP/1.1

All of them are delimited by what the standard calls LWS (linear white spaces), which are commonly
spaces, but can also be tabs or line feeds/carriage returns followed by spaces/tabs. The method
itself cannot contain any colon (':') and is limited to alphabetic letters. All those various
combinations make it desirable that HAProxy performs the splitting itself rather than leaving it to
the user to write a complex or inaccurate regular expression.

The URI itself can have several forms:

- A "relative URI":

```text
  /serv/login.php?lang=en&profile=2

It is a complete URL without the host part. This is generally what is
received by servers, reverse proxies and transparent proxies.
```

- An "absolute URI", also called a "URL":

```text
  http://192.168.0.12:8080/serv/login.php?lang=en&profile=2

It is composed of a "scheme" (the protocol name followed by '://'), a host
name or address, optionally a colon (':') followed by a port number, then
a relative URI beginning at the first slash ('/') after the address part.
This is generally what proxies receive, but a server supporting HTTP/1.1
must accept this form too.
```

- a star ('\*'): this form is only accepted in association with the OPTIONS method and is not
  relayable. It is used to inquiry a next hop's capabilities.

- an address:port combination: 192.168.0.12:80 This is used with the CONNECT method, which is used
  to establish TCP tunnels through HTTP proxies, generally for HTTPS, but sometimes for other
  protocols too.

In a relative URI, two sub-parts are identified. The part before the question mark is called the
"path". It is typically the relative path to static objects on the server. The part after the
question mark is called the "query string". It is mostly used with GET requests sent to dynamic
scripts and is very specific to the language, framework or application in use.

HTTP/2 and HTTP/3 do not convey a version information with the request, so the version is assumed to
be the same as the one of the underlying protocol (i.e. "HTTP/2"). In addition, these protocols do
not send a request line as one part, but split it into individual fields called "pseudo-headers",
whose name start with a colon, and which are conveniently reassembled by HAProxy into an equivalent
request line. For this reason, request lines found in logs may slightly differ between HTTP/1.x and
HTTP/2 or HTTP/3.

### 1.3.2. The request headers {#section-1-3-2}

The headers start at the second line. They are composed of a name at the beginning of the line,
immediately followed by a colon (':'). Traditionally, an LWS is added after the colon but that's not
required. Then come the values. Multiple identical headers may be folded into one single line,
delimiting the values with commas, provided that their order is respected. This is commonly
encountered in the "Cookie:" field. A header may span over multiple lines if the subsequent lines
begin with an LWS. In the example in 1.3, lines 4 and 5 define a total of 3 values for the "Accept:"
header. Finally, all LWS at the beginning or at the end of a header are ignored and are not part of
the value, as per the specification.

Contrary to a common misconception, header names are not case-sensitive, and their values are not
either if they refer to other header names (such as the "Connection:" header). In HTTP/2 and HTTP/3,
header names are always sent in lower case, as can be seen when running in debug mode. Internally,
all header names are normalized to lower case so that HTTP/1.x and HTTP/2 or HTTP/3 use the exact
same representation, and they are sent as-is on the other side. This explains why an HTTP/1.x
request typed with camel case is delivered in lower case.

The end of the headers is indicated by the first empty line. People often say that it's a double
line feed, which is not exact, even if a double line feed is one valid form of empty line.

Fortunately, HAProxy takes care of all these complex combinations when indexing headers, checking
values and counting them, so there is no reason to worry about the way they could be written, but it
is important not to accuse an application of being buggy if it does unusual, valid things.

Important note:

```text
As suggested by RFC7231, HAProxy normalizes headers by replacing line breaks
in the middle of headers by LWS in order to join multi-line headers. This
is necessary for proper analysis and helps less capable HTTP parsers to work
correctly and not to be fooled by such complex constructs.
```

## 1.4. HTTP response {#section-1-4}

An HTTP response looks very much like an HTTP request. Both are called HTTP messages. Let's consider
this HTTP response:

```text
Line     Contents
number
   1     HTTP/1.1 200 OK
   2     Content-length: 350
   3     Content-Type: text/html
```

As a special case, HTTP supports so called "Informational responses" as status codes 1xx. These
messages are special in that they don't convey any part of the response, they're just used as sort
of a signaling message to ask a client to continue to post its request for instance. In the case of
a status 100 response the requested information will be carried by the next non-100 response message
following the informational one. This implies that multiple responses may be sent to a single
request, and that this only works when keep-alive is enabled (1xx messages appeared in HTTP/1.1).
HAProxy handles these messages and is able to correctly forward and skip them, and only process the
next non-100 response. As such, these messages are neither logged nor transformed, unless explicitly
state otherwise. Status 101 messages indicate that the protocol is changing over the same connection
and that HAProxy must switch to tunnel mode, just as if a CONNECT had occurred. Then the Upgrade
header would contain additional information about the type of protocol the connection is switching
to.

### 1.4.1. The response line {#section-1-4-1}

Line 1 is the "response line". It is always composed of 3 fields:

- a version tag: HTTP/1.1
- a status code: 200
- a reason : OK

The status code is always 3-digit. The first digit indicates a general status:

- 1xx = informational message to be skipped (e.g. 100, 101)
- 2xx = OK, content is following (e.g. 200, 206)
- 3xx = OK, no content following (e.g. 302, 304)
- 4xx = error caused by the client (e.g. 401, 403, 404)
- 5xx = error caused by the server (e.g. 500, 502, 503)

Status codes greater than 599 must not be emitted in communications, though certain agents may
produce them in logs to report their internal statuses. Please refer to RFC9110 for the detailed
meaning of all such codes. HTTP/2 and above do not have a version tag and use the ":status"
pseudo-header to report the status code.

The "reason" field is just a hint, but is not parsed by clients. Anything can be found there, but
it's a common practice to respect the well-established messages. It can be composed of one or
multiple words, such as "OK", "Found", or "Authentication Required". It does not exist in HTTP/2 and
above and is not emitted there. When a response from HTTP/2 or above is transmitted to an HTTP/1
client, HAProxy will produce such a common reason field that matches the status code.

HAProxy may emit the following status codes by itself:

```text
Code  When / reason
 200  access to stats page, and when replying to monitoring requests
 301  when performing a redirection, depending on the configured code
 302  when performing a redirection, depending on the configured code
 303  when performing a redirection, depending on the configured code
 307  when performing a redirection, depending on the configured code
 308  when performing a redirection, depending on the configured code
 400  for an invalid or too large request
 401  when an authentication is required to perform the action (when
      accessing the stats page)
 403  when a request is forbidden by a "http-request deny" rule
 404  when the requested resource could not be found
 408  when the request timeout strikes before the request is complete
 410  when the requested resource is no longer available and will not
      be available again
 413  when a HTTP/1.0 GET/HEAD/DELETE requests has a payload, also see
      the "h1-accept-payload-with-any-method" option
 500  when HAProxy encounters an unrecoverable internal error, such as a
      memory allocation failure, which should never happen
 501 when HAProxy is unable to satisfy a client request because of an
     unsupported feature
 502  when the server returns an empty, invalid or incomplete response, or
      when an "http-response deny" rule blocks the response.
 503  when no server was available to handle the request, or in response to
      monitoring requests which match the "monitor fail" condition
 504  when the response timeout strikes before the server responds
```

The error 4xx and 5xx codes above may be customized (see "errorloc" in [section 4.2](/docs/haproxy/proxies/#section-4-2)). Other status
codes can be emitted on purpose by specific actions (see the "deny", "return" and "redirect" actions
in [section 4.3](/docs/haproxy/proxies/#section-4-3) for example).

### 1.4.2. The response headers {#section-1-4-2}

Response headers work exactly like request headers, and as such, HAProxy uses the same parsing
function for both. Please refer to paragraph 1.3.2 for more details.
