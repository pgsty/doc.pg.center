---
title: "6. Cache"
linkTitle: "6. Cache"
weight: 170
description: "Cache limitations and setup in cache and proxy sections"
icon: fa-solid fa-box-archive
module: [HAPROXY]
categories: [Reference]
aliases:
  - /haproxy/configuration/cache/
  - /docs/haproxy/configuration/cache/
  - /haproxy/cache/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 6"
---

HAProxy provides a cache, which was designed to perform cache on small objects (favicon, css...).
This is a minimalist low-maintenance cache which runs in RAM.

The cache is based on a memory area shared between all threads, and split in 1kB blocks.

If an object is not used anymore, it can be deleted to store a new object independently of its
expiration date. The oldest objects are deleted first when we try to allocate a new one.

The cache uses a hash of the host header and the URI as the key.

It's possible to view the status of a cache using the Unix socket command "show cache" consult
[section 9.3](/docs/haproxy/statistics-and-monitoring/#section-9-3) "Unix Socket commands" of Management Guide for more details.

When an object is delivered from the cache, the server name in the log is replaced by "`<CACHE>`".

## 6.1. Limitation {#section-6-1}

The cache won't store and won't deliver objects in these cases:

- If the response is not a 200

- If the response contains a Vary header and either the process-vary option is disabled, or a
  currently unmanaged header is specified in the Vary value (only accept-encoding, referer and
  origin are managed for now)

- If the Content-Length + the headers size is greater than "max-object-size"

- If the response is not cacheable

- If the response does not have an explicit expiration time (s-maxage or max-age Cache-Control
  directives or Expires header) or a validator (ETag or Last-Modified headers)

- If the process-vary option is enabled and there are already max-secondary-entries entries with the
  same primary key as the current response

- If the process-vary option is enabled and the response has an unknown encoding (not mentioned in
  <https://www.iana.org/assignments/http-parameters/http-parameters.xhtml>) while varying on the
  accept-encoding client header

- If the request is not a GET

- If the HTTP version of the request is smaller than 1.1

- If the request contains an Authorization header

## 6.2. Setup {#section-6-2}

To setup a cache, you must define a cache section and use it in a proxy with the corresponding
http-request and http-response actions.

### 6.2.1. Cache section {#section-6-2-1}

<a id="entry-6-2-1-cache"></a>

**`cache <name>`**

```haproxy
cache <name>
```

Declare a cache section, allocate a shared cache memory named `<name>`, the size of cache is
mandatory (see keyword "total-max-size" below).

<a id="entry-6-2-1-max-age"></a>

**`max-age <seconds>`**

```haproxy
max-age <seconds>
```

Define the maximum expiration duration. The expiration is set as the lowest value between the
s-maxage or max-age (in this order) directive in the Cache-Control response header and this value.
The default value is 60 seconds, which means that you can't cache an object more than 60 seconds by
default.

<a id="entry-6-2-1-max-object-size"></a>

**`max-object-size <bytes>`**

```haproxy
max-object-size <bytes>
```

Define the maximum size of the objects to be cached. Must not be greater than an half of
"total-max-size". If not set, it equals to a 256th of the cache size. All objects with sizes larger
than "max-object-size" will not be cached.

<a id="entry-6-2-1-max-secondary-entries"></a>

**`max-secondary-entries <number>`**

```haproxy
max-secondary-entries <number>
```

Define the maximum number of simultaneous secondary entries with the same primary key in the cache.
This needs the vary support to be enabled. Its default value is 10 and should be passed a strictly
positive integer.

<a id="entry-6-2-1-process-vary"></a>

**`process-vary <on/off>`**

```haproxy
process-vary <on/off>
```

Enable or disable the processing of the Vary header. When disabled, a response containing such a
header will never be cached. When enabled, we need to calculate a preliminary hash for a subset of
request headers on all the incoming requests (which might come with a cpu cost) which will be used
to build a secondary key for a given request (see RFC 7234#4.1). The secondary key is built out of
the contents of the 'accept-encoding', 'referer' and 'origin' headers for now. Note that the
'origin' and 'referer' headers are single-valued per the RFC, so a request carrying more than one
occurrence of either should be considered malformed. For such requests no secondary key is built and
the response is never delivered from the cache so that we can let the server decide how to handle
the situation. The default value is off (disabled).

<a id="entry-6-2-1-total-max-size"></a>

**`total-max-size <megabytes>`**

```haproxy
total-max-size <megabytes>
```

Define the size in RAM of the cache in megabytes. This size is split in blocks of 1kB which are used
by the cache entries. Its maximum value is 4095.

### 6.2.2. Proxy section {#section-6-2-2}

The proxy section making use of the cache will need to involve the "cache-use" action in the
"http-request" rule set in order to look up the requested object from the cache, and the
"cache-store" action in the "http-response" rule set in order to store or update the retrieved
object into the cache. Each of these actions may optionally involve conditions. For example, one
could decide to skip the "cache-use" action for a certain sub-directory that is known not to be
cacheable, or to skip the "cache-store" action for certain content-types that are known to be
worthless. Please note that the cache indexing key is computed during the "cache-use" action, so if
this action is skipped, no attempt to update the cache will be made on the response path anyway.

Example:

```text
backend bck1
  mode http

  http-request cache-use foobar
  http-response cache-store foobar
  server srv1 127.0.0.1:80

cache foobar
  total-max-size 4
  max-age 240
```
