---
title: "Standard Features"
linkTitle: "Standard Features"
weight: 50
description: "Sample fetches, maps, ACLs, content switching, stick tables, rewriting, and server protection"
icon: fa-solid fa-sliders
module: [HAPROXY]
categories: [Concept]
aliases:
  - /haproxy/intro/standard-features/
  - /docs/haproxy/intro/standard-features/
  - /haproxy/standard-features/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, sections 3.4–3.4.8"
---

In this section, some features that are very commonly used in HAProxy but are not necessarily
present on other load balancers are enumerated.

## 3.4.1. Standard features : Sampling and converting information {#section-3-4-1}

HAProxy supports information sampling using a wide set of "sample fetch functions". The principle is
to extract pieces of information known as samples, for immediate use. This is used for stickiness,
to build conditions, to produce information in logs or to enrich HTTP headers.

Samples can be fetched from various sources:

- constants: integers, strings, IP addresses, binary blocks;

- the process: date, environment variables, server/frontend/backend/process state, byte/connection
  counts/rates, queue length, random generator, ...

- variables: per-session, per-request, per-response variables;

- the client connection: source and destination addresses and ports, and all related statistics
  counters;

- the SSL client session: protocol, version, algorithm, cipher, key size, session ID, all client and
  server certificate fields, certificate serial, SNI, ALPN, NPN, client support for certain
  extensions;

- request and response buffers contents: arbitrary payload at offset/length, data length, RDP
  cookie, decoding of SSL hello type, decoding of TLS SNI;

- HTTP (request and response): method, URI, path, query string arguments, status code, headers
  values, positional header value, cookies, captures, authentication, body elements;

A sample may then pass through a number of operators known as "converters" to experience some
transformation. A converter consumes a sample and produces a new one, possibly of a completely
different type. For example, a converter may be used to return only the integer length of the input
string, or could turn a string to upper case. Any arbitrary number of converters may be applied in
series to a sample before final use. Among all available sample converters, the following ones are
the most commonly used:

- arithmetic and logic operators: they make it possible to perform advanced computation on input
  data, such as computing ratios, percentages or simply converting from one unit to another one;

- IP address masks are useful when some addresses need to be grouped by larger networks;

- data representation: URL-decode, base64, hex, JSON strings, hashing;

- string conversion: extract substrings at fixed positions, fixed length, extract specific fields
  around certain delimiters, extract certain words, change case, apply regex-based substitution;

- date conversion: convert to HTTP date format, convert local to UTC and conversely, add or remove
  offset;

- lookup an entry in a stick table to find statistics or assigned server;

- map-based key-to-value conversion from a file (mostly used for geolocation).

## 3.4.2. Standard features : Maps {#section-3-4-2}

Maps are a powerful type of converter consisting in loading a two-columns file into memory at boot
time, then looking up each input sample from the first column and either returning the corresponding
pattern on the second column if the entry was found, or returning a default value. The output
information also being a sample, it can in turn experience other transformations including other map
lookups. Maps are most commonly used to translate the client's IP address to an AS number or country
code since they support a longest match for network addresses but they can be used for various other
purposes.

Part of their strength comes from being updatable on the fly either from the CLI or from certain
actions using other samples, making them capable of storing and retrieving information between
subsequent accesses. Another strength comes from the binary tree based indexation which makes them
extremely fast even when they contain hundreds of thousands of entries, making geolocation very
cheap and easy to set up.

## 3.4.3. Standard features : ACLs and conditions {#section-3-4-3}

Most operations in HAProxy can be made conditional. Conditions are built by combining multiple ACLs
using logic operators (AND, OR, NOT). Each ACL is a series of tests based on the following elements:

- a sample fetch method to retrieve the element to test;

- an optional series of converters to transform the element;

- a list of patterns to match against;

- a matching method to indicate how to compare the patterns with the sample

For example, the sample may be taken from the HTTP "Host" header, it could then be converted to
lower case, then matched against a number of regex patterns using the regex matching method.

Technically, ACLs are built on the same core as the maps, they share the exact same internal
structure, pattern matching methods and performance. The only real difference is that instead of
returning a sample, they only return "found" or or "not found". In terms of usage, ACL patterns may
be declared inline in the configuration file and do not require their own file. ACLs may be named
for ease of use or to make configurations understandable. A named ACL may be declared multiple times
and it will evaluate all definitions in turn until one matches.

About 13 different pattern matching methods are provided, among which IP address mask, integer
ranges, substrings, regex. They work like functions, and just like with any programming language,
only what is needed is evaluated, so when a condition involving an OR is already true, next ones are
not evaluated, and similarly when a condition involving an AND is already false, the rest of the
condition is not evaluated.

There is no practical limit to the number of declared ACLs, and a handful of commonly used ones are
provided. However experience has shown that setups using a lot of named ACLs are quite hard to
troubleshoot and that sometimes using anonymous ACLs inline is easier as it requires less references
out of the scope being analyzed.

## 3.4.4. Standard features : Content switching {#section-3-4-4}

HAProxy implements a mechanism known as content-based switching. The principle is that a connection
or request arrives on a frontend, then the information carried with this request or connection are
processed, and at this point it is possible to write ACLs-based conditions making use of these
information to decide what backend will process the request. Thus the traffic is directed to one
backend or another based on the request's contents. The most common example consists in using the
Host header and/or elements from the path (sub-directories or file-name extensions) to decide
whether an HTTP request targets a static object or the application, and to route static objects
traffic to a backend made of fast and light servers, and all the remaining traffic to a more complex
application server, thus constituting a fine-grained virtual hosting solution. This is quite
convenient to make multiple technologies coexist as a more global solution.

Another use case of content-switching consists in using different load balancing algorithms
depending on various criteria. A cache may use a URI hash while an application would use
round-robin.

Last but not least, it allows multiple customers to use a small share of a common resource by
enforcing per-backend (thus per-customer connection limits).

Content switching rules scale very well, though their performance may depend on the number and
complexity of the ACLs in use. But it is also possible to write dynamic content switching rules
where a sample value directly turns into a backend name and without making use of ACLs at all. Such
configurations have been reported to work fine at least with 300000 backends in production.

## 3.4.5. Standard features : Stick-tables {#section-3-4-5}

Stick-tables are commonly used to store stickiness information, that is, to keep a reference to the
server a certain visitor was directed to. The key is then the identifier associated with the visitor
(its source address, the SSL ID of the connection, an HTTP or RDP cookie, the customer number
extracted from the URL or from the payload, ...) and the stored value is then the server's
identifier.

Stick tables may use 3 different types of samples for their keys: integers, strings and addresses.
Only one stick-table may be referenced in a proxy, and it is designated everywhere with the proxy
name. Up to 8 keys may be tracked in parallel. The server identifier is committed during request or
response processing once both the key and the server are known.

Stick-table contents may be replicated in active-active mode with other HAProxy nodes known as
"peers" as well as with the new process during a reload operation so that all load balancing nodes
share the same information and take the same routing decision if client's requests are spread over
multiple nodes.

Since stick-tables are indexed on what allows to recognize a client, they are often also used to
store extra information such as per-client statistics. The extra statistics take some extra space
and need to be explicitly declared. The type of statistics that may be stored includes the input and
output bandwidth, the number of concurrent connections, the connection rate and count over a period,
the amount and frequency of errors, some specific tags and counters, etc. In order to support
keeping such information without being forced to stick to a given server, a special "tracking"
feature is implemented and allows to track up to 3 simultaneous keys from different tables at the
same time regardless of stickiness rules. Each stored statistics may be searched, dumped and cleared
from the CLI and adds to the live troubleshooting capabilities.

While this mechanism can be used to surclass a returning visitor or to adjust the delivered quality
of service depending on good or bad behavior, it is mostly used to fight against service abuse and
more generally DDoS as it allows to build complex models to detect certain bad behaviors at a high
processing speed.

## 3.4.6. Standard features : Formatted strings {#section-3-4-6}

There are many places where HAProxy needs to manipulate character strings, such as logs, redirects,
header additions, and so on. In order to provide the greatest flexibility, the notion of Formatted
strings was introduced, initially for logging purposes, which explains why it's still called
"log-format". These strings contain escape characters allowing to introduce various dynamic data
including variables and sample fetch expressions into strings, and even to adjust the encoding while
the result is being turned into a string (for example, adding quotes). This provides a powerful way
to build header contents, to build response data or even response templates, or to customize log
lines. Additionally, in order to remain simple to build most common strings, about 50 special tags
are provided as shortcuts for information commonly used in logs.

## 3.4.7. Standard features : HTTP rewriting and redirection {#section-3-4-7}

Installing a load balancer in front of an application that was never designed for this can be a
challenging task without the proper tools. One of the most commonly requested operation in this case
is to adjust requests and response headers to make the load balancer appear as the origin server and
to fix hard coded information. This comes with changing the path in requests (which is strongly
advised against), modifying Host header field, modifying the Location response header field for
redirects, modifying the path and domain attribute for cookies, and so on. It also happens that a
number of servers are somewhat verbose and tend to leak too much information in the response, making
them more vulnerable to targeted attacks. While it's theoretically not the role of a load balancer
to clean this up, in practice it's located at the best place in the infrastructure to guarantee that
everything is cleaned up.

Similarly, sometimes the load balancer will have to intercept some requests and respond with a
redirect to a new target URL. While some people tend to confuse redirects and rewriting, these are
two completely different concepts, since the rewriting makes the client and the server see different
things (and disagree on the location of the page being visited) while redirects ask the client to
visit the new URL so that it sees the same location as the server.

In order to do this, HAProxy supports various possibilities for rewriting and redirects, among
which:

- regex-based URL and header rewriting in requests and responses. Regex are the most commonly used
  tool to modify header values since they're easy to manipulate and well understood;

- headers may also be appended, deleted or replaced based on formatted strings so that it is
  possible to pass information there (e.g. client side TLS algorithm and cipher);

- HTTP redirects can use any 3xx code to a relative, absolute, or completely dynamic (formatted
  string) URI;

- HTTP redirects also support some extra options such as setting or clearing a specific cookie,
  dropping the query string, appending a slash if missing, and so on;

- a powerful "return" directive allows to customize every part of a response like status, headers,
  body using dynamic contents or even template files.

- all operations support ACL-based conditions;

## 3.4.8. Standard features : Server protection {#section-3-4-8}

HAProxy does a lot to maximize service availability, and for this it takes large efforts to protect
servers against overloading and attacks. The first and most important point is that only complete
and valid requests are forwarded to the servers. The initial reason is that HAProxy needs to find
the protocol elements it needs to stay synchronized with the byte stream, and the second reason is
that until the request is complete, there is no way to know if some elements will change its
semantics. The direct benefit from this is that servers are not exposed to invalid or incomplete
requests. This is a very effective protection against slowloris attacks, which have almost no impact
on HAProxy.

Another important point is that HAProxy contains buffers to store requests and responses, and that
by only sending a request to a server when it's complete and by reading the whole response very
quickly from the local network, the server side connection is used for a very short time and this
preserves server resources as much as possible.

A direct extension to this is that HAProxy can artificially limit the number of concurrent
connections or outstanding requests to a server, which guarantees that the server will never be
overloaded even if it continuously runs at 100% of its capacity during traffic spikes. All excess
requests will simply be queued to be processed when one slot is released. In the end, this huge
resource savings most often ensures so much better server response times that it ends up actually
being faster than by overloading the server. Queued requests may be redispatched to other servers,
or even aborted in queue when the client aborts, which also protects the servers against the "reload
effect", where each click on "reload" by a visitor on a slow-loading page usually induces a new
request and maintains the server in an overloaded state.

The slow-start mechanism also protects restarting servers against high traffic levels while they're
still finalizing their startup or compiling some classes.

Regarding the protocol-level protection, it is possible to relax the HTTP parser to accept non
standard-compliant but harmless requests or responses and even to fix them. This allows bogus
applications to be accessible while a fix is being developed. In parallel, offending messages are
completely captured with a detailed report that help developers spot the issue in the application.
The most dangerous protocol violations are properly detected and dealt with and fixed. For example
malformed requests or responses with two Content-length headers are either fixed if the values are
exactly the same, or rejected if they differ, since it becomes a security problem. Protocol
inspection is not limited to HTTP, it is also available for other protocols like TLS or RDP.

When a protocol violation or attack is detected, there are various options to respond to the user,
such as returning the common "HTTP 400 bad request", closing the connection with a TCP reset, or
faking an error after a long delay ("tarpit") to confuse the attacker. All of these contribute to
protecting the servers by discouraging the offending client from pursuing an attack that becomes
very expensive to maintain.

HAProxy also proposes some more advanced options to protect against accidental data leaks and
session crossing. Not only it can log suspicious server responses but it will also log and
optionally block a response which might affect a given visitors' confidentiality. One such example
is a cacheable cookie appearing in a cacheable response and which may result in an intermediary
cache to deliver it to another visitor, causing an accidental session sharing.
