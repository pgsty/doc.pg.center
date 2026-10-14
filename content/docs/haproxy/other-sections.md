---
title: "12. Other Sections"
linkTitle: "12. Other Sections"
weight: 230
description: "Tracing, users, mailers, errors, rings, certificates, ACME, and global health checks"
icon: fa-solid fa-ellipsis
module: [HAPROXY]
categories: [Reference]
aliases:
  - /haproxy/configuration/other-sections/
  - /docs/haproxy/configuration/other-sections/
  - /haproxy/other-sections/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 12"
---

The sections described below are less commonly used and usually support only a few parameters. There
is no implicit relation between any of them. They're all started using a single keyword. None of
them is permitted before a "global" section. The support for some of them might be conditioned by
build options (e.g. anything SSL-related).

## 12.1. Traces {#section-12-1}

For debugging purpose, it is possible to activate traces on an HAProxy's subsystem. This will dump
debug messages about a specific subsystem. It is a very powerful tool to diagnose issues. Traces can
be dynamically configured via the CLI. It is also possible to predefined some settings in the
configuration file, in dedicated "traces" sections. More details about traces can be found in the
management guide. It remains a developer tools used during complex debugging sessions. It is pretty
verbose and have a cost, so use it with caution. And because it is a developer tool, there is no
warranty about the backward compatibility of this section.

<a id="entry-12-1-traces"></a>

**`traces`**

```haproxy
traces
```

Starts a new traces section. One or multiple "traces" section may be used. All direcitives are
evaluated in the declararion order, the last ones overriding previous ones.

<a id="entry-12-1-trace"></a>

**`trace <source> <args...>`**

```haproxy
trace <source> <args...>
```

Configures on "trace" subsystem. Each of them can be found in the management manual, and follow the
exact same syntax. Any output that the "trace" command would produce will be emitted during the
parsing step of the section. Most of the time these will be errors and warnings, but certain
incomplete commands might list permissible choices. This command is not meant for regular use, it
will generally only be suggested by developers along complex debugging sessions. It is important to
keep in mind that depending on the trace level and details, enabling traces can severely degrade the
global performance. Please refer to the management manual for the statements syntax.

Example:

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

## 12.2. Userlists {#section-12-2}

It is possible to control access to frontend/backend/listen sections or to http stats by allowing
only authenticated and authorized users. To do this, it is required to create at least one userlist
and to define users.

<a id="entry-12-2-userlist"></a>

**`userlist <listname>`**

```haproxy
userlist <listname>
```

Creates new userlist with name `<listname>`. Many independent userlists can be used to store
authentication & authorization data for independent customers.

<a id="entry-12-2-group"></a>

**`group <groupname> [users <user>,<user>,(...)]`**

```haproxy
group <groupname> [users <user>,<user>,(...)]
```

Adds group `<groupname>` to the current userlist. It is also possible to attach users to this group
by using a comma separated list of names proceeded by "users" keyword.

<a id="entry-12-2-user"></a>

**`user <username> [password|insecure-password <password>]`**

```haproxy
user <username> [password|insecure-password <password>]
                [groups <group>,<group>,(...)]
```

Adds user `<username>` to the current userlist. Both secure (encrypted) and insecure (unencrypted)
passwords can be used. Encrypted passwords are evaluated using the crypt(3) function, so depending
on the system's capabilities, different algorithms are supported. For example, modern Glibc based
Linux systems support MD5, SHA-256, SHA-512, and, of course, the classic DES-based method of
encrypting passwords.

Attention: Be aware that using encrypted passwords might cause significantly increased CPU usage,
depending on the number of requests, and the algorithm used. For any of the hashed variants, the
password for each request must be processed through the chosen algorithm, before it can be compared
to the value specified in the config file. Most current algorithms are deliberately designed to be
expensive to compute to achieve resistance against brute force attacks. They do not simply salt/hash
the clear text password once, but thousands of times. This can quickly become a major factor in
HAProxy's overall CPU consumption, and can even lead to application crashes!

To address the high CPU usage of hash functions, one approach is to reduce the number of rounds of
the hash function (SHA family algorithms) or decrease the "cost" of the function, if the algorithm
supports it.

As a side note, musl (e.g. Alpine Linux) implementations are known to be slower than their glibc
counterparts when calculating hashes, so you might want to consider this aspect too.

All passwords are considered normal arguments and are therefore subject to regular [section 2.2](/docs/haproxy/configuration-basics/#section-2-2)
Quoting and escaping. Single quoting passwords is therefore recommended.

Example:

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

Please note that both lists are functionally identical.

## 12.3. Mailers {#section-12-3}

It is possible to send email alerts when the state of servers changes. If configured email alerts
are sent to each mailer that is configured in a mailers section. Email is sent to mailers through
Lua (see examples/lua/mailers.lua).

<a id="entry-12-3-mailers"></a>

**`mailers <mailersect>`**

```haproxy
mailers <mailersect>
```

Creates a new mailer list with the name `<mailersect>`. It is an independent section which is
referenced by one or more proxies.

<a id="entry-12-3-mailer"></a>

**`mailer <mailername> <ip>:<port>`**

```haproxy
mailer <mailername> <ip>:<port>
```

Defines a mailer inside a mailers section.

Example:

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

Defines the time available for a mail/connection to be made and send to the mail-server. If not
defined the default value is 10 seconds. To allow for at least two SYN-ACK packets to be send during
initial TCP handshake it is advised to keep this value above 4 seconds.

Example:

```text
mailers mymailers
    timeout mail 20s
    mailer smtp1 192.168.0.1:587
```

## 12.4. HTTP-errors {#section-12-4}

It is possible to globally declare several groups of HTTP errors, to be imported afterwards in any
proxy section. Same group may be referenced at several places and can be fully or partially
imported.

<a id="entry-12-4-http-errors"></a>

**`http-errors <name>`**

```haproxy
http-errors <name>
```

Create a new http-errors group with the name `<name>`. It is an independent section that may be
referenced by one or more proxies using its name.

<a id="entry-12-4-errorfile"></a>

**`errorfile <code> <file>`**

```haproxy
errorfile <code> <file>
```

Associate a file contents to an HTTP error code

Arguments:

```text
<code>    is the HTTP status code. Currently, HAProxy is capable of
          generating codes 200, 400, 401, 403, 404, 405, 407, 408, 410,
          425, 429, 500, 501, 502, 503, and 504.

<file>    designates a file containing the full HTTP response. It is
          recommended to follow the common practice of appending ".http" to
          the filename so that people do not confuse the response with HTML
          error pages, and to use absolute paths, since files are read
          before any chroot is performed.
```

Please referrers to "errorfile" keyword in [section 4](/docs/haproxy/proxies/) for details.

Example:

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

## 12.5. Rings {#section-12-5}

It is possible to globally declare ring-buffers, to be used as target for log servers or traces.

<a id="entry-12-5-ring"></a>

**`ring <ringname>`**

```haproxy
ring <ringname>
```

Creates a new ring-buffer with name `<ringname>`.

<a id="entry-12-5-backing-file"></a>

**`backing-file <path>`**

```haproxy
backing-file <path>
```

This replaces the regular memory allocation by a RAM-mapped file to store the ring. This can be
useful for collecting traces or logs for post-mortem analysis, without having to attach a slow
client to the CLI. Newer contents will automatically replace older ones so that the latest contents
are always available. The contents written to the ring will be visible in that file once the process
stops (most often they will even be seen very soon after but there is no such guarantee since writes
are not synchronous).

When this option is used, the total storage area is reduced by the size of the "struct ring" that
starts at the beginning of the area, and that is required to recover the area's contents. The file
will be created with the starting user's ownership, with mode 0600 and will be of the size
configured by the "size" directive. When the directive is parsed (thus even during config checks),
any existing non-empty file will first be renamed with the extra suffix ".bak", and any previously
existing file with suffix ".bak" will be removed. This ensures that instant reload or restart of the
process will not wipe precious debugging information, and will leave time for an admin to spot this
new ".bak" file and to archive it if needed. As such, after a crash the file designated by `<path>`
will contain the freshest information, and if the service is restarted, the "`<path>`.bak" file will
have it instead. This means that the total storage capacity required will be double of the ring
size. Failures to rotate the file are silently ignored, so placing the file into a directory without
write permissions will be sufficient to avoid the backup file if not desired.

WARNING: there are stability and security implications in using this feature. First, backing the
ring to a slow device (e.g. physical hard drive) may cause perceptible slowdowns during accesses,
and possibly even panics if too many threads compete for accesses. Second, an external process
modifying the area could cause the haproxy process to crash or to overwrite some of its own memory
with traces. Third, if the file system fills up before the ring, writes to the ring may cause the
process to crash.

The information present in this ring are structured and are NOT directly readable using a text
editor (even though most of it looks barely readable). The output of this file is only intended for
developers.

<a id="entry-12-5-description"></a>

**`description <text>`**

```haproxy
description <text>
```

The description is an optional description string of the ring. It will appear on CLI. By default,
`<name>` is reused to fill this field.

<a id="entry-12-5-format"></a>

**`format <format>`**

```haproxy
format <format>
```

Format used to store events into the ring buffer.

Arguments:

```text
<format> is the log format used when generating syslog messages. It may be
         one of the following:

  iso     A message containing only the ISO date, followed by the text.
          The PID, process name and system name are omitted. This is
          designed to be used with a local log server.

  local   Analog to rfc3164 syslog message format except that hostname
          field is stripped. This is the default.
          Note: option "log-send-hostname" switches the default to
          rfc3164.

  raw     A message containing only the text. The level, PID, date, time,
          process name and system name are omitted. This is designed to be
          used in containers or during development, where the severity
          only depends on the file descriptor used (stdout/stderr). This
          is the default.

  rfc3164 The RFC3164 syslog message format.
          (https://tools.ietf.org/html/rfc3164)

  rfc5424 The RFC5424 syslog message format.
          (https://tools.ietf.org/html/rfc5424)

  short   A message containing only a level between angle brackets such as
          '<3>', followed by the text. The PID, date, time, process name
          and system name are omitted. This is designed to be used with a
          local log server. This format is compatible with what the systemd
          logger consumes.

 priority A message containing only a level plus syslog facility between angle
          brackets such as '<63>', followed by the text. The PID, date, time,
          process name and system name are omitted. This is designed to be used
          with a local log server.

  timed   A message containing only a level between angle brackets such as
          '<3>', followed by ISO date and by the text. The PID, process
          name and system name are omitted. This is designed to be
          used with a local log server.
```

<a id="entry-12-5-maxlen"></a>

**`maxlen <length>`**

```haproxy
maxlen <length>
```

The maximum length of an event message stored into the ring, including formatted header. If an event
message is longer than `<length>`, it will be truncated to this length.

<a id="entry-12-5-server"></a>

**`server <name> <address> [param*]`**

```haproxy
server <name> <address> [param*]
```

Used to configure a syslog tcp server to forward messages from ring buffer. This supports for all
"server" parameters found in 5.2 paragraph. Some of these parameters are irrelevant for "ring"
sections. Important point: there is little reason to add more than one server to a ring, because all
servers will receive the exact same copy of the ring contents, and as such the ring will progress at
the speed of the slowest server. If one server does not respond, it will prevent old messages from
being purged and may block new messages from being inserted into the ring. The proper way to send
messages to multiple servers is to use one distinct ring per log server, not to attach multiple
servers to the same ring. Note that specific server directive "log-proto" is used to set the
protocol used to send messages.

<a id="entry-12-5-size"></a>

**`size <size>`**

```haproxy
size <size>
```

This is the optional size in bytes for the ring-buffer. Default value is set to BUFSIZE.

<a id="entry-12-5-timeout-connect"></a>

**`timeout connect <timeout>`**

```haproxy
timeout connect <timeout>
```

Set the maximum time to wait for a connection attempt to a server to succeed.

Arguments:

```text
<timeout> is the timeout value specified in milliseconds by default, but
          can be in any other unit if the number is suffixed by the unit,
          as explained at the top of this document.
```

<a id="entry-12-5-timeout-server"></a>

**`timeout server <timeout>`**

```haproxy
timeout server <timeout>
```

Set the maximum time for pending data staying into output buffer.

Arguments:

```text
<timeout> is the timeout value specified in milliseconds by default, but
          can be in any other unit if the number is suffixed by the unit,
          as explained at the top of this document.
```

Example:

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

## 12.6. Log forwarding {#section-12-6}

It is possible to declare one or multiple log forwarding section, HAProxy will forward all received
log messages to a log servers list.

<a id="entry-12-6-log-forward"></a>

**`log-forward <name>`**

```haproxy
log-forward <name>
```

Creates a new log forwarder proxy identified as `<name>`.

<a id="entry-12-6-backlog"></a>

**`backlog <conns>`**

```haproxy
backlog <conns>
```

Give hints to the system about the approximate listen backlog desired size on connections accept.

<a id="entry-12-6-bind"></a>

**`bind <addr> [param*]`**

```haproxy
bind <addr> [param*]
```

Used to configure a stream log listener to receive messages to forward. This supports the "bind"
parameters found in 5.1 paragraph including those about ssl but some statements such as "alpn" may
be irrelevant for syslog protocol over TCP. Those listeners support both "Octet Counting" and
"Non-Transparent-Framing" modes as defined in rfc-6587.

<a id="entry-12-6-dgram-bind"></a>

**`dgram-bind <addr> [param*]`**

```haproxy
dgram-bind <addr> [param*]
```

Used to configure a datagram log listener to receive messages to forward. Addresses must be in IPv4
or IPv6 form,followed by a port. This supports for some of the "bind" parameters found in 5.1
paragraph among which "interface", "namespace" or "transparent", the other ones being silently
ignored as irrelevant for UDP/syslog case.

<a id="entry-12-6-log-global"></a>

**`log global`**

```haproxy
log global
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    <facility> [<level> [<minlevel>]]
```

Used to configure target log servers. See more details on proxies documentation. If no format
specified, HAProxy tries to keep the incoming log format. Configured facility is ignored, except if
incoming message does not present a facility but one is mandatory on the outgoing format. If there
is no timestamp available in the input format, but the field exists in output format, HAProxy will
use the local date.

Example:

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

Fix the maximum number of concurrent connections on a log forwarder. 10 is the default.

<a id="entry-12-6-timeout-client"></a>

**`timeout client <timeout>`**

```haproxy
timeout client <timeout>
```

Set the maximum inactivity time on the client side.

<a id="entry-12-6-option-assume-rfc6587-ntf"></a>

**`option assume-rfc6587-ntf`**

```haproxy
option assume-rfc6587-ntf
```

Directs HAProxy to treat incoming TCP log streams always as using non-transparent framing. This
option simplifies the framing logic and ensures consistent handling of messages, particularly useful
when dealing with improperly formed starting characters.

<a id="entry-12-6-option-dont-parse-log"></a>

**`option dont-parse-log`**

```haproxy
option dont-parse-log
```

Enables HAProxy to relay syslog messages without attempting to parse and restructure them, useful
for forwarding messages that may not conform to traditional formats. This option should be used with
the format raw setting on destination log targets to ensure the original message content is
preserved.

<a id="entry-12-6-option-host"></a>

**`option host { replace | fill | keep | append }`**

```haproxy
option host { replace | fill | keep | append }
```

Set the host strategy that should be used on the log-forward section regarding syslog hostname field
for outbound rfc3164 or rfc5424 messages.

      replace If input message already contains a value for the hostname field,
              we replace it by the source IP address from the sender.
              If input message doesn't contain a value for the hostname field
              (ie: '-' as input rfc5424 message or non compliant rfc3164 or
              rfc5424 message), we use the source IP address from the sender as
              hostname field.

      fill    If input message already contains a value for the hostname field,
              we keep it.
              If input message doesn't contain a value for the hostname field
              (ie: '-' as input rfc5424 message or non compliant rfc3164 or
              rfc5424 message), we use the source IP address from the sender as
              hostname field.
              (This is the default)

      keep    If input message already contains a value for the hostname field,
              we keep it.
              If input message doesn't contain a value for the hostname field,
              we set it to 'localhost' (rfc3164) or '-' (rfc5424).

      append  If input message already contains a value for the hostname field,
              we append a comma followed by the IP address from the sender.
              If input message doesn't contain a value for the hostname field,
              we use the source IP address from the sender.

For all options above, if the source IP address from the sender is not available (ie: UNIX/ABNS
socket), then the resulting strategy is "keep".

Note that this option is only relevant for rfc3164 or rfc5424 destination log format. Else setting
the option will have no visible effect.

## 12.7. Certificate Storage {#section-12-7}

HAProxy uses an internal storage mechanism to load and store certificates used in the configuration.
This storage can be configured by using a "crt-store" section. It allows to configure certificate
definitions and which files should be loaded in it. A certificate definition must be written before
it is used elsewhere in the configuration.

crt-store [`<name>`]

The "crt-store" takes an optional name in argument. If a name is specified, every certificate of
this store must be referenced using "@`<name>`/`<crt>`" or "@`<name>`/`<alias>`".

Files in the certificate storage can also be updated dynamically with the CLI. See "set ssl cert" in
the [section 9.3](/docs/haproxy/statistics-and-monitoring/#section-9-3) of the management guide.

The following keywords are supported in the "crt-store" section:

- crt-base
- key-base
- load

<a id="entry-12-7-crt-base"></a>

**`crt-base <dir>`**

```haproxy
crt-base <dir>
```

Assigns a default directory to fetch SSL certificates from when a relative path is used with "crt"
directives. Absolute locations specified prevail and ignore "crt-base". When used in a crt-store,
the crt-base of the global section is ignored.

<a id="entry-12-7-key-base"></a>

**`key-base <dir>`**

```haproxy
key-base <dir>
```

Assigns a default directory to fetch SSL private keys from when a relative path is used with "key"
directives. Absolute locations specified prevail and ignore "key-base". When used in a crt-store,
the key-base of the global section is ignored.

<a id="entry-12-7-load"></a>

**`load [crt <filename>] [param*]`**

```haproxy
load [crt <filename>] [param*]
```

Load SSL files in the certificate storage. For the parameter list, see section "12.7.1. Load
options"

Example:

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

### 12.7.1. Load options {#section-12-7-1}

Load SSL files in the certificate storage. The load keyword can take multiple parameters which are
listed below. These keywords are also usable in a crt-list.

<a id="entry-12-7-1-crt"></a>

**`crt <filename>`**

```haproxy
crt <filename>
```

This argument is mandatory, it loads a PEM which must contain the public certificate but could also
contain the intermediate certificates and the private key. If no private key is provided in this
file, a key can be provided with the "key" keyword.

<a id="entry-12-7-1-acme"></a>

**`acme <string>`**

```haproxy
acme <string>
```

This option allows to configure the ACME protocol for a given certificate. This is an experimental
feature which needs the "expose-experimental-directives" keyword in the global section.

When using the "acme" keyword in a crt-store, it is possible to start without an existing
certificate on the disk. Instead, a temporary key pair will be used until the ACME certificate is
generated. This behavior is exclusives to crt-stores, neither a crt-list line nor an ssl-f-use line
can achieve the same without declaring a crt-store first.

See also [Section 12.8](/docs/haproxy/other-sections/#section-12-8) ("ACME") and "domains" in this section.

<a id="entry-12-7-1-alias"></a>

**`alias <string>`**

```haproxy
alias <string>
```

Optional argument. Allow to name the certificate with an alias, so it can be referenced with it in
the configuration. An alias must be prefixed with '@/' when called elsewhere in the configuration.

<a id="entry-12-7-1-domains"></a>

**`domains <string>`**

```haproxy
domains <string>
```

Configure the list of domains that will be used for ACME certificates. The first domain of the list
is used as the CN. Domains are separated by commas in the list.

See also [Section 12.8](/docs/haproxy/other-sections/#section-12-8) ("ACME") and "acme" in this section.

Example:

```text
load crt "example.com.pem" acme LE domains "bar.example.com,foo.example.com"
```

<a id="entry-12-7-1-ips"></a>

**`ips <string>`**

```haproxy
ips <string>
```

Configure the list of IP addresses that will be included as IP SANs in the ACME certificate. IP
addresses are separated by commas in the list.

Generating a certificate with IPs might require the use of the "shortlived" profile.

See also [Section 12.8](/docs/haproxy/other-sections/#section-12-8) ("ACME"), "acme" and "domains" in this section.

Example:

```text
load crt "server.pem" acme LE ips "192.0.2.1,2001:db8::1"
```

<a id="entry-12-7-1-key"></a>

**`key <filename>`**

```haproxy
key <filename>
```

This argument is optional. Load a private key in PEM format. If a private key was already defined in
"crt", it will overwrite it.

<a id="entry-12-7-1-ocsp"></a>

**`ocsp <filename>`**

```haproxy
ocsp <filename>
```

This argument is optional, it loads an OCSP response in DER format. It can be updated with the CLI.

<a id="entry-12-7-1-issuer"></a>

**`issuer <filename>`**

```haproxy
issuer <filename>
```

This argument is optional. Load the OCSP issuer in PEM format. In order to identify which
certificate an OCSP Response applies to, the issuer's certificate is necessary. If the issuer's
certificate is not found in the "crt" file, it could be loaded from a file with this argument.

<a id="entry-12-7-1-sctl"></a>

**`sctl <filename>`**

```haproxy
sctl <filename>
```

This argument is optional. Support for Certificate Transparency (RFC6962) TLS extension is enabled.
The file must contain a valid Signed Certificate Timestamp List, as described in RFC. File is parsed
to check basic syntax, but no signatures are verified.

<a id="entry-12-7-1-ocsp-update"></a>

**`ocsp-update [ off | on ]`**

```haproxy
ocsp-update [ off | on ]
```

Enable automatic OCSP response update when set to 'on', disable it otherwise. Its value defaults to
'off'. To enable the OCSP auto update on a bind line, you can use this option in a crt-store or you
can use the global option "tune.ocsp-update.mode". If a given certificate is used in multiple
crt-lists with different values of the 'ocsp-update' set, an error will be raised. Likewise, if a
certificate inherits from the global option on a bind line and has an incompatible explicit
'ocsp-update' option set in a crt-list, the same error will be raised.

Examples:

Here is an example configuration enabling it with a crt-list:

haproxy.cfg:

```text
frontend fe
    bind :443 ssl crt-list haproxy.list
```

haproxy.list:

```text
server_cert.pem [ocsp-update on] foo.bar
```

Here is an example configuration enabling it with a crt-store:

haproxy.cfg:

```text
crt-store
  load crt foobar.pem ocsp-update on

frontend fe
    bind :443 ssl crt foobar.pem
```

When the option is set to 'on', we will try to get an ocsp response whenever an ocsp uri is found in
the frontend's certificate. The only limitation of this mode is that the certificate's issuer will
have to be known in order for the OCSP certid to be built. Each OCSP response will be updated at
least once an hour, and even more frequently if a given OCSP response has an expire date earlier
than this one hour limit. A minimum update interval of 5 minutes will still exist in order to avoid
updating too often responses that have a really short expire time or even no 'Next Update' at all.
Because of this hard limit, please note that when auto update is set to 'on', any OCSP response
loaded during init will not be updated until at least 5 minutes, even if its expire time ends before
now+5m. This should not be too much of a hassle since an OCSP response must be valid when it gets
loaded during init (its expire time must be in the future) so it is unlikely that this response
expires in such a short time after init. On the other hand, if a certificate has an OCSP uri
specified and no OCSP response, setting this option to 'on' for the given certificate will ensure
that the OCSP response gets fetched automatically right after init. The default minimum and maximum
delays (5 minutes and 1 hour respectively) can be configured by the "ocsp-update.maxdelay" and
"ocsp-update.mindelay" global options.

Whenever an OCSP response is updated by the auto update task or following a call to the "update ssl
ocsp-response" CLI command, a dedicated log line is emitted. It follows a dedicated format that
contains the following header "`<OCSP-UPDATE>`" and is followed by specific OCSP-related
information: - the path of the corresponding frontend certificate - a numerical update status - a
textual update status - the number of update failures for the given response - the number of update
successes for the givan response See "show ssl ocsp-updates" CLI command for a full list of error
codes and error messages. This line is emitted regardless of the success or failure of the concerned
OCSP response update. The OCSP request/response is sent and received through an http_client instance
that has the dontlog-normal option set and that uses the regular HTTP log format in case of error
(unreachable OCSP responder for instance). If such an error occurs, another log line that contains
HTTP-related information will then be emitted alongside the "regular" OCSP one (which will likely
have "HTTP error" as text status). But if a purely HTTP error happens (unreachable OCSP responder
for instance), an extra log line that follows the regular HTTP log-format will be emitted. Here are
two examples of such log lines, with a successful OCSP update log line first and then an example of
an HTTP error with the two different lines (lines were spit and the URL was shortened for
readability):

```text
<133>Mar  6 11:16:53 haproxy[14872]: <OCSP-UPDATE> /path_to_cert/foo.pem 1 \
        "Update successful" 0 1

<133>Mar  6 11:18:55 haproxy[14872]: <OCSP-UPDATE> /path_to_cert/bar.pem 2 \
        "HTTP error" 1 0
<133>Mar  6 11:18:55 haproxy[14872]: -:- [06/Mar/2023:11:18:52.200] \
        <OCSP-UPDATE> -/- 2/0/-1/-1/3009 503 217 - - SC-- 0/0/0/0/3 0/0 {} \
        "GET http://127.0.0.1:12345/MEMwQT HTTP/1.1"
```

Troubleshooting: A common error that can happen with Let's Encrypt certificates is if the DNS
resolution provides an IPv6 address and your system does not have a valid outgoing IPv6 route. In
such a case, you can either create the appropriate route or set the "httpclient.resolvers.prefer
ipv4" option in the global section. In case of "OCSP response check failure" error, you might want
to check that the issuer certificate that you provided is valid. A more precise error message might
also be displayed between parenthesis after the "generic" error message. It can happen for "OCSP
response check failure" or "Error during insertion" errors.

<a id="entry-12-7-1-jwt"></a>

**`jwt [ off | on ]`**

```haproxy
jwt [ off | on ]
```

Allow for this certificate to be used for JWT validation or decryption via the "jwt_verify_cert",
"jwt_decrypt_cert" or "jwt_decrypt" converters when set to 'on'. Its value defaults to 'off'.

When set to 'on' for a given certificate, the CLI command "del ssl cert" will not work. In order to
be deleted, a certificate must not be used, either for SSL handshakes or JWT validation.

This option can be changed during runtime via the "add ssl jwt" and "del ssl jwt" CLI commands. See
also "show ssl jwt" CLI command.

<a id="entry-12-7-1-generate-dummy"></a>

**`generate-dummy [ off | on ]`**

```haproxy
generate-dummy [ off | on ]
```

Allow the generation of a private key and its self-signed certificate at parsing time when set to
'on'. This may be useful if one does not have a certificate at disposal during testing phase for
instance. In this case, "keytype", "bits" and "curves" may be used to customize the private key.
When not used, the default value is 'off'. (also see "keytype", "bits" and "curves").

<a id="entry-12-7-1-keytype"></a>

**`keytype [ RSA | ECDSA ]`**

```haproxy
keytype [ RSA | ECDSA ]
```

Allow the selection of the private key type used to generate at parsing time a self-signed
certificate. This is the case if "generate-dummy" is set to 'on' for this certificate. When not
used, the default is 'RSA'. (also see "generate-dummy").

<a id="entry-12-7-1-bits"></a>

**`bits <number>`**

```haproxy
bits <number>
```

Configure the number of bits to generate an RSA self-signed certificate when "generate-dummy" is set
to 'on' for this self-signed certificate and "keytype" is set to 'RSA'. When not used, the default
is 2048. (also see "generate-dummy").

<a id="entry-12-7-1-curves"></a>

**`curves <string>`**

```haproxy
curves <string>
```

Configure the curves when "generate-dummy" is set to 'on' and "keytype" is set to 'ECDSA" for this
self-signed certificate. The default is 'P-384'.

## 12.8. ACME {#section-12-8}

acme `<name>`

The ACME protocol can be configured using the "acme" section. The section takes a "`<name>`"
argument, which is used to link a certificate to the section.

The ACME section allows to configure HAProxy as an ACMEv2 client. This feature is experimental
meaning that "expose-experimental-directives" must be in the global section so this can be used.

A guide is available on the HAProxy wiki
<https://github.com/haproxy/wiki/wiki/ACME:--native-haproxy>

Current limitations: <a id="entry-12-8-the-feature-is"></a>

**`- The feature is limited to the http-01, dns-01 or dns-persist-01 challenges`**

```haproxy
- The feature is limited to the http-01, dns-01 or dns-persist-01 challenges
```

for now. http-01 is completely handled by HAProxy, but dns-01 and dns-persist-01 needs either the
dataplaneAPI or another 3rd party tool to talk to a DNS provider API. dns-persist-01 only needs the
TXT entry to be set once, so it could be set manually without a tool.
<a id="entry-12-8-it-is-possible"></a>

**`- It is possible to start without an existing certificate on the disk. To do`**

```haproxy
- It is possible to start without an existing certificate on the disk. To do
```

so, the certificate must configured in a crt-store. When using the "acme" keyword in a crt-store, a
temporary key pair will be used until the ACME certificate is generated.
<a id="entry-12-8-the-current-haproxy"></a>

**`- The current HAProxy architecture is a non-blocking model, access to the disk`**

```haproxy
- The current HAProxy architecture is a non-blocking model, access to the disk
```

is not supposed to be done after the configuration is loaded, because it could block the event loop,
blocking the traffic on the same thread. Meaning that the certificates and keys generated from
HAProxy will need to be dumped from outside HAProxy using "dump ssl cert" on the stats socket. It's
possible to automate the dump of the certificates by using the dataplaneAPI or the
haproxy-dump-certs script provided in the admin/cli/ directory.

The ACME scheduler starts at HAProxy startup, it will loop over the certificates and start an ACME
renewal task when the notAfter task is past curtime + (notAfter - notBefore) / 12, or 7 days if
notBefore is not defined. The scheduler will then sleep and wakeup after 12 hours. It is possible to
start manually a renewal task with "acme renew'. See also "acme status" in the management guide.

The following keywords are usable in the ACME section:

<a id="entry-12-8-account-key"></a>

**`account-key <filename>`**

```haproxy
account-key <filename>
```

Configure the path to the account key. The key need to be generated before launching HAProxy. If no
account keyword is used, the acme section will try to load a filename using the section name
"`<name>`.account.key". If the file doesn't exist, HAProxy will generate one, using the parameters
from the acme section.

You can also generate manually an RSA private key with openssl:

```text
openssl genrsa -out account.key 2048
```

Or an ecdsa one:

```text
openssl ecparam -name secp384r1 -genkey -noout -out account.key
```

<a id="entry-12-8-acme-vars"></a>

**`acme-vars <string>`**

```haproxy
acme-vars <string>
```

Pass arbitrary variables to the external DNS provisioning tool (e.g. the dataplaneAPI) via the
"dpapi" sink. The semantics are tool-specific; refer to your DNS provisioning tool's documentation.

This keyword is only meaningful when the challenge type is "dns-01" or "dns-persist-01".

See also: "challenge", "provider-name"

<a id="entry-12-8-bits"></a>

**`bits <number>`**

```haproxy
bits <number>
```

Configure the number of bits to generate an RSA certificate. Default to 2048. Setting a too high
value can trigger a warning if your machine is not powerful enough. (This can be configured with
"warn-blocked-traffic-after" but blocking the traffic too long could trigger the watchdog.)

<a id="entry-12-8-challenge"></a>

**`challenge <string>`**

```haproxy
challenge <string>
```

Takes a challenge type as parameter, this must be http-01, dns-01 or dns-persist-01. When not used
the default is http-01.

dns-persist-01 implements draft-ietf-acme-dns-persist. Unlike dns-01, it uses a static TXT record at
"\_validation-persist.`<domain>`" that is set once and never changes between renewals. The record
must contain the account URI and an optional policy. This challenge type does not require write
access to the DNS provider API on each renewal.

<a id="entry-12-8-challenge-ready"></a>

**`challenge-ready <value>[,<value>]*`**

```haproxy
challenge-ready <value>[,<value>]*
```

Configure the conditions that must be met before notifying the ACME server that a dns-01 challenge
is ready to be validated. Accepted values are:

```text
cli  - wait for an operator to signal readiness via the CLI command
       "acme challenge_ready <crt> domain <domain>" on the master CLI or
       the stats socket. This allows an external DNS provisioning tool to
       confirm that the TXT record has been set before HAProxy proceeds.

dns  - perform a DNS pre-check by resolving the TXT record for
       "_acme-challenge.<domain>" using the configured "default" resolvers
       section, not the authoritative name servers. The challenge is not
       submitted until the TXT record matches the expected token. Results
       may therefore be affected by DNS caching at the resolver level. The
       delay between resolution attempts is controlled by "dns-delay". This
       option is independent of the CLI command, so no human intervention
       is required.

       For dns-01, the TXT record at "_acme-challenge.<domain>" is
       resolved and must match the expected token. For dns-persist-01,
       the TXT record at "_validation-persist.<domain>" is resolved and
       only its presence is checked.

delay - apply an initial wait of "dns-delay" before proceeding. Without
        "dns", the challenge is submitted after the delay expires. When
        combined with "dns", the initial wait is applied before starting
        the DNS pre-checks.

none - no readiness condition; the challenge is submitted to the ACME
       server immediately without waiting for any external confirmation.
       This option cannot be combined with others.
```

Multiple values can be combined with a comma. When several conditions are specified, HAProxy
processes them in the following order: first it waits for the CLI confirmation ("cli"), then applies
the initial delay ("delay"), then performs the DNS pre-checks ("dns").

This option is only compatible with the dns-01 and dns-persist-01 challenge types.

When "challenge" is set to "dns-01" and this option is not configured, the default is "cli".

When "challenge" is set to "dns-persist-01" and this option is not configured, the default is
"dns,delay".

When "challenge" is set to "dns-persist-01", an initial opportunistic DNS check is always performed
before the challenge-ready conditions are evaluated. Since the "\_validation-persist.`<domain>`" TXT
record is set once and never changes between renewals, HAProxy checks at renewal time whether the
record is already present. If the check succeeds for all domains, the challenge is submitted
immediately without going through the challenge-ready steps (cli, delay, dns). If the check fails,
HAProxy falls back to the normal challenge-ready flow.

Example:

```shell
# Wait for CLI confirmation, then verify DNS propagation
challenge-ready cli,dns
```

<a id="entry-12-8-contact"></a>

**`contact <string>`**

```haproxy
contact <string>
```

The contact email that will be associated to the account key in the CA.

<a id="entry-12-8-curves"></a>

**`curves <string>`**

```haproxy
curves <string>
```

When using the ECDSA keytype, configure the curves. The default is P-384.

<a id="entry-12-8-directory"></a>

**`directory <string>`**

```haproxy
directory <string>
```

This keyword configures the directory URL for the CA used by this acme section. This keyword is
mandatory as there is no default URL.

Example:

```text
directory https://acme-staging-v02.api.letsencrypt.org/directory
```

<a id="entry-12-8-dns-delay"></a>

**`dns-delay <time>`**

```haproxy
dns-delay <time>
```

Configure the delay used by "challenge-ready" conditions "delay" and "dns". The value is a time
expressed in HAProxy time format (e.g. "5m", "300s"). Default is 30 seconds.

Its role depends on the "challenge-ready" conditions in use:

```text
delay     - the challenge is submitted after this delay expires, without
            any DNS pre-check.

dns       - the delay between two consecutive DNS resolution attempts.
            The first probe fires immediately without any initial wait.

dns+delay - the initial wait before the first DNS resolution attempt, and
            the delay between subsequent retries.
```

Note that the resolution goes through the configured "default" resolvers section, not the
authoritative name servers. Results may therefore still be affected by DNS caching at the resolver
level.

<a id="entry-12-8-dns-timeout"></a>

**`dns-timeout <time>`**

```haproxy
dns-timeout <time>
```

When "challenge-ready" includes "dns", configure the maximum time allowed to successfully resolve
the TXT record before aborting the challenge. The value is a time expressed in HAProxy time format
(e.g. "10m", "600s"). Default is 600 seconds.

The timer starts from the moment the first DNS resolution attempt is triggered (after the initial
"dns-delay"). If the next resolution attempt would be triggered after the timeout has elapsed, the
challenge is aborted with an error. This prevents an infinite retry loop when DNS propagation fails.

See also: "dns-delay"

<a id="entry-12-8-keytype"></a>

**`keytype <string>`**

```haproxy
keytype <string>
```

Configure the type of key that will be generated. Value can be either "RSA" or "ECDSA". You can also
configure the "curves" for ECDSA and the number of "bits" for RSA. By default EC384 keys are
generated.

<a id="entry-12-8-map"></a>

**`map <map>`**

```haproxy
map <map>
```

Configure the map which will be used to store token (key) and thumbprint (value), which is useful to
reply to a challenge when there are multiple account used. The acme task will add entries before
validating the challenge and will remove the entries at the end of the task.

<a id="entry-12-8-profile"></a>

**`profile <string>`**

```haproxy
profile <string>
```

Request a specific certificate profile from the CA by including a "profile" field in the newOrder
request. This implements draft-ietf-acme-profiles.

Profile names are CA-specific short identifiers (e.g. "classic", "shortlived"). When set, the
profile name is sent as-is in the newOrder JSON payload. The CA is free to ignore the request or
return an error if the profile is not supported. When not set, no profile field is included and the
CA uses its default issuance policy.

See <https://letsencrypt.org/docs/profiles/> for Let's Encrypt profiles.

Example:

```shell
# Request short-lived certificates
profile shortlived
```

<a id="entry-12-8-provider-name"></a>

**`provider-name <string>`**

```haproxy
provider-name <string>
```

Set the DNS provider name passed to the external DNS provisioning tool (e.g. the dataplaneAPI) via
the "dpapi" sink. The accepted values are tool-specific; refer to your DNS provisioning tool's
documentation.

This keyword is only meaningful when the challenge type is "dns-01" or "dns-persist-01".

See also: "challenge", "acme-vars"

<a id="entry-12-8-reuse-key"></a>

**`reuse-key { on | off }`**

```haproxy
reuse-key { on | off }
```

If set to "on", HAProxy won't generate a new private key and will keep the previous one. Rotating
private keys is recommended, when enabling this option it is recommended to regenerate manually the
keys regularly.

This option might be useful when using RSA keys bigger than 2048 that can take time to generate and
might slow down one thread doing so.

Using the same key can be useful when using the cache of your ACME server, it can help to retrieve a
valid certificate corresponding to the current key.

The default setting is "off".

Example:

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

Configure the path to the EAB key id file. The credential is provided by the CA and must be placed
at the specified path before starting HAProxy. It is used during account creation only.

The file must contain a plain ASCII string.

EAB credentials are only required during the initial ACME account creation and can be removed
afterwards, either from the config or by emptying the files. An empty file is silently ignored.
Whitespace is not ignored, except for the trailing newline.

See also: "eab-mac-key", "eab-mac-alg"

<a id="entry-12-8-eab-mac-key"></a>

**`eab-mac-key <filename>`**

```haproxy
eab-mac-key <filename>
```

Configure the path to the EAB MAC key file. The credential is provided by the CA and must be placed
at the specified path before starting HAProxy. It is used during account creation only.

The file must contain a base64url encoded MAC key.

EAB credentials are only required during the initial ACME account creation and can be removed
afterwards, either from the config or by emptying the files. An empty file is silently ignored.
Whitespace is not ignored, except for the trailing newline.

See also: "eab-key-id", "eab-mac-alg"

<a id="entry-12-8-eab-mac-alg"></a>

**`eab-mac-alg { HS256 | HS384 | HS512 }`**

```haproxy
eab-mac-alg { HS256 | HS384 | HS512 }
```

Configure MAC algorithm used for EAB signing. Default is HS256. EAB MAC key must be large enough to
support specified MAC algorithm. Not all CAs support algorithms other than HS256.

See also: "eab-key-id", "eab-mac-key"

## 12.9. Healthchecks {#section-12-9}

It is possible to globally declare several health-checks that could be used by servers across all
the configuration, overriding the local proxy configuration.

<a id="entry-12-9-healthcheck"></a>

**`healthcheck <name>`**

```haproxy
healthcheck <name>
```

Created a new healthcheck with name `<name>`. This name must be unique. It should be used on server
line to reference a specific health-check section.

<a id="entry-12-9-type"></a>

**`type <type>`**

```haproxy
type <type>
```

Defines the health-check type. This parameter is mandatory. Following types of health-check are
supported:

    * tcp-check
    * httpchk
    * ssl-hello-chk
    * smtpchk
    * pgsql-check
    * redis-check
    * mysql-check
    * ldap-check
    * spop-check

Each type uses the same parameters, if any, than the corresponding proxy's option. For instance, the
method, the uri... may be speficied for the "httpchk" type:

Examples:

```text
   healthcheck my-http-check
type httpchk GET /health HTTP/1.1 %[srv_name]
```

See also: "option tcp-check", "option httpchk", "option ssl-hello-chk", "option smtpchk", "option
mysql-check", "option pgsql-check", "option redis-check", "option ldap-check and "option spop-check"

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

Add a specific http-check rule for a "httpchk" healthcheck. The same syntax than the corresponding
proxy's directives is used. See the corresponding proxy documentation for details.

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

Add a specific tcp-check rule for a "tcp-check" healthcheck. The same syntax than the corresponding
proxy's directives is used. See the corresponding proxy documentation for details.
