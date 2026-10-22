---
title: "11. Stick Tables and Peers"
linkTitle: "11. Stick Tables & Peers"
weight: 220
description: "Stick-table storage and peers replication declarations"
icon: fa-solid fa-table
module: [HAPROXY]
categories: [Reference]
aliases:
  - /haproxy/configuration/stick-tables-and-peers/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 11"
---

Stick-tables in HAProxy are a mechanism which permits to associate a certain number of information
and metrics with a key of a certain type, and this for a certain duration after the last update.
This can be seen as a multicolumn line in a table, where the line number is defined by the key
value, and the columns all represent distinct criteria.

Stick-tables were originally designed to store client-server stickiness information in order to
maintain persistent sessions between these entities. A client would connect or send a request, this
client would be identified via a discriminator (source address, cookie, URL parameter) and the
chosen server would be stored in association with this discriminator in a stick table for a
configurable duration so that subsequent accesses from the same client could automatically be routed
to the same server, where the client had created its application session.

Nowadays, stick-tables can store more information than just a server number, elements such as
activity metrics related to a specific client can be stored (request counts/rates, connection
counts/rates, byte counts/rates etc), as well as some arbitrary event counters ("gpc" for "General
Purpose Counters") and some tags to label a client with certain characteristics ("gpt" for "General
Purpose Tag").

Stick-tables may be referenced by the "stick" directives, which are used for client-server
stickiness, by "track-sc" rules, which are used to describe what key to track in which table in
order to collect metrics, as well as by a number of sample-fetch functions and converters which can
perform an immediate lookup of a given key to retrieve a specific metric or data. The general
principle is that updates to tables (gpt/gpc/metrics) as well as lookups of stickiness information
refresh the accessed entry and postpone its expiration, while mere lookups from sample-fetch
functions and converters only extract the data without postponing the entry's expiration.

In order for the mechanism to scale and to resist to HAProxy reloads and fail-over, it is possible
to share stick-tables updates with other nodes called "peers" via the "Peers" mechanism described in
[section 11.2](/haproxy/stick-tables-and-peers/#section-11-2). In order to finely tune the communication with peers, it is possible to also decide
that some tables only receive information from peers, or that updates from peers should instead be
forwarded to a different table.

Finally, stick-tables may be declared either in proxy sections (frontends, backends) using the
"stick-table" keyword, where there may only be one per section and where they will get the name of
that section, or in peers sections with the "table" keyword followed by the table's name, and which
permits to declare multiple stick-tables in the same "peers" section. If multiple stick-tables are
needed, usually the recommended solution is either to declare them in a peers section (in case they
intend to be shared), or to create extra backend sections, each with only the "stick-table"
definition in them.

## 11.1. stick-table declaration {#section-11-1}

The declaration of a stick-table in a proxy section ("frontend", "backend", "listen") and in "peers"
sections is very similar, with the differences being that the one in the peers section requires a
mandatory name and doesn't take a "peers" option.

In a "frontend", "backend" or "listen" section:

stick-table type `<type>` size `<size>` [expire `<expire>`] [nopurge] [recv-only] [write-to
`<wtable>`] [srvkey `<srvkey>`] [store `<data_type>`]\* [brates-factor `<factor>`] [peers
`<peersect>`]

In a "peers" section:

table `<name>` type `<type>` size `<size>` [expire `<expire>`] [nopurge] [recv-only]
[write-to `<wtable>`] [srvkey `<srvkey>`] [store `<data_type>`]\* [brates-factor `<factor>`]

Arguments: (mandatory ones first, then alphabetically sorted):

- type `<type>` This mandatory argument sets the key type to `<type>`, which usually is a single
  word but may also have its own arguments:

  - ip This type should be avoided in favor of a more explicit one such as "ipv4" or "ipv6". Prior
    to version 3.2 it was the only way to configure IPv4. In 3.2, "ip" is an alias for "ipv4", and
    "ipv4" is preferred. In a future version, "ip" will instead correspond to "ipv6". It is only
    meant to ease the transition from pre-3.2 to post-3.2.

  - ipv4 A table declared with this type will only store IPv4 addresses. This form is very compact
    (about 50 bytes per entry) and allows very fast entry lookup and stores with almost no overhead.
    This is mainly used to store client source IP addresses.

  - ipv6 A table declared with "type ipv6" will only store IPv6 addresses. This form is very compact
    (about 60 bytes per entry) and allows very fast entry lookup and stores with almost no overhead.
    This is mainly used to store client source IP addresses.

  - integer A table declared with "type integer" will store 32bit integers which can represent a
    client identifier found in a request for instance.

  - string [len `<len>`] A table declared with "type string" will store substrings of up to
    `<len>` characters. If the string provided by the pattern extractor is larger than `<len>`, it
    will be truncated before being stored. During matching, at most `<len>` characters will be
    compared between the string in the table and the extracted pattern. When not specified, the
    string is automatically limited to 32 characters. Increasing the length can have a
    non-negligible memory usage impact.

  - binary [len `<len>`] A table declared with "type binary" will store binary blocks of `<len>`
    bytes. If the block provided by the pattern extractor is larger than `<len>`, it will be
    truncated before being stored. If the block provided by the sample expression is shorter than
    `<len>`, it will be padded by 0. When not specified, the block is automatically limited to 32
    bytes. Increasing the length can have a non-negligible memory usage impact.

- size `<size>` This mandatory argument sets maximum number of entries that can fit in the table to
  `<size>`. This value directly impacts memory usage. Count approximately 50 bytes per entry in
  addition to the key size above, and optionally stored metrics, plus the size of a string if any.
  The size supports suffixes "k", "m", "g" for 2^10, 2^20 and 2^30 factors.

- expire `<delay>` Defines the maximum duration of an entry in the table since it was last created,
  refreshed using 'track-sc' or matched using 'stick match' or 'stick on' rule. The expiration delay
  `<delay>` is defined using the standard time format, similarly as the various timeouts, defaulting
  to milliseconds. The maximum duration is slightly above 24 days. See [section 2.5](/haproxy/configuration-basics/#section-2-5) for more
  information. If this delay is not specified, sessions won't automatically expire, but oldest
  entries will be removed upon creation once full. Be sure not to use the "nopurge" parameter if not
  expiration delay is specified. Note: 'table\_\*' converters performs lookups but won't update
  touch expire since they don't require 'track-sc'.

- brates-factor `<factor>` Specifies a factor to be applied to in/out bytes rate. Instead of
  counting each bytes, blocks of bytes are counted. Internally, rates are defined on 32-bits
  counters, limiting them to about 4 billion per period. By using this parameter, it is possible to
  have rates exceeding this 4G limit over the defined period. The factor must be greater than 0 and
  lower than or equal to 1024.

- nopurge indicates that we refuse to purge older entries when the table is full. When not specified
  and the table is full when HAProxy wants to store an entry in it, it will flush a few of the
  oldest entries in order to release some space for the new ones. This is most often the desired
  behavior. In some specific cases, it will be desirable to refuse new entries instead of purging
  the older ones. That may be the case when the amount of data to store is far above the hardware
  limits and we prefer not to offer access to new clients than to reject the ones already connected.
  When using this parameter, be sure to properly set the "expire" parameter (see above).

- recv-only indicates that we don't intend to use the table to perform updates on it, but that we
  only plan on using the table to retrieve data from a remote peer which we are interested in.
  Indeed, the use of this keyword enables the retrieval of local-only values such as "conn_cur" that
  are not learned by default as they would conflict with local updates performed on the table by the
  local peer. Use of this option is only relevant for tables that are not involved in tracking rules
  or methods that perform update operations on the table, or put simpler: remote tables that are
  only used to retrieve information.

- peers `<peersect>` Entries that are created, updated or refreshed will be sent to the peers in
  section `<peersect>` for synchronization, and keys learned from peers in this section will also be
  inserted or updated in the table. Additionally, on startup, an attempt may be done to learn
  entries from an older instance of the process, designated as the "local peer" via this section.

- srvkey `<srvkey>` Specifies how each server is identified for the purposes of the stick table. The
  valid values are "name" and "addr". If "name" is given, then `<name>` argument for the server (may
  be generated by a template). If "addr" is given, then the server is identified by its current
  network address, including the port. "addr" is especially useful if you are using service
  discovery to generate the addresses for servers with peered stick-tables and want to consistently
  use the same host across peers for a stickiness token.

- store `<data_type>` This is used to store additional information in the stick-table. This may be
  used by ACLs in order to control various criteria related to the activity of the client matching
  the stick-table. For each item specified here, the size of each entry will be inflated so that the
  additional data can fit. Several data types may be stored with an entry. Multiple data types may
  be specified after the "store" keyword, as a comma-separated list. Alternatively, it is possible
  to repeat the "store" keyword followed by one or several data types. Except for the "server_id"
  type which is automatically detected and enabled, all data types must be explicitly declared to be
  stored. If an ACL references a data type which is not stored, the ACL will simply not match. Some
  data types require an argument which must be passed just after the type between parenthesis. See
  below for the supported data types and their arguments.

- write-to `<wtable>` Specifies the name of another stick table where peers updates will be written
  to in addition to the source table. `<wtable>` must be of the same type as the table being defined
  and must have the same key length, and source table cannot be used as a target table itself. Every
  time an entry update will be received on the source table through a peer, HAProxy will try to
  refresh related `<wtable>` entry. If the entry doesn't exist yet, it will be created, else its
  values will be updated as well as its timer. Note that only types that are not involved in
  arithmetic ops such as server_id, server_key and gpt will be written to `<wtable>` to prevent
  processed values from a remote table from interfering with arithmetic operations performed on the
  local target table. (ie: prevent shared cumulative counter from growing indefinitely) One common
  use of this option is to be able to use sticking rules (for server persistence) in a peers cluster
  setup, because matching keys will be learned from remote tables.

The data types that can be associated with an entry via the "store" directive are listed below. It
is important to keep in mind that memory requirements may be important when storing many data types.
Indeed, storing all indicators below at once in each entry can requires hundreds of bytes per entry,
or hundreds of MB for a 1-million entries table. For this reason, the approximate storage size is
mentioned below for each type between brackets after the argument.

Arguments:

- bytes_in_cnt [8 bytes] This is the client to server byte count. It is a positive 64-bit integer
  which counts the cumulative number of bytes received from clients which matched this entry.
  Headers are included in the count. This may be used to limit abuse of upload features on photo or
  video servers. Note that the values are measured when the data enter haproxy, thus the counts are
  not affected by compression.

- bytes_in_rate(`<period>`) [12 bytes] This is a rate counter on bytes from the client to the
  server. It takes an integer parameter `<period>` which indicates in milliseconds the length of the
  period over which the average is measured. It reports the average incoming bytes rate over that
  period, in bytes per period. It may be used to detect users which upload too much and too fast.
  Warning: with large uploads, it is possible that the amount of uploaded data will be counted once
  upon termination, thus causing spikes in the average transfer speed instead of having a smooth
  one. This may partially be smoothed with "option contstats" though this is not perfect. Use of
  bytes_in_cnt is recommended for better fairness.

- bytes_out_cnt [8 bytes] This is the server to client byte count. It is a positive 64-bit integer
  which counts the cumulative number of bytes sent to clients which matched this entry. Headers are
  included in the count. This may be used to limit abuse of bots sucking the whole site. Note that
  the values are measured when the data enter haproxy, thus the counts are not affected by
  compression.

- bytes_out_rate(`<period>`) [12 bytes] This is a rate counter on bytes from the server to the
  client. It takes an integer parameter `<period>` which indicates in milliseconds the length of the
  period over which the average is measured. It reports the average outgoing bytes rate over that
  period, in bytes per period. It may be used to detect users which download too much and too fast.
  Warning: with large transfers, it is possible that the amount of transferred data will be counted
  once upon termination, thus causing spikes in the average transfer speed instead of having a
  smooth one. This may partially be smoothed with "option contstats" though this is not perfect yet.
  Use of bytes_out_cnt is recommended for better fairness.

- conn_cnt [4 bytes] This is the Connection Count. It is a positive 32-bit integer which counts
  the absolute number of connections received from clients which matched this entry. It does not
  mean the connections were accepted, just that they were received.

- conn_cur [4 bytes] This is the Current Connections count. It is a positive 32-bit integer which
  stores the concurrent connection count for the entry. It is incremented once an incoming
  connection matches the entry, and decremented once the connection leaves. That way it is possible
  to know at any time the exact number of concurrent connections for an entry. This type is not
  learned from other peers by default as it wouldn't represent anything given that it would ignore
  the local count. However, in combination with recv-only it can be used to learn the number of
  concurrent connections seen by peers.

- conn_rate(`<period>`) [12 bytes] This is a connection frequency counter. It takes an integer
  parameter `<period>` which indicates in milliseconds the length of the period over which the
  average is measured. It reports the average incoming connection rate over that period, in
  connections per period. The result is an integer which can be matched using ACLs. Whether
  connections are accepted or rejected has no effect on their measurement.

- glitch_cnt [4 bytes] This is the front glitches count. It is a positive 32-bit integer which
  counts the cumulative number of glitches reported on a front connection. Glitches correspond to
  either unusual or unexpected actions (protocol- wise) from the client that could indicate a badly
  defective client or possibly an attacker. As such, this counter can help in order to decide how to
  act with them in such case.

- glitch_rate(`<period>`) [12 bytes] This is a frequency counter on glitches. It takes an integer
  parameter `<period>` which indicates in milliseconds the length of the period over which the
  average is measured. It reports the average front glitches rate over that period. It may be used
  to detect defective clients or potential attackers that perform uncommon or unexpected actions
  from a protocol point of view, provided that HAProxy flagged them them as such.

- gpc(`<nb>`) [4 \* `<nb>` bytes] This is an array of `<nb>` General Purpose Counter elements.
  This is an array of positive 32-bit integers which may be used to count anything. Most of the time
  they will be used as a incremental counters on some entries, for instance to note that a limit is
  reached and trigger some actions. This array is limited to a maximum of 100 elements: gpc0 to
  gpc99, to ensure that the build of a peer update message can fit into the buffer. Users should
  take in consideration that a large amount of counters will increase the data size and the traffic
  load using peers protocol since all data/counters are pushed each time any of them is updated.
  This data_type will exclude the usage of the legacy data_types 'gpc0' and 'gpc1' on the same
  table. Using the 'gpc' array data_type, all 'gpc0' and 'gpc1' related sample fetch functions and
  actions will apply to the two first elements of this array.

- gpc_rate(`<nb>`,`<period>`) [12 \* `<nb>` bytes] This is an array of increment rates of General
  Purpose Counters over a period. Those elements are positive 32-bit integers which may be used for
  anything. Just like `<gpc>`, the count events, but instead of keeping a cumulative number, they
  maintain the rate at which the counter is incremented. Most of the time it will be used to measure
  the frequency of occurrence of certain events (e.g. requests to a specific URL). This array is
  limited to a maximum of 100 elements: gpc_rate(100,`<period>`) allowing the storage of gpc0_rate
  to gpc99_rate, to ensure that the build of a peer update message can fit into the buffer. The
  array cannot contain less than 1 element: use gpc_rate(1,`<period>`) if you want to store only the
  counter rate gpc0_rate. Users should take in consideration that a large amount of counters will
  increase the data size and the traffic load using peers protocol since all data/counters are
  pushed each time any of them is updated. This data_type will exclude the usage of the legacy
  data_types 'gpc0_rate' and 'gpc1_rate' on the same table. Using the 'gpc_rate' array data_type,
  all 'gpc0' and 'gpc1' related fetches and actions will apply to the two first elements of this
  array.

- gpc0 [4 bytes] This is the first General Purpose Counter. It is a positive 32-bit integer
  integer which may be used for anything. Most of the time it will be used to put a special tag on
  some entries, for instance to note that a specific behavior was detected and must be known for
  future matches.

- gpc0_rate(`<period>`) [12 bytes] This is the increment rate of the first General Purpose Counter
  over a period. It is a positive 32-bit integer integer which may be used for anything. Just like
  `<gpc0>`, it counts events, but instead of keeping a cumulative number, it maintains the rate at
  which the counter is incremented. Most of the time it will be used to measure the frequency of
  occurrence of certain events (e.g. requests to a specific URL).

- gpc1 [4 bytes] This is the second General Purpose Counter. It is a positive 32-bit integer
  integer which may be used for anything. Most of the time it will be used to put a special tag on
  some entries, for instance to note that a specific behavior was detected and must be known for
  future matches.

- gpc1_rate(`<period>`) [12 bytes] This is the increment rate of the second General Purpose
  Counter over a period. It is a positive 32-bit integer integer which may be used for anything.
  Just like `<gpc1>`, it counts events, but instead of keeping a cumulative number, it maintains the
  rate at which the counter is incremented. Most of the time it will be used to measure the
  frequency of occurrence of certain events (e.g. requests to a specific URL).

- gpt(`<nb>`) [4 \* `<nb>` bytes] This is an array of `<nb>` General Purpose Tags elements. This
  is an array of positive 32-bit integers which may be used for anything. Most of the time they will
  be used to put a special tags on some entries, for instance to note that a specific behavior was
  detected and must be known for future matches. This array is limited to a maximum of 100 elements:
  gpt(100) allowing the storage of gpt0 to gpt99, to ensure that the build of a peer update message
  can fit into the buffer. The array cannot contain less than 1 element: use gpt(1) if you want to
  to store only the tag gpt0. Users should take in consideration that a large amount of counters
  will increase the data size and the traffic load using peers protocol since all data/counters are
  pushed each time any of them is updated. This data_type will exclude the usage of the legacy
  data_type 'gpt0' on the same table. Using the 'gpt' array data_type, all 'gpt0' related fetches
  and actions will apply to the first element of this array.

- gpt0 [4 bytes] This is the first General Purpose Tag. It is a positive 32-bit integer which may
  be used for anything. Most of the time it will be used to put a special tag on some entries, for
  instance to note that a specific behavior was detected and must be known for future matches.

- http_req_cnt [4 bytes] This is the HTTP request Count. It is a positive 32-bit integer which
  counts the absolute number of HTTP requests received from clients which matched this entry. It
  does not matter whether they are valid requests or not. Note that this is different from sessions
  when keep-alive is used on the client side.

- http_req_rate(`<period>`) [12 bytes] This is a request frequency counter. It takes an integer
  parameter `<period>` which indicates in milliseconds the length of the period over which the
  average is measured. It reports the average HTTP request rate over that period, in requests per
  period. The result is an integer which can be matched using ACLs. It does not matter whether they
  are valid requests or not. Note that this is different from sessions when keep-alive is used on
  the client side.

- http_err_cnt [4 bytes] This is the HTTP request Error Count. It is a positive 32-bit integer
  which counts the absolute number of HTTP requests errors induced by clients which matched this
  entry. Errors are counted on invalid and truncated requests, as well as on denied or tarpitted
  requests, and on failed authentications. If the server responds with 4xx, then the request is also
  counted as an error since it's an error triggered by the client (e.g. vulnerability scan).

- http_err_rate(`<period>`) [12 bytes] This is an HTTP request frequency counter. It takes an
  integer parameter `<period>` which indicates in milliseconds the length of the period over which
  the average is measured. It reports the average HTTP request error rate over that period, in
  requests per period (see http_err_cnt above for what is accounted as an error). The result is an
  integer which can be matched using ACLs.

- http_fail_cnt [4 bytes] This is the HTTP response Failure Count. It is a positive 32-bit integer
  which counts the absolute number of HTTP response failures induced by servers which matched this
  entry. Errors are counted on invalid and truncated responses, as well as any 5xx response other
  than 501 or 505. It aims at being used combined with path or URI to detect service failures.

- http_fail_rate(`<period>`) [12 bytes] This is an HTTP response failure frequency counter. It
  takes an integer parameter `<period>` which indicates in milliseconds the length of the period
  over which the average is measured. It reports the average HTTP response failure rate over that
  period, in requests per period (see http_fail_cnt above for what is accounted as a failure). The
  result is an integer which can be matched using ACLs.

- server_id [4 bytes] This is an integer which holds the numeric ID of the server a request was
  assigned to. It is used by the "stick match", "stick store", and "stick on" rules. It is
  automatically enabled when referenced. It is important to understand that stickiness based on
  learning information has some limitations, including the fact that all learned associations are
  lost upon restart unless peers are properly configured to transfer such information upon restart
  (recommended). In general it can be good as a complement to other stickiness mechanisms but not
  always as the sole mechanism.

- sess_cnt [4 bytes] This is the Session Count. It is a positive 32-bit integer which counts the
  absolute number of sessions received from clients which matched this entry. A session is a
  connection that was accepted by the layer 4 rules ("tcp-request connection").

- sess_rate(`<period>`) [12 bytes] This is a session frequency counter. It takes an integer
  parameter `<period>` which indicates in milliseconds the length of the period over which the
  average is measured. It reports the average incoming session rate over that period, in sessions
  per period. The result is an integer which can be matched using ACLs.

Example:

```shell
# Keep track of counters of up to 1 million IP addresses over 5 minutes
# and store a general purpose counter and the average connection rate
# computed over a sliding window of 30 seconds.
stick-table type ip size 1m expire 5m store gpc0,conn_rate(30s)
```

See also: "stick match", "stick on", "stick store-request", "track-sc", [section 2.5](/haproxy/configuration-basics/#section-2-5) about time
format, [section 11.2](/haproxy/stick-tables-and-peers/#section-11-2) about peers, [section 9.7](/haproxy/filters/#section-9-7) about bandwidth limitations, and [section 7](/haproxy/acls-and-samples/) about ACLs.

## 11.2. Peers declaration {#section-11-2}

It is possible to propagate entries of any data-types in stick-tables between several HAProxy
instances over TCP connections in a multi-master fashion. Each instance pushes its local updates and
insertions to remote peers. The pushed values overwrite remote ones without aggregation.

One exception is the data type "conn_cur" which is never learned from peers by default as it is
supposed to reflect local values. Earlier versions used to synchronize it by default which was known
to cause negative values in active-active setups, and always-growing values upon reloads or
active-passive switches because the local value would reflect more connections than locally present.
However there are some setups where it could be relevant to learn this value from peers, for
instance when the table is a passive remote table solely used to learn/monitor data from it without
relying on it for write-oriented operations or updates. To achieve this, the "recv-only" keyword can
be added on the table declaration. In any case, the "conn_cur" info is always pushed so that
monitoring systems can watch it.

Interrupted exchanges are automatically detected and recovered from the last known point. In
addition, during a soft restart, the old process connects to the new one using such a TCP connection
to push all its entries before the new process tries to connect to other peers. That ensures very
fast replication during a reload, it typically takes a fraction of a second even for large tables.

Note that Server IDs are used to identify servers remotely, so it is important that configurations
look similar or at least that the same IDs are forced on each server on all participants.

<a id="entry-11-2-peers"></a>

**`peers <peersect>`**

```haproxy
peers <peersect>
```

Creates a new peer list with name `<peersect>`. It is an independent section, which is referenced by
one or more stick-tables.

<a id="entry-11-2-bind"></a>

**`bind [<address>]:port [param*]`**

```haproxy
bind [<address>]:port [param*]
bind /<path> [param*]
```

Defines the binding parameters of the local peer of this "peers" section. Such lines are not
supported with "peer" line in the same "peers" section.

<a id="entry-11-2-disabled"></a>

**`disabled`**

```haproxy
disabled
```

Disables a peers section. It disables both listening and any synchronization related to this
section. This is provided to disable synchronization of stick tables without having to comment out
all "peers" references.

<a id="entry-11-2-default-bind"></a>

**`default-bind [param*]`**

```haproxy
default-bind [param*]
```

Defines the binding parameters for the local peer, excepted its address.

<a id="entry-11-2-default-server"></a>

**`default-server [param*]`**

```haproxy
default-server [param*]
```

Change default options for a server in a "peers" section.

Arguments:

```text
<param*>  is a list of parameters for this server. The "default-server"
          keyword accepts an important number of options and has a complete
          section dedicated to it. In a peers section, the transport
          parameters of a "default-server" line are supported. Please refer
          to section 5 for more details, and the "server" keyword below in
          this section for some of the restrictions.
```

See also: "server" and [section 5](/haproxy/bind-and-server-options/) about server options

<a id="entry-11-2-enabled"></a>

**`enabled`**

```haproxy
enabled
```

This re-enables a peers section which was previously disabled via the "disabled" keyword.

<a id="entry-11-2-log"></a>

**`log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]`**

```haproxy
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    <facility> [<level> [<minlevel>]]
```

"peers" sections support the same "log" keyword as for the proxies to log information about the
"peers" listener. See "log" option for proxies for more details.

<a id="entry-11-2-peer"></a>

**`peer <peername> [<address>]:port [param*]`**

```haproxy
peer <peername> [<address>]:port [param*]
peer <peername> /<path> [param*]
```

Defines a peer inside a peers section. If `<peername>` is set to the local peer name (by default
hostname, or forced using "-L" command line option or "localpeer" global configuration setting),
HAProxy will listen for incoming remote peer connection on the provided address. Otherwise, the
address defines where to connect to in order to join the remote peer, and `<peername>` is used at
the protocol level to identify and validate the remote peer on the server side.

During a soft restart, local peer address is used by the old instance to connect the new one and
initiate a complete replication (teaching process).

It is strongly recommended to have the exact same peers declaration on all peers and to only rely on
the "-L" command line argument or the "localpeer" global configuration setting to change the local
peer name. This makes it easier to maintain coherent configuration files across all peers.

You may want to reference some environment variables in the address parameter, see [section 2.3](/haproxy/configuration-basics/#section-2-3) about
environment variables.

Note: "peer" keyword may transparently be replaced by "server" keyword (see "server" keyword
explanation below).

<a id="entry-11-2-server"></a>

**`server <peername> [<address>:<port>] [param*]`**

```haproxy
server <peername> [<address>:<port>] [param*]
server <peername> [/<path>] [param*]
```

As previously mentioned, "peer" keyword may be replaced by "server" keyword with a support for all
"server" parameters found in 5.2 paragraph that are related to transport settings. If the underlying
peer is local, the address parameter must not be present; it must be provided on a "bind" line (see
"bind" keyword of this "peers" section).

A number of "server" parameters are irrelevant for "peers" sections. Peers by nature do not support
dynamic host name resolution nor health checks, hence parameters like "init_addr", "resolvers",
"check", "agent-check", or "track" are not supported. Similarly, there is no load balancing nor
stickiness, thus parameters such as "weight" or "cookie" have no effect.

Example:

```text
 # The old way.
 peers mypeers
     peer haproxy1 192.168.0.1:1024
     peer haproxy2 192.168.0.2:1024
     peer haproxy3 10.2.0.1:1024

 backend mybackend
     mode tcp
     balance roundrobin
     stick-table type ip size 20k peers mypeers
     stick on src

     server srv1 192.168.0.30:80
     server srv2 192.168.0.31:80

Example:
  peers mypeers
     bind 192.168.0.1:1024 ssl crt mycerts/pem
     default-server ssl verify none
     server haproxy1 #local peer
     server haproxy2 192.168.0.2:1024
     server haproxy3 10.2.0.1:1024
```

shards `<shards>`

In some configurations, one would like to distribute the stick-table contents to some peers in place
of sending all the stick-table contents to each peer declared in the "peers" section. In such cases,
"shards" specifies the number of peer involved in this stick-table contents distribution. See also
"shard" server parameter.

<a id="entry-11-2-table"></a>

**`table <tablename> type {ip | integer | string [len <length>] | binary [len <length>]}`**

```haproxy
table <tablename> type {ip | integer | string [len <length>] | binary [len <length>]}
```

      size `<size>` [expire `<expire>`] [write-to `<wtable>`] [nopurge] [store `<data_type>`]*
      [recv-only]

Configure a stickiness table for the current section. This line is parsed exactly the same way as
the "stick-table" keyword in others section, except for the "peers" argument which is not required
here and with an additional mandatory first parameter to designate the stick-table. Contrary to
others sections, there may be several "table" lines in "peers" sections (see also the complete
definition of the "table" and "stick-table" keywords in [section 11.1](/haproxy/stick-tables-and-peers/#section-11-1) above).

Also be aware of the fact that "peers" sections have their own stick-table namespaces to avoid
collisions between stick-table names identical in different "peers" section. This is internally
handled prepending the "peers" sections names to the name of the stick-tables followed by a '/'
character. If somewhere else in the configuration file you have to refer to such stick-tables
declared in "peers" sections you must use the prefixed version of the stick-table name as follows:

```text
peers mypeers
    peer A ...
    peer B ...
    table t1 ...

frontend fe1
    tcp-request content track-sc0 src table mypeers/t1
```

This is also this prefixed version of the stick-table names which must be used to refer to
stick-tables through the CLI.

About "peers" protocol, as only "peers" belonging to the same section may communicate with each
others, there is no need to do such a distinction. Several "peers" sections may declare stick-tables
with the same name. This is shorter version of the stick-table name which is sent over the network.
There is only a '/' character as prefix to avoid stick-table name collisions between stick-tables
declared as backends and stick-table declared in "peers" sections as follows in this weird but
supported configuration:

```text
peers mypeers
    peer A ...
    peer B ...
    table t1 type string size 10m store gpc0

backend t1
    stick-table type string size 10m store gpc0 peers mypeers
```

Here "t1" table declared in "mypeers" section has "mypeers/t1" as global name. "t1" table declared
as a backend as "t1" as global name. But at peer protocol level the former table is named "/t1", the
latter is again named "t1".
