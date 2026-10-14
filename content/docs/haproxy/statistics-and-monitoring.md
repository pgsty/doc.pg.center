---
title: "9. Statistics and Monitoring"
linkTitle: "9. Stats & Monitoring"
weight: 330
description: "CSV and typed stats, runtime CLI commands, master CLI, and stats files"
icon: fa-solid fa-chart-line
module: [HAPROXY]
categories: [Task]
aliases:
  - /haproxy/management/statistics-and-monitoring/
  - /docs/haproxy/management/statistics-and-monitoring/
  - /haproxy/statistics-and-monitoring/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 9"
---

It is possible to query HAProxy about its status. The most commonly used mechanism is the HTTP
statistics page. This page also exposes an alternative CSV output format for monitoring tools. The
same format is provided on the Unix socket.

Statistics are regroup in categories labelled as domains, corresponding to the multiple components
of HAProxy. There are two domains available: proxy and resolvers. If not specified, the proxy domain
is selected. Note that only the proxy statistics are printed on the HTTP page.

## 9.1. CSV format {#section-9-1}

The statistics may be consulted either from the unix socket or from the HTTP page. Both means
provide a CSV format whose fields follow. The first line begins with a sharp ('#') and has one word
per comma-delimited field which represents the title of the column. All other lines starting at the
second one use a classical CSV format using a comma as the delimiter, and the double quote ('"') as
an optional text delimiter, but only if the enclosed text is ambiguous (if it contains a quote or a
comma). The double-quote character ('"') in the text is doubled ('""'), which is the format that
most tools recognize. Please do not insert any column before these ones in order not to break tools
which use hard-coded column positions.

For proxy statistics, after each field name, the types which may have a value for that field are
specified in brackets. The types are L (Listeners), F (Frontends), B (Backends), and S (Servers).
There is a fixed set of static fields that are always available in the same order. A column
containing the character '-' delimits the end of the static fields, after which presence or order of
the fields are not guaranteed.

Here is the list of static fields using the proxy statistics domain:

```text
 0. pxname [LFBS]: proxy name
 1. svname [LFBS]: service name (FRONTEND for frontend, BACKEND for backend,
    any name for server/listener)
 2. qcur [..BS]: current queued requests. For the backend this reports the
    number queued without a server assigned.
 3. qmax [..BS]: max value of qcur
 4. scur [LFBS]: current sessions
 5. smax [LFBS]: max sessions
 6. slim [LFBS]: configured session limit
 7. stot [LFBS]: cumulative number of sessions
 8. bin [LFBS]: bytes in
 9. bout [LFBS]: bytes out
10. dreq [LFB.]: requests denied because of security concerns.
    - For tcp this is because of a matched tcp-request content rule.
    - For http this is because of a matched http-request or tarpit rule.
11. dresp [LFBS]: responses denied because of security concerns.
    - For http this is because of a matched http-request rule, or
      "option checkcache".
12. ereq [LF..]: request errors. Some of the possible causes are:
    - early termination from the client, before the request has been sent.
    - read error from the client
    - client timeout
    - client closed connection
    - various bad requests from the client.
    - request was tarpitted.
13. econ [..BS]: number of requests that encountered an error trying to
    connect to a backend server. The backend stat is the sum of the stat
    for all servers of that backend, plus any connection errors not
    associated with a particular server (such as the backend having no
    active servers).
14. eresp [..BS]: response errors. srv_abrt will be counted here also.
    Some other errors are:
    - write error on the client socket (won't be counted for the server stat)
    - failure applying filters to the response.
15. wretr [..BS]: number of times a connection to a server was retried.
16. wredis [..BS]: number of times a request was redispatched to another
    server. The server value counts the number of times that server was
    switched away from.
17. status [LFBS]: status (UP/DOWN/NOLB/MAINT/MAINT(via)/MAINT(resolution)...)
18. weight [..BS]: total effective weight (backend), effective weight (server)
19. act [..BS]: number of active servers (backend), server is active (server)
20. bck [..BS]: number of backup servers (backend), server is backup (server)
21. chkfail [...S]: number of failed checks. (Only counts checks failed when
    the server is up.)
22. chkdown [..BS]: number of UP->DOWN transitions. The backend counter counts
    transitions to the whole backend being down, rather than the sum of the
    counters for each server.
23. lastchg [..BS]: number of seconds since the last UP<->DOWN transition
24. downtime [..BS]: total downtime (in seconds). The value for the backend
    is the downtime for the whole backend, not the sum of the server downtime.
25. qlimit [...S]: configured maxqueue for the server, or nothing in the
    value is 0 (default, meaning no limit)
26. pid [LFBS]: process id (0 for first instance, 1 for second, ...)
27. iid [LFBS]: unique proxy id
28. sid [L..S]: server id (unique inside a proxy)
29. throttle [...S]: current throttle percentage for the server, when
    slowstart is active, or no value if not in slowstart.
30. lbtot [..BS]: total number of times a server was selected, either for new
    sessions, or when re-dispatching. The server counter is the number
    of times that server was selected.
31. tracked [...S]: id of proxy/server if tracking is enabled.
32. type [LFBS]: (0=frontend, 1=backend, 2=server, 3=socket/listener)
33. rate [.FBS]: number of sessions per second over last elapsed second
34. rate_lim [.F..]: configured limit on new sessions per second
35. rate_max [.FBS]: max number of new sessions per second
36. check_status [...S]: status of last health check, one of:
       UNK     -> unknown
       INI     -> initializing
       SOCKERR -> socket error
       L4OK    -> check passed on layer 4, no upper layers testing enabled
       L4TOUT  -> layer 1-4 timeout
       L4CON   -> layer 1-4 connection problem, for example
                  "Connection refused" (tcp rst) or "No route to host" (icmp)
       L6OK    -> check passed on layer 6
       L6TOUT  -> layer 6 (SSL) timeout
       L6RSP   -> layer 6 invalid response - protocol error
       L7OK    -> check passed on layer 7
       L7OKC   -> check conditionally passed on layer 7, for example 404 with
                  disable-on-404
       L7TOUT  -> layer 7 (HTTP/SMTP) timeout
       L7RSP   -> layer 7 invalid response - protocol error
       L7STS   -> layer 7 response error, for example HTTP 5xx
    Notice: If a check is currently running, the last known status will be
    reported, prefixed with "* ". e. g. "* L7OK".
37. check_code [...S]: layer5-7 code, if available
38. check_duration [...S]: time in ms took to finish last health check
39. hrsp_1xx [.FBS]: http responses with 1xx code
40. hrsp_2xx [.FBS]: http responses with 2xx code
41. hrsp_3xx [.FBS]: http responses with 3xx code
42. hrsp_4xx [.FBS]: http responses with 4xx code
43. hrsp_5xx [.FBS]: http responses with 5xx code
44. hrsp_other [.FBS]: http responses with other codes (protocol error)
45. hanafail [...S]: failed health checks details
46. req_rate [.F..]: HTTP requests per second over last elapsed second
47. req_rate_max [.F..]: max number of HTTP requests per second observed
48. req_tot [.FB.]: total number of HTTP requests received
49. cli_abrt [..BS]: number of data transfers aborted by the client
50. srv_abrt [..BS]: number of data transfers aborted by the server
    (inc. in eresp)
51. comp_in [.FB.]: number of HTTP response bytes fed to the compressor
52. comp_out [.FB.]: number of HTTP response bytes emitted by the compressor
53. comp_byp [.FB.]: number of bytes that bypassed the HTTP compressor
    (CPU/BW limit)
54. comp_rsp [.FB.]: number of HTTP responses that were compressed
55. lastsess [..BS]: number of seconds since last session assigned to
    server/backend
56. last_chk [...S]: last health check contents or textual error
57. last_agt [...S]: last agent check contents or textual error
58. qtime [..BS]: the average queue time in ms over the 1024 last requests
59. ctime [..BS]: the average connect time in ms over the 1024 last requests
60. rtime [..BS]: the average response time in ms over the 1024 last requests
    (0 for TCP)
61. ttime [..BS]: the average total session time in ms over the 1024 last
    requests
62. agent_status [...S]: status of last agent check, one of:
       UNK     -> unknown
       INI     -> initializing
       SOCKERR -> socket error
       L4OK    -> check passed on layer 4, no upper layers testing enabled
       L4TOUT  -> layer 1-4 timeout
       L4CON   -> layer 1-4 connection problem, for example
                  "Connection refused" (tcp rst) or "No route to host" (icmp)
       L7OK    -> agent reported "up"
       L7STS   -> agent reported "fail", "stop", or "down"
63. agent_code [...S]: numeric code reported by agent if any (unused for now)
64. agent_duration [...S]: time in ms taken to finish last check
65. check_desc [...S]: short human-readable description of check_status
66. agent_desc [...S]: short human-readable description of agent_status
67. check_rise [...S]: server's "rise" parameter used by checks
68. check_fall [...S]: server's "fall" parameter used by checks
69. check_health [...S]: server's health check value between 0 and rise+fall-1
70. agent_rise [...S]: agent's "rise" parameter, normally 1
71. agent_fall [...S]: agent's "fall" parameter, normally 1
72. agent_health [...S]: agent's health parameter, between 0 and rise+fall-1
73. addr [L..S]: address:port or "unix". IPv6 has brackets around the address.
74: cookie [..BS]: server's cookie value or backend's cookie name
75: mode [LFBS]: proxy mode (tcp, http, health, unknown)
76: algo [..B.]: load balancing algorithm
77: conn_rate [.F..]: number of connections over the last elapsed second
78: conn_rate_max [.F..]: highest known conn_rate
79: conn_tot [.F..]: cumulative number of connections
80: intercepted [.FB.]: cum. number of intercepted requests (monitor, stats)
81: dcon [LF..]: requests denied by "tcp-request connection" rules
82: dses [LF..]: requests denied by "tcp-request session" rules
83: wrew [LFBS]: cumulative number of failed header rewriting warnings
84: connect [..BS]: cumulative number of connection establishment attempts
85: reuse [..BS]: cumulative number of connection reuses
86: cache_lookups [.FB.]: cumulative number of cache lookups
87: cache_hits [.FB.]: cumulative number of cache hits
88: srv_icur [...S]: current number of idle connections available for reuse
89: src_ilim [...S]: limit on the number of available idle connections
90. qtime_max [..BS]: the maximum observed queue time in ms
91. ctime_max [..BS]: the maximum observed connect time in ms
92. rtime_max [..BS]: the maximum observed response time in ms (0 for TCP)
93. ttime_max [..BS]: the maximum observed total session time in ms
94. eint [LFBS]: cumulative number of internal errors
95. idle_conn_cur [...S]: current number of unsafe idle connections
96. safe_conn_cur [...S]: current number of safe idle connections
97. used_conn_cur [...S]: current number of connections in use
98. need_conn_est [...S]: estimated needed number of connections
99. uweight [..BS]: total user weight (backend), server user weight (server)
100. agg_server_status [..B.]: backend aggregated gauge of server's status
101. agg_server_status_check [..B.]: (deprecated)
102. agg_check_status [..B.]: backend aggregated gauge of server's state check
     status
103. srid [...S]: server id revision
104. sess_other [.F..]: total number of sessions other than HTTP since process
     started
105. h1_sess [.F..]: total number of HTTP/1 sessions since process started
106. h2_sess [.F..]: total number of HTTP/2 sessions since process started
107. h3_sess [.F..]: total number of HTTP/3 sessions since process started
108. req_other [.F..]: total number of sessions other than HTTP processed by
     this object since the worker process started
109. h1req [.F..]: total number of HTTP/1 sessions processed by this object
     since the worker process started
110. h2req [.F..]: total number of hTTP/2 sessions processed by this object
     since the worker process started
111. h3req [.F..]: total number of HTTP/3 sessions processed by this object
     since the worker process started
112. proto [L...]: protocol
113. priv_idle_cur [...S]: current number of private idle connections
114. reqbin [LFBS]: total number of request bytes received since the worker
     process started
115. reqbout [LFBS]: total number of request bytes sent since the worker
     process started
116. resbin [LFBS]: total number of response bytes received since the worker
     process started
117. resbout [LFBS]: total number of response bytes sent since the worker
     process started
```

For all other statistics domains, the presence or the order of the fields are not guaranteed. In
this case, the header line should always be used to parse the CSV data.

## 9.2. Typed output format {#section-9-2}

Both "show info" and "show stat" support a mode where each output value comes with its type and
sufficient information to know how the value is supposed to be aggregated between processes and how
it evolves.

In all cases, the output consists in having a single value per line with all the information split
into fields delimited by colons (':').

The first column designates the object or metric being dumped. Its format is specific to the command
producing this output and will not be described in this section. Usually it will consist in a series
of identifiers and field names.

The second column contains 4 characters respectively indicating the origin, the nature, the scope
and the persistence state of the value being reported. The first character (the origin) indicates
where the value was extracted from. Possible characters are:

```text
M   The value is a metric. It is valid at one instant any may change depending
    on its nature .

S   The value is a status. It represents a discrete value which by definition
    cannot be aggregated. It may be the status of a server ("UP" or "DOWN"),
    the PID of the process, etc.

K   The value is a sorting key. It represents an identifier which may be used
    to group some values together because it is unique among its class. All
    internal identifiers are keys. Some names can be listed as keys if they
    are unique (eg: a frontend name is unique). In general keys come from the
    configuration, even though some of them may automatically be assigned. For
    most purposes keys may be considered as equivalent to configuration.

C   The value comes from the configuration. Certain configuration values make
    sense on the output, for example a concurrent connection limit or a cookie
    name. By definition these values are the same in all processes started
    from the same configuration file.

P   The value comes from the product itself. There are very few such values,
    most common use is to report the product name, version and release date.
    These elements are also the same between all processes.
```

The second character (the nature) indicates the nature of the information carried by the field in
order to let an aggregator decide on what operation to use to aggregate multiple values. Possible
characters are:

```text
A   The value represents an age since a last event. This is a bit different
    from the duration in that an age is automatically computed based on the
    current date. A typical example is how long ago did the last session
    happen on a server. Ages are generally aggregated by taking the minimum
    value and do not need to be stored.

a   The value represents an already averaged value. The average response times
    and server weights are of this nature. Averages can typically be averaged
    between processes.

C   The value represents a cumulative counter. Such measures perpetually
    increase until they wrap around. Some monitoring protocols need to tell
    the difference between a counter and a gauge to report a different type.
    In general counters may simply be summed since they represent events or
    volumes. Examples of metrics of this nature are connection counts or byte
    counts.

D   The value represents a duration for a status. There are a few usages of
    this, most of them include the time taken by the last health check and
    the time a server has spent down. Durations are generally not summed,
    most of the time the maximum will be retained to compute an SLA.

G   The value represents a gauge. It's a measure at one instant. The memory
    usage or the current number of active connections are of this nature.
    Metrics of this type are typically summed during aggregation.

L   The value represents a limit (generally a configured one). By nature,
    limits are harder to aggregate since they are specific to the point where
    they were retrieved. In certain situations they may be summed or be kept
    separate.

M   The value represents a maximum. In general it will apply to a gauge and
    keep the highest known value. An example of such a metric could be the
    maximum amount of concurrent connections that was encountered in the
    product's life time. To correctly aggregate maxima, you are supposed to
    output a range going from the maximum of all maxima and the sum of all
    of them. There is indeed no way to know if they were encountered
    simultaneously or not.

m   The value represents a minimum. In general it will apply to a gauge and
    keep the lowest known value. An example of such a metric could be the
    minimum amount of free memory pools that was encountered in the product's
    life time. To correctly aggregate minima, you are supposed to output a
    range going from the minimum of all minima and the sum of all of them.
    There is indeed no way to know if they were encountered simultaneously
    or not.

N   The value represents a name, so it is a string. It is used to report
    proxy names, server names and cookie names. Names have configuration or
    keys as their origin and are supposed to be the same among all processes.

O   The value represents a free text output. Outputs from various commands,
    returns from health checks, node descriptions are of such nature.

R   The value represents an event rate. It's a measure at one instant. It is
    quite similar to a gauge except that the recipient knows that this measure
    moves slowly and may decide not to keep all values. An example of such a
    metric is the measured amount of connections per second. Metrics of this
    type are typically summed during aggregation.

T   The value represents a date or time. A field emitting the current date
    would be of this type. The method to aggregate such information is left
    as an implementation choice. For now no field uses this type.
```

The third character (the scope) indicates what extent the value reflects. Some elements may be per
process while others may be per configuration or per system. The distinction is important to know
whether or not a single value should be kept during aggregation or if values have to be aggregated.
The following characters are currently supported:

```text
C   The value is valid for a whole cluster of nodes, which is the set of nodes
    communicating over the peers protocol. An example could be the amount of
    entries present in a stick table that is replicated with other peers. At
    the moment no metric use this scope.

P   The value is valid only for the process reporting it. Most metrics use
    this scope.

S   The value is valid for the whole service, which is the set of processes
    started together from the same configuration file. All metrics originating
    from the configuration use this scope. Some other metrics may use it as
    well for some shared resources (eg: shared SSL cache statistics).

s   The value is valid for the whole system, such as the system's hostname,
    current date or resource usage. At the moment this scope is not used by
    any metric.
```

The fourth character (persistence state) indicates that the value (the metric) is volatile or
persistent across reloads. The following characters are expected:

```text
V   The metric is volatile because it is local to the current process so
    the value will be lost when reloading.

P   The metric is persistent because it may be shared with other co-processes
    so that the value is preserved across reloads.
```

Consumers of these information will generally have enough of these 4 characters to determine how to
accurately report aggregated information across multiple processes.

After this column, the third column indicates the type of the field, among "s32" (signed 32-bit
integer), "s64" (signed 64-bit integer), "u32" (unsigned 32-bit integer), "u64" (unsigned 64-bit
integer), "str" (string). It is important to know the type before parsing the value in order to
properly read it. For example a string containing only digits is still a string an not an integer
(eg: an error code extracted by a check).

Then the fourth column is the value itself, encoded according to its type. Strings are dumped as-is
immediately after the colon without any leading space. If a string contains a colon, it will appear
normally. This means that the output should not be exclusively split around colons or some check
outputs or server addresses might be truncated.

## 9.3. Unix Socket commands {#section-9-3}

The stats socket is not enabled by default. In order to enable it, it is necessary to add one line
in the global section of the haproxy configuration. A second line is recommended to set a larger
timeout, always appreciated when issuing commands by hand:

```text
global
    stats socket /var/run/haproxy.sock mode 600 level admin
    stats timeout 2m
```

It is also possible to add multiple instances of the stats socket by repeating the line, and make
them listen to a TCP port instead of a UNIX socket. This is never done by default because this is
dangerous, but can be handy in some situations:

```text
global
    stats socket /var/run/haproxy.sock mode 600 level admin
    stats socket ipv4@192.168.0.1:9999 level admin
    stats timeout 2m
```

To access the socket, an external utility such as "socat" is required. Socat is a swiss-army knife
to connect anything to anything. We use it to connect terminals to the socket, or a couple of
stdin/stdout pipes to it for scripts. The two main syntaxes we'll use are the following:

```shell
# socat /var/run/haproxy.sock stdio
# socat /var/run/haproxy.sock readline
```

The first one is used with scripts. It is possible to send the output of a script to haproxy, and
pass haproxy's output to another script. That's useful for retrieving counters or attack traces for
example.

The second one is only useful for issuing commands by hand. It has the benefit that the terminal is
handled by the readline library which supports line editing and history, which is very convenient
when issuing repeated commands (eg: watch a counter).

The socket supports three operation modes:

- non-interactive, silent
- interactive, silent
- interactive with prompt

The non-interactive mode is the default when socat connects to the socket. In this mode, a single
line may be sent. It is processed as a whole, responses are sent back, and the connection closes
after the end of the response. This is the mode that scripts and monitoring tools use. It is
possible to send multiple commands in this mode, they need to be delimited by a semi-colon (';').
For example:

```shell
# echo "show info;show stat;show table" | socat /var/run/haproxy stdio
```

If a command needs to use a semi-colon or a backslash (eg: in a value), it must be preceded by a
backslash ('&#92;').

The interactive mode allows new commands to be sent after the ones from the previous lines finish.
It exists in two variants, one silent, which works like the non-interactive mode except that the
socket waits for a new command instead of closing, and one where a prompt is displayed ('\>') at the
beginning of the line. The interactive mode is preferred for advanced tools while the prompt mode is
preferred for humans.

The mode can be changed using the "prompt" command. By default, it toggles the interactive+prompt
modes. Entering "prompt" in interactive mode will switch to prompt mode. The command optionally
takes a specific mode among which:

- "n": non-interactive mode (single command and quits)
- "i": interactive mode (multiple commands, no prompt)
- "p": prompt mode (multiple commands with a prompt)

Since the default mode is non-interactive, "prompt" must be used as the first command in order to
switch it, otherwise the previous command will cause the connection to be closed. Switching to
non-interactive mode will result in the connection to be closed after all the commands of the same
line complete.

For this reason, when debugging by hand, it's quite common to start with the "prompt" command:

```haproxy
# socat /var/run/haproxy readline
prompt
```

> show info ...

Interactive tools might prefer starting with "prompt i" to switch to interactive mode without the
prompt.

Optionally the process' uptime may be displayed in the prompt. In order to enable this, the "prompt
timed" command will enable the prompt and toggle the displaying of the time. The uptime is displayed
in format "d:hh:mm:ss" where "d" is the number of days, and "hh", "mm", "ss" are respectively the
number of hours, minutes and seconds on two digits each:

```haproxy
# socat /var/run/haproxy readline
prompt timed
```

[23:03:34:39]\> show version 2.8-dev9-e5e622-18

[23:03:34:41]\> quit

When the timed prompt is set on the master CLI, the prompt will display the currently selected
process' uptime, so this will work for the master, current worker or an older worker:

```shell
master> prompt timed
[0:00:00:50] master> show proc
(...)
[0:00:00:58] master> @!11955     <-- master, switch to current worker
[0:00:01:03] 11955> @!11942      <-- current worker, switch to older worker
[0:00:02:17] 11942> @            <-- older worker, switch back to master
[0:00:01:10] master>
```

Since multiple commands may be issued at once, haproxy uses the empty line as a delimiter to mark an
end of output for each command, and takes care of ensuring that no command can emit an empty line on
output. A script can thus easily parse the output even when multiple commands were pipelined on a
single line.

Some commands may take an optional payload. To add one to a command, the first line needs to end
with the "\<\<&#92;n" pattern. The next lines will be treated as the payload
and can contain as many lines as needed. To validate a command with a payload, it needs to end with
an empty line.

The payload pattern can be customized in order to change the way the payload ends. In order to end a
payload with something else than an empty line, a customized pattern can be set between '\<\<' and
'&#92;n'. Up to 64 characters can be used in addition to '\<\<', otherwise
this won't be considered a payload. It should be enough to use random payload patterns. For example,
to use a PEM file that contains empty lines and comments:

```haproxy
# echo -e "set ssl cert common.pem <<%EOF%\n$(cat common.pem)\n%EOF%\n" | \
socat /var/run/haproxy.stat -
```

Limitations do exist: The pattern "\<\<" must not be glued to the last word of the line. The length
of a command line must not be greater than tune.bufsize, including the pattern starting the payload,
but excluding the payload itself. The payload size is limited to 128KB by default. This can be
changed by setting "tune.cli.max-payload-size" global parameter, with some cautions. Note the
pattern marking the end of the payload is part of this limit.

When entering a payload while in interactive mode, the prompt will change from "\> " to "+ ".

It is important to understand that when multiple haproxy processes are started on the same sockets,
any process may pick up the request and will output its own stats.

The list of commands currently supported on the stats socket is provided below. If an unknown
command is sent, haproxy displays the usage message which reminds all supported commands. Some
commands support a more complex syntax, generally it will explain what part of the command is
invalid when this happens.

Some commands require a higher level of privilege to work. If you do not have enough privilege, you
will get an error "Permission denied". Please check the "level" option of the "bind" keyword lines
in the configuration manual for more information.

<a id="entry-9-3-abort-ssl-ca-file"></a>

**`abort ssl ca-file <cafile>`**

```haproxy
abort ssl ca-file <cafile>
```

Abort and destroy a temporary CA file update transaction.

See also "set ssl ca-file" and "commit ssl ca-file".

<a id="entry-9-3-abort-ssl-cert"></a>

**`abort ssl cert <filename>`**

```haproxy
abort ssl cert <filename>
```

Abort and destroy a temporary SSL certificate update transaction.

See also "set ssl cert" and "commit ssl cert".

<a id="entry-9-3-abort-ssl-crl-file"></a>

**`abort ssl crl-file <crlfile>`**

```haproxy
abort ssl crl-file <crlfile>
```

Abort and destroy a temporary CRL file update transaction.

See also "set ssl crl-file" and "commit ssl crl-file".

<a id="entry-9-3-acme-renew"></a>

**`acme renew <certificate>`**

```haproxy
acme renew <certificate>
```

Starts an ACME certificate generation task with the given certificate name. The certificate must be
linked to an acme section, see [section 12.8](/docs/haproxy/other-sections/#section-12-8) "ACME" of the configuration manual. See also "acme
status".

<a id="entry-9-3-acme-status"></a>

**`acme status`**

```haproxy
acme status
```

Show the status of every certificates that were configured with ACME.

This command outputs, separated by a tab:

- The name of the certificate configured in haproxy
- The acme section used in the configuration
- The state of the acme task, either "Running", "Scheduled" or "Stopped"
- The UTC expiration date of the certificate in ISO8601 format
- The relative expiration time (0d if expired)
- The UTC scheduled date of the certificate in ISO8601 format
- The relative schedule time (0d if Running)

Example:

```shell
$ echo "@1; acme status" | socat /tmp/master.sock - | column -t -s $'\t'
# certificate   section  state      expiration date (UTC)  expires in        scheduled date (UTC)  scheduled in
ecdsa.pem       LE       Running    2020-01-18T09:31:12Z   0d 0h00m00s       2020-01-15T21:31:12Z  0d 0h00m00s
foobar.pem.rsa  LE       Scheduled  2025-08-04T11:50:54Z   89d 23h01m13s     2025-07-27T23:50:55Z  82d 11h01m14s
```

<a id="entry-9-3-add-acl"></a>

**`add acl [@<ver>] <acl> <pattern>`**

```haproxy
add acl [@<ver>] <acl> <pattern>
```

Add an entry into the acl `<acl>`. `<acl>` is the \#`<id>` or the `<name>` returned by "show acl".
This command does not verify if the entry already exists. Entries are added to the current version
of the ACL, unless a specific version is specified with "@`<ver>`". This version number must have
preliminary been allocated by "prepare acl", and it will be comprised between the versions reported
in "curr_ver" and "next_ver" on the output of "show acl". Entries added with a specific version
number will not match until a "commit acl" operation is performed on them. They may however be
consulted using the "show acl @`<ver>`" command, and cleared using a "clear acl @`<ver>`" command.
This command cannot be used if the reference `<acl>` is a name also used with a map. In this case,
the "add map" command must be used instead.

<a id="entry-9-3-add-backend"></a>

**`add backend <name> from <defproxy> [mode <mode>] [guid <guid>]`**

```haproxy
add backend <name> from <defproxy> [mode <mode>] [guid <guid>]
```

Instantiate a new backend proxy with the name `<name>`.

Only TCP or HTTP proxies can be created. All of the settings are inherited from `<defproxy>` default
proxy instance. By default, it is mandatory to specify the backend mode via the argument of the same
name, unless `<defproxy>` already defines it explicitly. It is also possible to use an optional GUID
argument if wanted.

Servers can be added via the command "add server". The backend is initialized in the unpublished
state. Once considered ready for traffic, use "publish backend" to expose the newly created
instance.

All named default proxies can be used, given that they validate the same inheritance rules applied
during configuration parsing. There is some exceptions though, for example when the mode is neither
TCP nor HTTP.

This command is restricted and can only be issued on sockets configured for level "admin".

<a id="entry-9-3-add-map"></a>

**`add map [@<ver>] <map> <key> <value>`**

```haproxy
add map [@<ver>] <map> <key> <value>
add map [@<ver>] <map> <payload>
```

Add an entry into the map `<map>` to associate the value `<value>` to the key `<key>`. This command
does not verify if the entry already exists. It is mainly used to fill a map after a "clear" or
"prepare" operation. Entries are added to the current version of the ACL, unless a specific version
is specified with "@`<ver>`". This version number must have preliminary been allocated by "prepare
acl", and it will be comprised between the versions reported in "curr_ver" and "next_ver" on the
output of "show acl". Entries added with a specific version number will not match until a "commit
map" operation is performed on them. They may however be consulted using the "show map @`<ver>`"
command, and cleared using a "clear acl @`<ver>`" command. If the designated map is also used as an
ACL, the ACL will only match the `<key>` part and will ignore the `<value>` part. Using the payload
syntax it is possible to add multiple key/value pairs by entering them on separate lines. On each
new line, the first word is the key and the rest of the line is considered to be the value which can
even contains spaces.

Example:

```shell
# socat /tmp/sock1 -
prompt

> add map #-1 <<
+ key1 value1
+ key2 value2 with spaces
+ key3 value3 also with spaces
+ key4 value4

>
```

<a id="entry-9-3-add-server"></a>

**`add server <backend>/<server> [args]*`**

```haproxy
add server <backend>/<server> [args]*
```

Instantiate a new server attached to the backend `<backend>`.

The `<server>` name must not be already used in the backend. A special restriction is put on the
backend which must used a dynamic load-balancing algorithm. A subset of keywords from the server
config file statement can be used to configure the server behavior (see "add server help" to list
them). Also note that no settings will be reused from an hypothetical 'default-server' statement in
the same backend.

Currently a dynamic server is statically initialized with the "none" init-addr method. This means
that no resolution will be undertaken if a FQDN is specified as an address, even if the server
creation will be validated.

To support the reload operations, it is expected that the server created via the CLI is also
manually inserted in the relevant haproxy configuration file. A dynamic server not present in the
configuration won't be restored after a reload operation.

A dynamic server may use the "track" keyword to follow the check status of another server from the
configuration. However, it is not possible to track another dynamic server. This is to ensure that
the tracking chain is kept consistent even in the case of dynamic servers deletion.

Use the "check" keyword to enable health-check support. Note that the health-check is disabled by
default and must be enabled independently from the server using the "enable health" command. For
agent checks, use the "agent-check" keyword and the "enable agent" command. Note that in this case
the server may be activated via the agent depending on the status reported, without an explicit
"enable server" command. This also means that extra care is required when removing a dynamic server
with agent check. The agent should be first deactivated via "disable agent" to be able to put the
server in the required maintenance mode before removal.

It may be possible to reach the fd limit when using a large number of dynamic servers. Please refer
to the "u-limit" global keyword documentation in this case.

<a id="entry-9-3-add-server-help"></a>

**`add server help`**

```haproxy
add server help
```

List the keywords supported for dynamic servers by the current haproxy version. Keyword syntax is
similar to the server line from the configuration file, please refer to their individual
documentation for details.

<a id="entry-9-3-add-ssl-ca-file"></a>

**`add ssl ca-file <cafile> <payload>`**

```haproxy
add ssl ca-file <cafile> <payload>
```

Add a new certificate to a ca-file. This command is useful when you reached the buffer size limit on
the CLI and want to add multiple certificates. Instead of doing a "set" with all the certificates
you are able to add each certificate individually. A "set ssl ca-file" will reset the ca-file.

Example:

```text
echo -e "set ssl ca-file cafile.pem <<\n$(cat rootCA.crt)\n" | \
socat /var/run/haproxy.stat -
echo -e "add ssl ca-file cafile.pem <<\n$(cat intermediate1.crt)\n" | \
socat /var/run/haproxy.stat -
echo -e "add ssl ca-file cafile.pem <<\n$(cat intermediate2.crt)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl ca-file cafile.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-add-ssl-crt-list"></a>

**`add ssl crt-list <crtlist> <certificate>`**

```haproxy
add ssl crt-list <crtlist> <certificate>
add ssl crt-list <crtlist> <payload>
```

Add an certificate in a crt-list. It can also be used for directories since directories are now
loaded the same way as the crt-lists. This command allow you to use a certificate name in parameter,
to use SSL options or filters a crt-list line must sent as a payload instead. Only one crt-list line
is supported in the payload. This command will load the certificate for every bind lines using the
crt-list. To push a new certificate to HAProxy the commands "new ssl cert" and "set ssl cert" must
be used.

Example:

```shell
$ echo "new ssl cert foobar.pem" | socat /tmp/sock1 -
$ echo -e "set ssl cert foobar.pem <<\n$(cat foobar.pem)\n" | socat
/tmp/sock1 -
$ echo "commit ssl cert foobar.pem" | socat /tmp/sock1 -
$ echo "add ssl crt-list certlist1 foobar.pem" | socat /tmp/sock1 -

$ echo -e 'add ssl crt-list certlist1 <<\nfoobar.pem [allow-0rtt] foo.bar.com
!test1.com\n' | socat /tmp/sock1 -
```

<a id="entry-9-3-add-ssl-ech"></a>

**`add ssl ech <bind> <payload>`**

```haproxy
add ssl ech <bind> <payload>
```

Add an ECH key to a `<bind>` line. The payload must be in the PEM for ECH format.
(<https://datatracker.ietf.org/doc/html/draft-farrell-tls-pemesni>)

The bind line format is `<frontend>`/@`<filename>`:`<linenum>` (Example: frontend1/@haproxy.conf:19)
or `<frontend>`/`<name>` if the bind line was named with the "name" keyword.

Necessitates an OpenSSL version that supports ECH, and HAProxy must be compiled with USE_ECH=1. This
command is only supported on a CLI connection running in experimental mode (see "experimental-mode
on").

See also "show ssl ech" and "ech" in the [Section 5.1](/docs/haproxy/bind-and-server-options/#section-5-1) of the configuration manual.

Example:

```shell
$ openssl ech -public_name foobar.com -out foobar3.com.ech
$ echo -e "experimental-mode on; add ssl ech frontend1/@haproxy.conf:19 <<%EOF%\n$(cat foobar3.com.ech)\n%EOF%\n" | \
  socat /tmp/haproxy.sock -
added a new ECH config to frontend1
```

<a id="entry-9-3-add-ssl-jwt"></a>

**`add ssl jwt <filename>`**

```haproxy
add ssl jwt <filename>
```

Add an already loaded certificate to the list of certificates that can be used for JWT validation
(see "jwt_verify_cert" converter). This command does not work on ongoing transactions. See also "del
ssl jwt" and "show ssl jwt" commands. See "jwt" certificate option for more information.

<a id="entry-9-3-clear-counters"></a>

**`clear counters`**

```haproxy
clear counters
```

Clear the max values of the statistics counters in each proxy (frontend & backend) and in each
server. The accumulated counters are not affected. The internal activity counters reported by "show
activity" are also reset. This can be used to get clean counters after an incident, without having
to restart nor to clear traffic counters. This command is restricted and can only be issued on
sockets configured for levels "operator" or "admin".

<a id="entry-9-3-clear-counters-all"></a>

**`clear counters all`**

```haproxy
clear counters all
```

Clear all statistics counters in each proxy (frontend & backend) and in each server. This has the
same effect as restarting. This command is restricted and can only be issued on sockets configured
for level "admin".

<a id="entry-9-3-clear-acl"></a>

**`clear acl [@<ver>] <acl>`**

```haproxy
clear acl [@<ver>] <acl>
```

Remove all entries from the acl `<acl>`. `<acl>` is the \#`<id>` or the `<name>` returned by "show
acl". Note that if the reference `<acl>` is a name and is shared with a map, this map will be also
cleared. By default only the current version of the ACL is cleared (the one being matched against).
However it is possible to specify another version using '@' followed by this version.

<a id="entry-9-3-clear-map"></a>

**`clear map [@<ver>] <map>`**

```haproxy
clear map [@<ver>] <map>
```

Remove all entries from the map `<map>`. `<map>` is the \#`<id>` or the `<name>` returned by "show
map". Note that if the reference `<map>` is a name and is shared with a acl, this acl will be also
cleared. By default only the current version of the map is cleared (the one being matched against).
However it is possible to specify another version using '@' followed by this version.

<a id="entry-9-3-clear-table"></a>

**`clear table <table> [ data.<type> <operator> <value> ] | [ key <key> ] |`**

```haproxy
clear table <table> [ data.<type> <operator> <value> ] | [ key <key> ] |
                    [ ptr <ptr> ]
```

Remove entries from the stick-table `<table>`.

This is typically used to unblock some users complaining they have been abusively denied access to a
service, but this can also be used to clear some stickiness entries matching a server that is going
to be replaced (see "show table" below for details). Note that sometimes, removal of an entry will
be refused because it is currently tracked by a session. Retrying a few seconds later after the
session ends is usual enough.

In the case where no options arguments are given all entries will be removed.

When the "data." form is used entries matching a filter applied using the stored data (see
"stick-table" in section 4.2) are removed. A stored data type must be specified in `<type>`, and
this data type must be stored in the table otherwise an error is reported. The data is compared
according to `<operator>` with the 64-bit integer `<value>`. Operators are the same as with the
ACLs:

    - eq: match entries whose data is equal to this value
    - ne: match entries whose data is not equal to this value
    - le: match entries whose data is less than or equal to this value
    - ge: match entries whose data is greater than or equal to this value
    - lt: match entries whose data is less than this value
    - gt: match entries whose data is greater than this value

When the key form is used the entry `<key>` is removed. The key must be of the same type as the
table, which currently is limited to IPv4, IPv6, integer and string.

When the ptr form is used the entry `<ptr>` is removed. `<ptr>` is written in the form 0xffff and
must correspond to the address returned by a previous "show table" command. Matching an entry using
its pointer may be relevant if the entry cannot be matched using the key due to empty key or
incompatible characters on the cli.

If data.`<type>` is an array type, "[]" may be used to access a specific index in the array, like
so: data.gpt[1]

Example:

```shell
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a4c: key=127.0.0.1 use=0 exp=3594729 gpc0=0 conn_rate(30000)=1 \
      bytes_out_rate(60000)=187
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200

    $ echo "clear table http_proxy key 127.0.0.1" | socat stdio /tmp/sock1

    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:1
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200
      bytes_out_rate(60000)=191
    $ echo "clear table http_proxy data.gpc0 eq 1" | socat stdio /tmp/sock1
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:1
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200

    $ echo "clear table http_proxy ptr 0x80e6b40" | socat stdio /tmp/sock1
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:0
```

<a id="entry-9-3-commit-acl"></a>

**`commit acl @<ver> <acl>`**

```haproxy
commit acl @<ver> <acl>
```

Commit all changes made to version `<ver>` of ACL `<acl>`, and deletes all past versions. `<acl>` is
the \#`<id>` or the `<name>` returned by "show acl". The version number must be between "curr_ver"+1
and "next_ver" as reported in "show acl". The contents to be committed to the ACL can be consulted
with "show acl @`<ver>` `<acl>`" if desired. The specified version number has normally been created
with the "prepare acl" command. The replacement is atomic. It consists in atomically updating the
current version to the specified version, which will instantly cause all entries in other versions
to become invisible, and all entries in the new version to become visible. It is also possible to
use this command to perform an atomic removal of all visible entries of an ACL by calling "prepare
acl" first then committing without adding any entries. This command cannot be used if the reference
`<acl>` is a name also used as a map. In this case, the "commit map" command must be used instead.

<a id="entry-9-3-commit-map"></a>

**`commit map @<ver> <map>`**

```haproxy
commit map @<ver> <map>
```

Commit all changes made to version `<ver>` of map `<map>`, and deletes all past versions. `<map>` is
the \#`<id>` or the `<name>` returned by "show map". The version number must be between "curr_ver"+1
and "next_ver" as reported in "show map". The contents to be committed to the map can be consulted
with "show map @`<ver>` `<map>`" if desired. The specified version number has normally been created
with the "prepare map" command. The replacement is atomic. It consists in atomically updating the
current version to the specified version, which will instantly cause all entries in other versions
to become invisible, and all entries in the new version to become visible. It is also possible to
use this command to perform an atomic removal of all visible entries of an map by calling "prepare
map" first then committing without adding any entries.

<a id="entry-9-3-commit-ssl-ca-file"></a>

**`commit ssl ca-file <cafile>`**

```haproxy
commit ssl ca-file <cafile>
```

Commit a temporary SSL CA file update transaction.

In the case of an existing CA file (in a "Used" state in "show ssl ca-file"), the new CA file tree
entry is inserted in the CA file tree and every instance that used the CA file entry is rebuilt,
along with the SSL contexts it needs. All the contexts previously used by the rebuilt instances are
removed. Upon success, the previous CA file entry is removed from the tree. Upon failure, nothing is
removed or deleted, and all the original SSL contexts are kept and used. Once the temporary
transaction is committed, it is destroyed.

In the case of a new CA file (after a "new ssl ca-file" and in a "Unused" state in "show ssl
ca-file"), the CA file will be inserted in the CA file tree but it won't be used anywhere in
HAProxy. To use it and generate SSL contexts that use it, you will need to add it to a crt-list with
"add ssl crt-list".

See also "new ssl ca-file", "set ssl ca-file", "add ssl ca-file", "abort ssl ca-file" and "add ssl
crt-list".

<a id="entry-9-3-commit-ssl-cert"></a>

**`commit ssl cert <filename>`**

```haproxy
commit ssl cert <filename>
```

Commit a temporary SSL certificate update transaction.

In the case of an existing certificate (in a "Used" state in "show ssl cert"), generate every SSL
contexts and SNIs it needs, insert them, and remove the previous ones. Replace in memory the
previous SSL certificates everywhere the `<filename>` was used in the configuration. Upon failure it
doesn't remove or insert anything. Once the temporary transaction is committed, it is destroyed.

In the case of a new certificate (after a "new ssl cert" and in a "Unused" state in "show ssl
cert"), the certificate will be committed in a certificate storage, but it won't be used anywhere in
haproxy. To use it and generate its SNIs you will need to add it to a crt-list or a directory with
"add ssl crt-list".

See also "new ssl cert", "set ssl cert", "abort ssl cert" and "add ssl crt-list".

<a id="entry-9-3-commit-ssl-crl-file"></a>

**`commit ssl crl-file <crlfile>`**

```haproxy
commit ssl crl-file <crlfile>
```

Commit a temporary SSL CRL file update transaction.

In the case of an existing CRL file (in a "Used" state in "show ssl crl-file"), the new CRL file
entry is inserted in the CA file tree (which holds both the CA files and the CRL files) and every
instance that used the CRL file entry is rebuilt, along with the SSL contexts it needs. All the
contexts previously used by the rebuilt instances are removed. Upon success, the previous CRL file
entry is removed from the tree. Upon failure, nothing is removed or deleted, and all the original
SSL contexts are kept and used. Once the temporary transaction is committed, it is destroyed.

In the case of a new CRL file (after a "new ssl crl-file" and in a "Unused" state in "show ssl
crl-file"), the CRL file will be inserted in the CRL file tree but it won't be used anywhere in
HAProxy. To use it and generate SSL contexts that use it, you will need to add it to a crt-list with
"add ssl crt-list".

See also "new ssl crl-file", "set ssl crl-file", "abort ssl crl-file" and "add ssl crt-list".

<a id="entry-9-3-debug-counters"></a>

**`debug counters [reset|show|on|off|all|bug|chk|cnt|glt|?]*`**

```haproxy
debug counters [reset|show|on|off|all|bug|chk|cnt|glt|?]*
```

List internal counters placed in the code, which may vary depending on some build options. Some of
them depend on DEBUG_STRICT, others on DEBUG_COUNTERS. The command takes a combination of multiple
arguments, some defining actions and others defining filters: - bug enables listing the counters for
BUG_ON() statements - cnt enables listing the counters for COUNT_IF() statements - chk enables
listing the counters for CHECK_IF() statements - glt enables listing the counters for COUNT_GLITCH()
statements - all enables showing counters that never triggered (value 0) - off action: disables
updating of the COUNT_IF() counters - on action: enables updating of the COUNT_IF() counters - reset
action: resets all specified counters - show action: shows all specified counters

By default, the action is "show" to show counters, and the listed counters are all types with a
non-zero value. The "show" command is implicit when no other action is specified, and is only
present to ease the production of commands from scripts.

The output starts with an integer counter, followed by the type of the counter in upper case, then
its location in the code (file:line), the function name, and optionally ": " followed by a
description. Please note that the output format might change between major versions, and new types
and entries might be backported to stable versions for the purpose of improved debugging
capabilities. Any monitoring performed on them should only be done in a very lenient and permissive
way, and preferably not.

Normally, end users will not use this command, but they may be invited to do so by a developer
trying to figure the cause of an issue, looking for CNT or GLT entries. By the way, non-zero "CHK"
entries are not expected to happen and should be reported to developers as they might indicate some
incorrect assumptions in the code.

<a id="entry-9-3-debug-dev"></a>

**`debug dev <command> [args]*`**

```haproxy
debug dev <command> [args]*
```

Call a developer-specific command. Only supported on a CLI connection running in expert mode (see
"expert-mode on"). Such commands are extremely dangerous and not forgiving, any misuse may result in
a crash of the process. They are intended for experts only, and must really not be used unless told
to do so. Some of them are only available when haproxy is built with DEBUG_DEV defined because they
may have security implications. All of these commands require admin privileges, and are purposely
not documented to avoid encouraging their use by people who are not at ease with the source code.

<a id="entry-9-3-del-acl"></a>

**`del acl <acl> [<key>|#<ref>]`**

```haproxy
del acl <acl> [<key>|#<ref>]
```

Delete all the acl entries from the acl `<acl>` corresponding to the key `<key>`. `<acl>` is the
\#`<id>` or the `<name>` returned by "show acl". If the `<ref>` is used, this command delete only
the listed reference. The reference can be found with listing the content of the acl. Note that if
the reference `<acl>` is a name and is shared with a map, the entry will be also deleted in the map.

<a id="entry-9-3-del-backend"></a>

**`del backend <name>`**

```haproxy
del backend <name>
```

Removes the backend proxy with the name `<name>`.

This operation is only possible for TCP or HTTP proxies. To succeed, the backend instance must have
been first unpublished. Also, all of its servers must first be removed (via "del server" CLI).
Finally, no stream must still be attached to the backend instance.

There is additional restrictions which prevent backend removal. First, a backend cannot be removed
if it is explicitly referenced by config elements, for example via a use_backend rule or in sample
expressions. Some proxies options are also incompatible with runtime deletion. Currently, this is
the case when deprecated dispatch or option transparent are used. Also, a backend cannot be removed
if there is a stick-table declared in it. Finally, it is impossible for now to remove a backend if
QUIC servers were present in it.

It can be useful to use "wait be-removable" prior to this command to check for the aforementioned
requisites. This also provides a method to wait for the final closure of the streams attached to the
target backend.

This command is restricted and can only be issued on sockets configured for level "admin".

<a id="entry-9-3-del-map"></a>

**`del map <map> [<key>|#<ref>]`**

```haproxy
del map <map> [<key>|#<ref>]
```

Delete all the map entries from the map `<map>` corresponding to the key `<key>`. `<map>` is the
\#`<id>` or the `<name>` returned by "show map". If the `<ref>` is used, this command delete only
the listed reference. The reference can be found with listing the content of the map. Note that if
the reference `<map>` is a name and is shared with a acl, the entry will be also deleted in the map.

<a id="entry-9-3-del-ssl-ca-file"></a>

**`del ssl ca-file <cafile>`**

```haproxy
del ssl ca-file <cafile>
```

Delete a CA file tree entry from HAProxy. The CA file must be unused and removed from any crt-list.
"show ssl ca-file" displays the status of the CA files. The deletion doesn't work with a certificate
referenced directly with the "ca-file" or "ca-verify-file" directives in the configuration.

<a id="entry-9-3-del-ssl-cert"></a>

**`del ssl cert <certfile>`**

```haproxy
del ssl cert <certfile>
```

Delete a certificate store from HAProxy. The certificate must be unused (included for JWT
validation) and removed from any crt-list or directory. "show ssl cert" displays the status of the
certificate. The deletion doesn't work with a certificate referenced directly with the "crt"
directive in the configuration.

<a id="entry-9-3-del-ssl-crl-file"></a>

**`del ssl crl-file <crlfile>`**

```haproxy
del ssl crl-file <crlfile>
```

Delete a CRL file tree entry from HAProxy. The CRL file must be unused and removed from any
crt-list. "show ssl crl-file" displays the status of the CRL files. The deletion doesn't work with a
certificate referenced directly with the "crl-file" directive in the configuration.

<a id="entry-9-3-del-ssl-crt-list"></a>

**`del ssl crt-list <filename> <certfile[:line]>`**

```haproxy
del ssl crt-list <filename> <certfile[:line]>
```

Delete an entry in a crt-list. This will delete every SNIs used for this entry in the frontends. If
a certificate is used several time in a crt-list, you will need to provide which line you want to
delete. To display the line numbers, use "show ssl crt-list -n `<crtlist>`".

<a id="entry-9-3-del-ssl-ech"></a>

**`del ssl ech <bind>`**

```haproxy
del ssl ech <bind>
```

Delete the ECH keys of a bind line.

The bind line format is `<frontend>`/@`<filename>`:`<linenum>` (Example: frontend1/@haproxy.conf:19)
or `<frontend>`/`<name>` if the bind line was named with the "name" keyword.

Necessitates an OpenSSL version that supports ECH, and HAProxy must be compiled with USE_ECH=1. This
command is only supported on a CLI connection running in experimental mode (see "experimental-mode
on").

See also "show ssl ech", "add ssl ech" and "ech" in the [Section 5.1](/docs/haproxy/bind-and-server-options/#section-5-1) of the configuration manual.

Example:

```shell
$ echo "experimental-mode on; del ssl ech frontend1/@haproxy.conf:19" | socat /tmp/haproxy.sock -
deleted all ECH configs from frontend1/@haproxy.conf:19
```

<a id="entry-9-3-del-ssl-jwt"></a>

**`del ssl jwt <filename>`**

```haproxy
del ssl jwt <filename>
```

Remove an already loaded certificate to the list of certificates that can be used for JWT validation
(see "jwt_verify_cert" converter). This command does not work on ongoing transactions. See also "add
ssl jwt" and "show ssl jwt" commands. See "jwt" certificate option for more information.

<a id="entry-9-3-del-server"></a>

**`del server <backend>/<server>`**

```haproxy
del server <backend>/<server>
```

Delete a removable server attached to the backend `<backend>`. A removable server is the server
which satisfies all of these conditions:

- not referenced by other configuration elements
- must already be in maintenance (see "disable server")
- must not have any active or idle connections

If any of these conditions is not met, the command will fail.

Active connections are those with at least one ongoing request. It is possible to speed up their
termination using "shutdown sessions server". It is highly recommended to use "wait srv-removable"
before "del server" to ensure that all active or idle connections are closed and that the command
succeeds.

<a id="entry-9-3-disable-agent"></a>

**`disable agent <backend>/<server>`**

```haproxy
disable agent <backend>/<server>
```

Mark the auxiliary agent check as temporarily stopped.

In the case where an agent check is being run as a auxiliary check, due to the agent-check parameter
of a server directive, new checks are only initialized when the agent is in the enabled. Thus,
disable agent will prevent any new agent checks from begin initiated until the agent re-enabled
using enable agent.

When an agent is disabled the processing of an auxiliary agent check that was initiated while the
agent was set as enabled is as follows: All results that would alter the weight, specifically
"drain" or a weight returned by the agent, are ignored. The processing of agent check is otherwise
unchanged.

The motivation for this feature is to allow the weight changing effects of the agent checks to be
paused to allow the weight of a server to be configured using set weight without being overridden by
the agent.

This command is restricted and can only be issued on sockets configured for level "admin".

<a id="entry-9-3-disable-dynamic-cookie-backend"></a>

**`disable dynamic-cookie backend <backend>`**

```haproxy
disable dynamic-cookie backend <backend>
```

Disable the generation of dynamic cookies for the backend `<backend>`

<a id="entry-9-3-disable-frontend"></a>

**`disable frontend <frontend>`**

```haproxy
disable frontend <frontend>
```

Mark the frontend as temporarily stopped. This corresponds to the mode which is used during a soft
restart: the frontend releases the port but can be enabled again if needed. This should be used with
care as some non-Linux OSes are unable to enable it back. This is intended to be used in
environments where stopping a proxy is not even imaginable but a misconfigured proxy must be fixed.
That way it's possible to release the port and bind it into another process to restore operations.
The frontend will appear with status "STOP" on the stats page.

The frontend may be specified either by its name or by its numeric ID, prefixed with a sharp ('#').

This command is restricted and can only be issued on sockets configured for level "admin".

<a id="entry-9-3-disable-health"></a>

**`disable health <backend>/<server>`**

```haproxy
disable health <backend>/<server>
```

Mark the primary health check as temporarily stopped. This will disable sending of health checks,
and the last health check result will be ignored. The server will be in unchecked state and
considered UP unless an auxiliary agent check forces it down.

This command is restricted and can only be issued on sockets configured for level "admin".

<a id="entry-9-3-disable-server"></a>

**`disable server <backend>/<server>`**

```haproxy
disable server <backend>/<server>
```

Mark the server DOWN for maintenance. In this mode, no more checks will be performed on the server
until it leaves maintenance. If the server is tracked by other servers, those servers will be set to
DOWN during the maintenance.

In the statistics page, a server DOWN for maintenance will appear with a "MAINT" status, its
tracking servers with the "MAINT(via)" one.

Both the backend and the server may be specified either by their name or by their numeric ID,
prefixed with a sharp ('#').

This command is restricted and can only be issued on sockets configured for level "admin".

<a id="entry-9-3-dump-ssl-cert"></a>

**`dump ssl cert <certfile>`**

```haproxy
dump ssl cert <certfile>
```

Dump a certificate loaded into HAProxy memory. This will dump the certificate in PEM format, the
private key, then the leaf certificate and finally the chain will be dumped. You can also dump a
transaction by prefixing the filename by an asterisk. This is useful in order to save certificates
on the filesystem when it was updated on the CLI and not on the filesystem.

This command is restricted and can only be issued on sockets configured for level "admin".

Examples:

```shell
$ echo "dump ssl cert cert1.pem" | socat /tmp/sock1 -

$ echo "dump ssl cert cert1.pem" | socat /tmp/sock1 - | openssl storeutl -noout -text /dev/stdin
```

<a id="entry-9-3-dump-stats-file"></a>

**`dump stats-file`**

```haproxy
dump stats-file
```

Generate a stats-file which can be used to preload haproxy counters values on startup. See
"Stats-file" section for more detail.

<a id="entry-9-3-echo"></a>

**`echo <text>`**

```haproxy
echo <text>
```

Print some text with the CLI. Can be useful to wrote commentaries between commands when dumping the
result of multiple commands.

Example:

```text
echo "expert-mode on; echo FDs from fdtab; show fd; echo wild FDs; debug dev fd" | socat /var/run/haproxy.sock -

```

<a id="entry-9-3-enable-agent"></a>

**`enable agent <backend>/<server>`**

```haproxy
enable agent <backend>/<server>
```

Resume auxiliary agent check that was temporarily stopped.

See "disable agent" for details of the effect of temporarily starting and stopping an auxiliary
agent.

This command is restricted and can only be issued on sockets configured for level "admin".

<a id="entry-9-3-enable-dynamic-cookie-backend"></a>

**`enable dynamic-cookie backend <backend>`**

```haproxy
enable dynamic-cookie backend <backend>
```

Enable the generation of dynamic cookies for the backend `<backend>`. A secret key must also be
provided.

<a id="entry-9-3-enable-frontend"></a>

**`enable frontend <frontend>`**

```haproxy
enable frontend <frontend>
```

Resume a frontend which was temporarily stopped. It is possible that some of the listening ports
won't be able to bind anymore (eg: if another process took them since the 'disable frontend'
operation). If this happens, an error is displayed. Some operating systems might not be able to
resume a frontend which was disabled.

The frontend may be specified either by its name or by its numeric ID, prefixed with a sharp ('#').

This command is restricted and can only be issued on sockets configured for level "admin".

<a id="entry-9-3-enable-health"></a>

**`enable health <backend>/<server>`**

```haproxy
enable health <backend>/<server>
```

Resume a primary health check that was temporarily stopped. This will enable sending of health
checks again. Please see "disable health" for details.

This command is restricted and can only be issued on sockets configured for level "admin".

<a id="entry-9-3-enable-server"></a>

**`enable server <backend>/<server>`**

```haproxy
enable server <backend>/<server>
```

If the server was previously marked as DOWN for maintenance, this marks the server UP and checks are
re-enabled.

Both the backend and the server may be specified either by their name or by their numeric ID,
prefixed with a sharp ('#').

This command is restricted and can only be issued on sockets configured for level "admin".

<a id="entry-9-3-experimental-mode"></a>

**`experimental-mode [on|off]`**

```haproxy
experimental-mode [on|off]
```

Without options, this indicates whether the experimental mode is enabled or disabled on the current
connection. When passed "on", it turns the experimental mode on for the current CLI connection only.
With "off" it turns it off.

The experimental mode is used to access to extra features still in development. These features are
currently not stable and should be used with care. They may be subject to breaking changes across
versions.

When used from the master CLI, this command shouldn't be prefixed, as it will set the mode for any
worker when connecting to its CLI.

Example:

```text
echo "@1; experimental-mode on; <experimental_cmd>..." | socat /var/run/haproxy.master -
echo "experimental-mode on; @1 <experimental_cmd>..." | socat /var/run/haproxy.master -
```

<a id="entry-9-3-expert-mode"></a>

**`expert-mode [on|off]`**

```haproxy
expert-mode [on|off]
```

This command is similar to experimental-mode but is used to toggle the expert mode.

The expert mode enables displaying of expert commands that can be extremely dangerous for the
process and which may occasionally help developers collect important information about complex bugs.
Any misuse of these features will likely lead to a process crash. Do not use this option without
being invited to do so. Note that this command is purposely not listed in the help message. This
command is only accessible in admin level. Changing to another level automatically resets the expert
mode.

When used from the master CLI, this command shouldn't be prefixed, as it will set the mode for any
worker when connecting to its CLI.

Example:

```text
echo "@1; expert-mode on; debug dev exit 1" | socat /var/run/haproxy.master -
echo "expert-mode on; @1 debug dev exit 1" | socat /var/run/haproxy.master -
```

<a id="entry-9-3-get-map"></a>

**`get map <map> <value>`**

```haproxy
get map <map> <value>
get acl <acl> <value>
```

Lookup the value `<value>` in the map `<map>` or in the ACL `<acl>`. `<map>` or `<acl>` are the
\#`<id>` or the `<name>` returned by "show map" or "show acl". This command returns all the matching
patterns associated with this map. This is useful for debugging maps and ACLs. The output format is
composed by one line par matching type. Each line is composed by space-delimited series of words.

The first two words are:

```text
<match method>:   The match method applied. It can be "found", "bool",
                  "int", "ip", "bin", "len", "str", "beg", "sub", "dir",
                  "dom", "end" or "reg".

<match result>:   The result. Can be "match" or "no-match".
```

The following words are returned only if the pattern matches an entry.

     `<index type>`:     "tree" or "list". The internal lookup algorithm.

     `<case>`:           "case-insensitive" or "case-sensitive". The
                       interpretation of the case.

     `<entry matched>`:  match="`<entry>`". Return the matched pattern. It is
                       useful with regular expressions.

The two last word are used to show the returned value and its type. With the "acl" case, the pattern
doesn't exist.

     return=nothing:        No return because there are no "map".
     return="`<value>`":      The value returned in the string format.
     return=cannot-display: The value cannot be converted as string.

     type="`<type>`":         The type of the returned sample.

<a id="entry-9-3-get-var"></a>

**`get var <name>`**

```haproxy
get var <name>
```

Show the existence, type and contents of the process-wide variable 'name'. Only process-wide
variables are readable, so the name must begin with 'proc.' otherwise no variable will be found.
This command requires levels "operator" or "admin".

<a id="entry-9-3-get-weight"></a>

**`get weight <backend>/<server>`**

```haproxy
get weight <backend>/<server>
```

Report the current weight and the initial weight of server `<server>` in backend `<backend>` or an
error if either doesn't exist. The initial weight is the one that appears in the configuration file.
Both are normally equal unless the current weight has been changed. Both the backend and the server
may be specified either by their name or by their numeric ID, prefixed with a sharp ('#').

<a id="entry-9-3-help"></a>

**`help [<command>]`**

```haproxy
help [<command>]
```

Print the list of known keywords and their basic usage, or commands matching the requested one. The
same help screen is also displayed for unknown commands.

<a id="entry-9-3-httpclient"></a>

**`httpclient [--htx] <method> <URI>`**

```haproxy
httpclient [--htx] <method> <URI>
```

Launch an HTTP client request and print the response on the CLI. Only supported on a CLI connection
running in expert mode (see "expert-mode on"). It's only meant for debugging. The httpclient is able
to resolve a server name in the URL using the "default" resolvers section, which is populated with
the DNS servers of your /etc/resolv.conf by default. However it won't be able to resolve an host
from /etc/hosts if you don't use a local dns daemon which can resolve those.

The --htx option allow to use the haproxy internal htx representation using the htx_dump() function,
mainly used for debugging.

<a id="entry-9-3-new-ssl-ca-file"></a>

**`new ssl ca-file <cafile>`**

```haproxy
new ssl ca-file <cafile>
```

Create a new empty CA file tree entry to be filled with a set of CA certificates and added to a
crt-list. This command should be used in combination with "set ssl ca-file", "add ssl ca-file" and
"add ssl crt-list".

<a id="entry-9-3-new-ssl-cert"></a>

**`new ssl cert <filename>`**

```haproxy
new ssl cert <filename>
```

Create a new empty SSL certificate store to be filled with a certificate and added to a directory or
a crt-list. This command should be used in combination with "set ssl cert" and "add ssl crt-list".

<a id="entry-9-3-new-ssl-crl-file"></a>

**`new ssl crl-file <crlfile>`**

```haproxy
new ssl crl-file <crlfile>
```

Create a new empty CRL file tree entry to be filled with a set of CRLs and added to a crt-list. This
command should be used in combination with "set ssl crl-file" and "add ssl crt-list".

<a id="entry-9-3-prepare-acl"></a>

**`prepare acl <acl>`**

```haproxy
prepare acl <acl>
```

Allocate a new version number in ACL `<acl>` for atomic replacement. `<acl>` is the \#`<id>` or the
`<name>` returned by "show acl". The new version number is shown in response after "New version
created:". This number will then be usable to prepare additions of new entries into the ACL which
will then atomically replace the current ones once committed. It is reported as "next_ver" in "show
acl". There is no impact of allocating new versions, as unused versions will automatically be
removed once a more recent version is committed. Version numbers are unsigned 32-bit values which
wrap at the end, so care must be taken when comparing them in an external program. This command
cannot be used if the reference `<acl>` is a name also used as a map. In this case, the "prepare
map" command must be used instead.

<a id="entry-9-3-prepare-map"></a>

**`prepare map <map>`**

```haproxy
prepare map <map>
```

Allocate a new version number in map `<map>` for atomic replacement. `<map>` is the \#`<id>` or the
`<name>` returned by "show map". The new version number is shown in response after "New version
created:". This number will then be usable to prepare additions of new entries into the map which
will then atomically replace the current ones once committed. It is reported as "next_ver" in "show
map". There is no impact of allocating new versions, as unused versions will automatically be
removed once a more recent version is committed. Version numbers are unsigned 32-bit values which
wrap at the end, so care must be taken when comparing them in an external program.

<a id="entry-9-3-prompt"></a>

**`prompt [help | n | i | p | timed]*`**

```haproxy
prompt [help | n | i | p | timed]*
```

Changes the behavior of the interactive mode and the prompt displayed at the beginning of the line
in interactive mode: - "help" : displays the command's usage - "n" : switches to non-interactive
mode - "i" : switches to interactive mode - "p" : switches to interactive + prompt mode - "timed" :
toggles displaying the time in the prompt

Without any option, this will cycle through prompt mode then non-interactive mode. In
non-interactive mode, the connection is closed after the last command of the current line completes.
In interactive mode, the connection is not closed after a command completes, so that a new one can
be entered. In prompt mode, the interactive mode is still in use, and a prompt will appear at the
beginning of the line, indicating to the user that the interpreter is waiting for a new command. The
prompt consists in a right angle bracket followed by a space "\> ".

The prompt mode is more suited to human users, the interactive mode to advanced scripts, and the
non-interactive mode (default) to basic scripts. Note that the non-interactive mode is not available
for the master socket.

<a id="entry-9-3-publish-backend"></a>

**`publish backend <backend>`**

```haproxy
publish backend <backend>
```

Activates content switching to a backend instance. This is the reverse operation of "unpublish
backend" command. This command is restricted and can only be issued on sockets configured for levels
"operator" or "admin".

<a id="entry-9-3-quit"></a>

**`quit`**

```haproxy
quit
```

Close the connection when in interactive mode.

<a id="entry-9-3-set-anon"></a>

**`set anon [on|off] [<key>]`**

```haproxy
set anon [on|off] [<key>]
```

This command enables or disables the "anonymized mode" for the current CLI session, which replaces
certain fields considered sensitive or confidential in command outputs with hashes that preserve
sufficient consistency between elements to help developers identify relations between elements when
trying to spot bugs, but a low enough bit count (24) to make them non-reversible due to the high
number of possible matches. When turned on, if no key is specified, the global key will be used
(either specified in the configuration file by "anonkey" or set via the CLI command "set anon
global-key"). If no such key was set, a random one will be generated. Otherwise it's possible to
specify the 32-bit key to be used for the current session, for example, to reuse the key that was
used in a previous dump to help compare outputs. Developers will never need this key and it's
recommended never to share it as it could allow to confirm/infirm some guesses about what certain
hashes could be hiding.

<a id="entry-9-3-set-dynamic-cookie-key-backend"></a>

**`set dynamic-cookie-key backend <backend> <value>`**

```haproxy
set dynamic-cookie-key backend <backend> <value>
```

Modify the secret key used to generate the dynamic persistent cookies. This will break the existing
sessions.

<a id="entry-9-3-set-anon-global-key"></a>

**`set anon global-key <key>`**

```haproxy
set anon global-key <key>
```

This sets the global anonymizing key to `<key>`, which must be a 32-bit integer between 0 and
4294967295 (0 disables the global key). This command requires admin privilege.

<a id="entry-9-3-set-map"></a>

**`set map <map> [<key>|#<ref>] <value>`**

```haproxy
set map <map> [<key>|#<ref>] <value>
```

Modify the value corresponding to each key `<key>` in a map `<map>`. `<map>` is the \#`<id>` or
`<name>` returned by "show map". If the `<ref>` is used in place of `<key>`, only the entry pointed
by `<ref>` is changed. The new value is `<value>`.

<a id="entry-9-3-set-maxconn-frontend"></a>

**`set maxconn frontend <frontend> <value>`**

```haproxy
set maxconn frontend <frontend> <value>
```

Dynamically change the specified frontend's maxconn setting. Any positive value is allowed including
zero, but setting values larger than the global maxconn does not make much sense. If the limit is
increased and connections were pending, they will immediately be accepted. If it is lowered to a
value below the current number of connections, new connections acceptation will be delayed until the
threshold is reached. The frontend might be specified by either its name or its numeric ID prefixed
with a sharp ('#').

<a id="entry-9-3-set-maxconn-server"></a>

**`set maxconn server <backend/server> <value>`**

```haproxy
set maxconn server <backend/server> <value>
```

Dynamically change the specified server's maxconn setting. Any positive value is allowed including
zero, but setting values larger than the global maxconn does not make much sense.

<a id="entry-9-3-set-maxconn-global"></a>

**`set maxconn global <maxconn>`**

```haproxy
set maxconn global <maxconn>
```

Dynamically change the global maxconn setting within the range defined by the initial global maxconn
setting. If it is increased and connections were pending, they will immediately be accepted. If it
is lowered to a value below the current number of connections, new connections acceptation will be
delayed until the threshold is reached. A value of zero restores the initial setting.

<a id="entry-9-3-set-profiling-memory"></a>

**`set profiling memory { on | off }`**

```haproxy
set profiling memory { on | off }
set profiling tasks { auto | on | off | lock | no-lock | memory | no-memory }
```

Enables or disables CPU or memory profiling for the indicated subsystem. This is equivalent to
setting or clearing the "profiling" settings in the "global" section of the configuration file.
Please also see "show profiling". Note that manually setting the tasks profiling to "on"
automatically resets the scheduler statistics, thus allows to check activity over a given interval.
The memory profiling is limited to certain operating systems (known to work on the linux-glibc
target), and requires USE_MEMORY_PROFILING to be set at compile time.

. For tasks profiling, it is possible to enable or disable the collection of per-task lock and
memory timings at runtime, but the change is only taken into account next time the profiler switches
from off/auto to on (either automatically or manually). Thus when using "no-lock" to disable
per-task lock profiling and save CPU cycles, it is recommended to flip the task profiling off then
on to commit the change.

<a id="entry-9-3-set-rate-limit-connections-global"></a>

**`set rate-limit connections global <value>`**

```haproxy
set rate-limit connections global <value>
```

Change the process-wide connection rate limit, which is set by the global 'maxconnrate' setting. A
value of zero disables the limitation. This limit applies to all frontends and the change has an
immediate effect. The value is passed in number of connections per second.

<a id="entry-9-3-set-rate-limit-http-compression-global"></a>

**`set rate-limit http-compression global <value>`**

```haproxy
set rate-limit http-compression global <value>
```

Change the maximum input compression rate, which is set by the global 'maxcomprate' setting. A value
of zero disables the limitation. The value is passed in number of kilobytes per second. The value is
available in the "show info" on the line "CompressBpsRateLim" in bytes.

<a id="entry-9-3-set-rate-limit-sessions-global"></a>

**`set rate-limit sessions global <value>`**

```haproxy
set rate-limit sessions global <value>
```

Change the process-wide session rate limit, which is set by the global 'maxsessrate' setting. A
value of zero disables the limitation. This limit applies to all frontends and the change has an
immediate effect. The value is passed in number of sessions per second.

<a id="entry-9-3-set-rate-limit-ssl-sessions-global"></a>

**`set rate-limit ssl-sessions global <value>`**

```haproxy
set rate-limit ssl-sessions global <value>
```

Change the process-wide SSL session rate limit, which is set by the global 'maxsslrate' setting. A
value of zero disables the limitation. This limit applies to all frontends and the change has an
immediate effect. The value is passed in number of sessions per second sent to the SSL stack. It
applies before the handshake in order to protect the stack against handshake abuses.

<a id="entry-9-3-set-server"></a>

**`set server <backend>/<server> addr <ip4 or ip6 address> [port <port>]`**

```haproxy
set server <backend>/<server> addr <ip4 or ip6 address> [port <port>]
```

Replace the current IP address of a server by the one provided. Optionally, the port can be changed
using the 'port' parameter. Note that changing the port also support switching from/to port mapping
(notation with +X or -Y), only if a port is configured for the health check.

<a id="entry-9-3-set-server-2"></a>

**`set server <backend>/<server> agent [ up | down ]`**

```haproxy
set server <backend>/<server> agent [ up | down ]
```

Force a server's agent to a new state. This can be useful to immediately switch a server's state
regardless of some slow agent checks for example. Note that the change is propagated to tracking
servers if any.

<a id="entry-9-3-set-server-3"></a>

**`set server <backend>/<server> agent-addr <addr> [port <port>]`**

```haproxy
set server <backend>/<server> agent-addr <addr> [port <port>]
```

Change addr for servers agent checks. Allows to migrate agent-checks to another address at runtime.
You can specify both IP and hostname, it will be resolved. Optionally, change the port agent.

<a id="entry-9-3-set-server-4"></a>

**`set server <backend>/<server> agent-port <port>`**

```haproxy
set server <backend>/<server> agent-port <port>
```

Change the port used for agent checks.

<a id="entry-9-3-set-server-5"></a>

**`set server <backend>/<server> agent-send <value>`**

```haproxy
set server <backend>/<server> agent-send <value>
```

Change agent string sent to agent check target. Allows to update string while changing server
address to keep those two matching.

<a id="entry-9-3-set-server-6"></a>

**`set server <backend>/<server> health [ up | stopping | down ]`**

```haproxy
set server <backend>/<server> health [ up | stopping | down ]
```

Force a server's health to a new state. This can be useful to immediately switch a server's state
regardless of some slow health checks for example. Note that the change is propagated to tracking
servers if any.

<a id="entry-9-3-set-server-7"></a>

**`set server <backend>/<server> check-addr <ip4 | ip6> [port <port>]`**

```haproxy
set server <backend>/<server> check-addr <ip4 | ip6> [port <port>]
```

Change the IP address used for server health checks. Optionally, change the port used for server
health checks.

<a id="entry-9-3-set-server-8"></a>

**`set server <backend>/<server> check-port <port>`**

```haproxy
set server <backend>/<server> check-port <port>
```

Change the port used for health checking to `<port>`

<a id="entry-9-3-set-server-9"></a>

**`set server <backend>/<server> state [ ready | drain | maint ]`**

```haproxy
set server <backend>/<server> state [ ready | drain | maint ]
```

Force a server's administrative state to a new state. This can be useful to disable load balancing
and/or any traffic to a server. Setting the state to "ready" puts the server in normal mode, and the
command is the equivalent of the "enable server" command. Setting the state to "maint" disables any
traffic to the server as well as any health checks. This is the equivalent of the "disable server"
command. Setting the mode to "drain" only removes the server from load balancing but still allows it
to be checked and to accept new persistent connections. Changes are propagated to tracking servers
if any.

<a id="entry-9-3-set-server-10"></a>

**`set server <backend>/<server> weight <weight>[%]`**

```haproxy
set server <backend>/<server> weight <weight>[%]
```

Change a server's weight to the value passed in argument. This is the exact equivalent of the "set
weight" command below.

<a id="entry-9-3-set-server-11"></a>

**`set server <backend>/<server> fqdn <FQDN>`**

```haproxy
set server <backend>/<server> fqdn <FQDN>
```

Change a server's FQDN to the value passed in argument. This requires the internal run-time DNS
resolver to be configured and enabled for this server.

<a id="entry-9-3-set-server-12"></a>

**`set server <backend>/<server> ssl [ on | off ]  (deprecated)`**

```haproxy
set server <backend>/<server> ssl [ on | off ]  (deprecated)
```

This option configures SSL ciphering on outgoing connections to the server. When switch off, all
traffic becomes plain text; health check path is not changed.

This command is deprecated, create a new server dynamically with or without SSL instead, using the
"add server" command.

<a id="entry-9-3-set-severity-output"></a>

**`set severity-output [ none | number | string ]`**

```haproxy
set severity-output [ none | number | string ]
```

Change the severity output format of the stats socket connected to for the duration of the current
session.

<a id="entry-9-3-set-ssl-ca-file"></a>

**`set ssl ca-file <cafile> <payload>`**

```haproxy
set ssl ca-file <cafile> <payload>
```

this command is part of a transaction system, the "commit ssl ca-file" and "abort ssl ca-file"
commands could be required. if there is no on-going transaction, it will create a ca file tree entry
into which the certificates contained in the payload will be stored. the ca file entry will not be
stored in the ca file tree and will only be kept in a temporary transaction. if a transaction with
the same filename already exists, the previous ca file entry will be deleted and replaced by the new
one. once the modifications are done, you have to commit the transaction through a "commit ssl
ca-file" call. If you want to add multiple certificates separately, you can use the "add ssl
ca-file" command

Example:

```text
echo -e "set ssl ca-file cafile.pem <<\n$(cat rootCA.crt)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl ca-file cafile.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-set-ssl-cert"></a>

**`set ssl cert <filename> <payload>`**

```haproxy
set ssl cert <filename> <payload>
```

This command is part of a transaction system, the "commit ssl cert" and "abort ssl cert" commands
could be required. This whole transaction system works on any certificate displayed by the "show ssl
cert" command, so on any frontend or backend certificate. If there is no on-going transaction, it
will duplicate the certificate `<filename>` in memory to a temporary transaction, then update this
transaction with the PEM file in the payload. If a transaction exists with the same filename, it
will update this transaction. It's also possible to update the files linked to a certificate
(.issuer, .sctl, .ocsp etc.) Once the modification are done, you have to "commit ssl cert" the
transaction.

Injection of files over the CLI must be done with caution since an empty line is used to notify the
end of the payload. It is recommended to inject a PEM file which has been sanitized. A simple method
would be to remove every empty line and only leave what are in the PEM sections. It could be
achieved with a sed command.

Example:

```haproxy
# With some simple sanitizing
 echo -e "set ssl cert localhost.pem <<\n$(sed -n '/^$/d;/-BEGIN/,/-END/p' 127.0.0.1.pem)\n" | \
 socat /var/run/haproxy.stat -

 # Complete example with commit
 echo -e "set ssl cert localhost.pem <<\n$(cat 127.0.0.1.pem)\n" | \
 socat /var/run/haproxy.stat -
 echo -e \
 "set ssl cert localhost.pem.issuer <<\n $(cat 127.0.0.1.pem.issuer)\n" | \
 socat /var/run/haproxy.stat -
 echo -e \
 "set ssl cert localhost.pem.ocsp <<\n$(base64 -w 1000 127.0.0.1.pem.ocsp)\n" | \
 socat /var/run/haproxy.stat -
 echo "commit ssl cert localhost.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-set-ssl-crl-file"></a>

**`set ssl crl-file <crlfile> <payload>`**

```haproxy
set ssl crl-file <crlfile> <payload>
```

This command is part of a transaction system, the "commit ssl crl-file" and "abort ssl crl-file"
commands could be required. If there is no on-going transaction, it will create a CRL file tree
entry into which the Revocation Lists contained in the payload will be stored. The CRL file entry
will not be stored in the CRL file tree and will only be kept in a temporary transaction. If a
transaction with the same filename already exists, the previous CRL file entry will be deleted and
replaced by the new one. Once the modifications are done, you have to commit the transaction through
a "commit ssl crl-file" call.

Example:

```text
echo -e "set ssl crl-file crlfile.pem <<\n$(cat rootCRL.pem)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl crl-file crlfile.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-set-ssl-ech"></a>

**`set ssl ech <bind> <payload>`**

```haproxy
set ssl ech <bind> <payload>
```

Replace the ECH keys of a bind line with this one. The payload must be in the PEM for ECH format.
(<https://datatracker.ietf.org/doc/html/draft-farrell-tls-pemesni>)

The bind line format is `<frontend>`/@`<filename>`:`<linenum>` (Example: frontend1/@haproxy.conf:19)
or `<frontend>`/`<name>` if the bind line was named with the "name" keyword.

Necessitates an OpenSSL version that supports ECH, and HAProxy must be compiled with USE_ECH=1. This
command is only supported on a CLI connection running in experimental mode (see "experimental-mode
on").

See also "show ssl ech", "add ssl ech" and "ech" in the [Section 5.1](/docs/haproxy/bind-and-server-options/#section-5-1) of the configuration manual.

    $ openssl ech -public_name foobar.com -out foobar3.com.ech
    $ echo -e "experimental-mode on;
               set ssl ech frontend1/@haproxy.conf:19 <<%EOF%&#92;n$(cat foobar3.com.ech)&#92;n%EOF%&#92;n" | &#92;
      socat /tmp/haproxy.sock -
    set new ECH configs for frontend1/@haproxy.conf:19

<a id="entry-9-3-set-ssl-ocsp-response"></a>

**`set ssl ocsp-response <response | payload>`**

```haproxy
set ssl ocsp-response <response | payload>
```

This command is used to update an OCSP Response for a certificate (see "crt" on "bind" lines). Same
controls are performed as during the initial loading of the response. The `<response>` must be
passed as a base64 encoded string of the DER encoded response from the OCSP server. This command is
not supported with BoringSSL.

Example:

```text
openssl ocsp -issuer issuer.pem -cert server.pem \
             -host ocsp.issuer.com:80 -respout resp.der
echo "set ssl ocsp-response $(base64 -w 10000 resp.der)" | \
             socat stdio /var/run/haproxy.stat

using the payload syntax:
echo -e "set ssl ocsp-response <<\n$(base64 resp.der)\n" | \
             socat stdio /var/run/haproxy.stat
```

<a id="entry-9-3-set-ssl-tls-key"></a>

**`set ssl tls-key <id> <tlskey>`**

```haproxy
set ssl tls-key <id> <tlskey>
```

Set the next TLS key for the `<id>` listener to `<tlskey>`. This key becomes the ultimate key, while
the penultimate one is used for encryption (others just decrypt). The oldest TLS key present is
overwritten. `<id>` is either a numeric \#`<id>` or `<file>` returned by "show tls-keys". `<tlskey>`
is a base64 encoded 48 or 80 bytes TLS ticket key (ex. openssl rand 80 \| openssl base64 -A).

<a id="entry-9-3-set-table"></a>

**`set table <table> key <key> [data.<data_type> <value>]*`**

```haproxy
set table <table> key <key> [data.<data_type> <value>]*
set table <table> ptr <ptr> [data.<data_type> <value>]*
```

Create or update a stick-table entry in the table. If the key is not present, an entry is inserted.
See stick-table in section 4.2 to find all possible values for `<data_type>`. The most likely use
consists in dynamically entering entries for source IP addresses, with a flag in gpc0 to dynamically
block an IP address or affect its quality of service. It is possible to pass multiple data_types in
a single call.

Optional ptr lookup may be used instead of key lookup for an existing entry: `<ptr>` is written in
the form 0xffff and must correspond to the address returned by a previous "show table" command.
Matching an entry using its pointer may be relevant if the entry cannot be matched using the key due
to empty key or incompatible characters on the cli.

If data.`<data_type>` is an array type, "[]" may be used to access a specific index in the array,
like so: data.gpt[1]

<a id="entry-9-3-set-timeout-cli"></a>

**`set timeout cli <delay>`**

```haproxy
set timeout cli <delay>
```

Change the CLI interface timeout for current connection. This can be useful during long debugging
sessions where the user needs to constantly inspect some indicators without being disconnected. The
delay is passed in seconds.

<a id="entry-9-3-set-var"></a>

**`set var <name> <expression>`**

```haproxy
set var <name> <expression>
set var <name> expr <expression>
set var <name> fmt <format>
```

Allows to set or overwrite the process-wide variable 'name' with the result of expression
`<expression>` or format string `<format>`. Only process-wide variables may be used, so the name
must begin with 'proc.' otherwise no variable will be set. The `<expression>` and `<format>` may
only involve "internal" sample fetch keywords and converters even though the most likely useful ones
will be str('something'), int(), simple strings or references to other variables. Note that the
command line parser doesn't know about quotes, so any space in the expression must be preceded by a
backslash. This command requires levels "operator" or "admin". This command is only supported on a
CLI connection running in experimental mode (see "experimental-mode on").

<a id="entry-9-3-set-weight"></a>

**`set weight <backend>/<server> <weight>[%]`**

```haproxy
set weight <backend>/<server> <weight>[%]
```

Change a server's weight to the value passed in argument. If the value ends with the '%' sign, then
the new weight will be relative to the initially configured weight. Absolute weights are permitted
between 0 and 256. Relative weights must be positive with the resulting absolute weight is capped at
256. Servers which are part of a farm running a static load-balancing algorithm have stricter
limitations because the weight cannot change once set. Thus for these servers, the only accepted
values are 0 and 100% (or 0 and the initial weight). Changes take effect immediately, though certain
LB algorithms require a certain amount of requests to consider changes. A typical usage of this
command is to disable a server during an update by setting its weight to zero, then to enable it
again after the update by setting it back to 100%. This command is restricted and can only be issued
on sockets configured for level "admin". Both the backend and the server may be specified either by
their name or by their numeric ID, prefixed with a sharp ('#').

<a id="entry-9-3-show-acl"></a>

**`show acl [[@<ver>] <acl>]`**

```haproxy
show acl [[@<ver>] <acl>]
```

Dump info about acl converters. Without argument, the list of all available acls is returned. If a
`<acl>` is specified, its contents are dumped. `<acl>` is the \#`<id>` or `<name>`. By default the
current version of the ACL is shown (the version currently being matched against and reported as
'curr_ver' in the ACL list). It is possible to instead dump other versions by prepending '@`<ver>`'
before the ACL's identifier. The version works as a filter and non-existing versions will simply
report no result. The dump format is the same as for the maps even for the sample values. The data
returned are not a list of available ACL, but are the list of all patterns composing any ACL. Many
of these patterns can be shared with maps. The 'entry_cnt' value represents the count of all the ACL
entries, not just the active ones, which means that it also includes entries currently being added.

<a id="entry-9-3-show-anon"></a>

**`show anon`**

```haproxy
show anon
```

Display the current state of the anonymized mode (enabled or disabled) and the current session's
key.

<a id="entry-9-3-show-backend"></a>

**`show backend`**

```haproxy
show backend
```

Dump the list of backends available in the running process

<a id="entry-9-3-show-cli-level"></a>

**`show cli level`**

```haproxy
show cli level
```

Display the CLI level of the current CLI session. The result could be 'admin', 'operator' or 'user'.
See also the 'operator' and 'user' commands.

Example:

```shell
$ socat /tmp/sock1 readline
prompt
> operator
> show cli level
operator
> user
> show cli level
user
> operator
Permission denied
```

<a id="entry-9-3-operator"></a>

**`operator`**

```haproxy
operator
```

Decrease the CLI level of the current CLI session to operator. It can't be increased. It also drops
expert and experimental mode. See also "show cli level".

<a id="entry-9-3-unpublish-backend"></a>

**`unpublish backend <backend>`**

```haproxy
unpublish backend <backend>
```

Marks the backend as unqualified for future traffic selection. In effect, use_backend /
default_backend rules which reference it are ignored and the next content switching rules are
evaluated. Contrary to disabled backends, servers health checks remain active. This command is
restricted and can only be issued on sockets configured for levels "operator" or "admin".

<a id="entry-9-3-user"></a>

**`user`**

```haproxy
user
```

Decrease the CLI level of the current CLI session to user. It can't be increased. It also drops
expert and experimental mode. See also "show cli level".

<a id="entry-9-3-show-activity"></a>

**`show activity [-1 | 0 | thread_num]`**

```haproxy
show activity [-1 | 0 | thread_num]
```

Reports some counters about internal events that will help developers and more generally people who
know haproxy well enough to narrow down the causes of reports of abnormal behaviours. A typical
example would be a properly running process never sleeping and eating 100% of the CPU. The output
fields will be made of one line per metric, and per-thread counters on the same line. These counters
are 32-bit and will wrap during the process's life, which is not a problem since calls to this
command will typically be performed twice. The fields are purposely not documented so that their
exact meaning is verified in the code where the counters are fed. These values are also reset by the
"clear counters" command. On multi-threaded deployments, the first column will indicate the total
(or average depending on the nature of the metric) for all threads, and the list of all threads'
values will be represented between square brackets in the thread order. Optionally the thread number
to be dumped may be specified in argument. The special value "0" will report the aggregated value
(first column), and "-1", which is the default, will display all the columns. Note that just like in
single-threaded mode, there will be no brackets when a single column is requested.

<a id="entry-9-3-show-cli-sockets"></a>

**`show cli sockets`**

```haproxy
show cli sockets
```

List CLI sockets. The output format is composed of 3 fields separated by spaces. The first field is
the socket address, it can be a unix socket, a ipv4 address:port couple or a ipv6 one. Socket of
other types won't be dump. The second field describe the level of the socket: 'admin', 'user' or
'operator'. The last field list the processes on which the socket is bound, separated by commas, it
can be numbers or 'all'.

Example:

```shell
$ echo 'show cli sockets' | socat stdio /tmp/sock1
# socket lvl processes
/tmp/sock1 admin all
127.0.0.1:9999 user 2,3,4
127.0.0.2:9969 user 2
[::1]:9999 operator 2
```

<a id="entry-9-3-show-cache"></a>

**`show cache`**

```haproxy
show cache
```

List the configured caches and the objects stored in each cache tree.

\$ echo 'show cache' \| socat stdio /tmp/sock1 0x7f6ac6c5b03a: foobar (shctx:0x7f6ac6c5b000,
available blocks:3918) 1 2 3 4

1.  pointer to the cache structure
2.  cache name
3.  pointer to the mmap area (shctx)
4.  number of blocks available for reuse in the shctx

0x7f6ac6c5b4cc hash:286881868 vary:0x0011223344556677 size:39114 (39 blocks), refcount:9, expire:237
1 2 3 4 5 6 7

1.  pointer to the cache entry
2.  first 32 bits of the hash
3.  secondary hash of the entry in case of vary
4.  size of the object in bytes
5.  number of blocks used for the object
6.  number of transactions using the entry
7.  expiration time, can be negative if already expired

<a id="entry-9-3-show-dev"></a>

**`show dev`**

```haproxy
show dev
```

This command is meant to centralize some information that HAProxy developers might need to better
understand the causes of a given problem. It generally does not provide useful information for the
user, but these information allow developers to eliminate certain hypothesis. The format is roughly
a series of sections containing indented lines with one element per line, such as the OS type and
version, the CPU type or the boot-time FD limits for example. Some fields will be omitted to avoid
repetition or output pollution when they do not add value (e.g. unlimited values). More fields may
appear in the future, and some may change. This output is not meant for being parsed by scripts, and
should not be considered with a high degree of reliability, it's essentially aimed at saving time
for those who can read it.

Technically speaking, such information are taken as-is out of an internal structure that stores them
together at boot time so that they can also be found in a core file after a crash. As such, it may
happen that developers ask for an early output on a well behaving process to compare with what is
found in a core dump, or to compare between several reloads (e.g. some limits might change). If
anonymizing is enabled, any possibly sensitive value will be anonymized as well (e.g. the node
name).

Example of output:

```shell
$ socat stdio /tmp/sock1 <<< "show dev"
Platform info
  machine vendor: To be filled by O.E.M
  machine family: Altra
  cpu model: Impl 0x41 Arch 8 Part 0xd0c r3p1
  virtual machine: no
  container: no
  OS name: Linux
  OS release: 6.2.0-36-generic
  OS version: #37~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  9 18:01:07 UTC 2
  OS architecture: aarch64
  node name: 489aaf
Process info
  pid: 1735846
  boot uid: 509
  boot gid: 1002
  fd limit (soft): 1024
  fd limit (hard): 1048576
```

<a id="entry-9-3-show-env"></a>

**`show env [<name>]`**

```haproxy
show env [<name>]
```

Dump one or all environment variables known by the process. Without any argument, all variables are
dumped. With an argument, only the specified variable is dumped if it exists. Otherwise "Variable
not found" is emitted. Variables are dumped in the same format as they are stored or returned by the
"env" utility, that is, "`<name>`=`<value>`". This can be handy when debugging certain configuration
files making heavy use of environment variables to ensure that they contain the expected values.
This command is restricted and can only be issued on sockets configured for levels "operator" or
"admin".

<a id="entry-9-3-show-errors"></a>

**`show errors [<iid>|<proxy>] [request|response]`**

```haproxy
show errors [<iid>|<proxy>] [request|response]
```

Dump last known HTTP/1.x request and response errors collected by frontends and backends. If `<iid>`
is specified, the limit the dump to errors concerning either frontend or backend whose ID is
`<iid>`. Proxy ID "-1" will cause all instances to be dumped. If a proxy name is specified instead,
its ID will be used as the filter. If "request" or "response" is added after the proxy name or ID,
only request or response errors will be dumped. This command is restricted and can only be issued on
sockets configured for levels "operator" or "admin".

The errors which may be collected are the last request and response errors caused by protocol
violations, often due to invalid characters in header names. The report precisely indicates what
exact character violated the protocol. Other important information such as the exact date the error
was detected, frontend and backend names, the server name (when known), the internal transaction ID
and the source address which has initiated the session are reported too.

All characters are returned, and non-printable characters are encoded. The most common ones
(&#92;t = 9, &#92;n = 10, &#92;r =
13 and &#92;e = 27) are encoded as one letter following a backslash. The
backslash itself is encoded as '&#92;&#92;' to avoid
confusion. Other non-printable characters are encoded '&#92;xNN' where NN is
the two-digits hexadecimal representation of the character's ASCII code.

Lines are prefixed with the position of their first character, starting at 0 for the beginning of
the buffer. At most one input line is printed per line, and large lines will be broken into multiple
consecutive output lines so that the output never goes beyond 79 characters wide. It is easy to
detect if a line was broken, because it will not end with '&#92;n' and the
next line's offset will be followed by a '+' sign, indicating it is a continuation of previous line.

Example:

```shell
    $ echo "show errors -1 response" | socat stdio /tmp/sock1
>>> [04/Mar/2009:15:46:56.081] backend http-in (#2): invalid response
      src 127.0.0.1, session #54, frontend fe-eth0 (#1), server s2 (#1)
      response length 213 bytes, error at position 23:

      00000  HTTP/1.0 200 OK\r\n
      00017  header/bizarre:blah\r\n
      00038  Location: blah\r\n
      00054  Long-line: this is a very long line which should b
      00104+ e broken into multiple lines on the output buffer,
      00154+  otherwise it would be too large to print in a ter
      00204+ minal\r\n
      00211  \r\n

In the example above, we see that the backend "http-in" which has internal
ID 2 has blocked an invalid response from its server s2 which has internal
ID 1. The request was on transaction 54 (called "session" here) initiated
by source 127.0.0.1 and received by frontend fe-eth0 whose ID is 1. The
total response length was 213 bytes when the error was detected, and the
error was at byte 23. This is the slash ('/') in header name
"header/bizarre", which is not a valid HTTP character for a header name.
```

<a id="entry-9-3-show-events"></a>

**`show events [<sink>] [-w] [-n] [-0] [-s]`**

```haproxy
show events [<sink>] [-w] [-n] [-0] [-s]
```

With no option, this lists all known event sinks and their types. With an option, it will dump all
available events in the designated sink if it is of type buffer. If option "-w" is passed after the
sink name, then once the end of the buffer is reached, the command will wait for new events and
display them. It is possible to stop the operation by entering any input (which will be discarded)
or by closing the session. Finally, option "-n" is used to directly seek to the end of the buffer,
which is often convenient when combined with "-w" to only report new events. For convenience, "-wn"
or "-nw" may be used to enable both options at once. By default, all events are delimited by a line
feed character ('&#92;n' or 10 or 0x0A). It is possible to change this to the
NUL character ('&#92;0' or 0) by passing the "-0" argument. Option "-s"
sanitizes the output, so that binary contents resulting from captured or decoded data do not alter
the terminal's rendering. Whitespace characters (space and tab) are replaced with a space so that
each record stays on a single line, and the other control characters (0x00 to 0x1F and 0x7F) as well
as non-ASCII chars (0x80 and above) are replaced with a '?'. The output length is preserved. This
way, dumping a ring cannot inject ANSI escape sequences nor writing direction codes into the
operator's terminal, which is useful when dumping to a terminal, or to a program whose input must
not be interpreted as special (e.g. monitoring scripts whose output is copied verbatim into
reports).

<a id="entry-9-3-show-fd"></a>

**`show fd [-!plcfbsd]* [[<tgid>]/[<fd>] | <fd>]`**

```haproxy
show fd [-!plcfbsd]* [[<tgid>]/[<fd>] | <fd>]
```

Dump the list of either all open file descriptors or just the one number `<fd>` if specified. The
form "`<tgid>`/`<fd>`" is also accepted, where either side may be empty as a wildcard ("/`<fd>`" for
fd `<fd>` across thread groups, "`<tgid>`/" for all fds of `<tgid>`). The `<tgid>` is currently
parsed but ignored, pending future support for per-thread-group fd tables. A set of flags may
optionally be passed to restrict the dump only to certain FD types or to omit certain FD types. When
'-' or '!' are encountered, the selection is inverted for the following characters in the same
argument. The inversion is reset before each argument word delimited by white spaces. Selectable FD
types include 'p' for pipes, 'l' for listeners, 'c' for connections (any type), 'f' for frontend
connections, 'b' for backend connections (any type), 's' for connections to servers, 'd' for
connections to the "dispatch" address or the backend's transparent address. With this, 'b' is a
shortcut for 'sd' and 'c' for 'fb' or 'fsd'. 'c!f' is equivalent to 'b' ("any connections except
frontend connections" are indeed backend connections). This is only aimed at developers who need to
observe internal states in order to debug complex issues such as abnormal CPU usages. One fd is
reported per lines, and for each of them, its state in the poller using upper case letters for
enabled flags and lower case for disabled flags, using "P" for "polled", "R" for "ready", "A" for
"active", the events status using "H" for "hangup", "E" for "error", "O" for "output", "P" for
"priority" and "I" for "input", a few other flags like "N" for "new" (just added into the fd cache),
"U" for "updated" (received an update in the fd cache), "L" for "linger_risk", "C" for "cloned",
then the cached entry position, the pointer to the internal owner, the pointer to the I/O callback
and its name when known. When the owner is a connection, the connection flags, and the target are
reported (frontend, proxy or server). When the owner is a listener, the listener's state and its
frontend are reported. There is no point in using this command without a good knowledge of the
internals. It's worth noting that the output format may evolve over time so this output must not be
parsed by tools designed to be durable. Some internal structure states may look suspicious to the
function listing them, in this case the output line will be suffixed with an exclamation mark ('!').
This may help find a starting point when trying to diagnose an incident.

<a id="entry-9-3-show-info"></a>

**`show info [typed|json] [desc] [float]`**

```haproxy
show info [typed|json] [desc] [float]
```

Dump info about haproxy status on current process. If "typed" is passed as an optional argument,
field numbers, names and types are emitted as well so that external monitoring products can easily
retrieve, possibly aggregate, then report information found in fields they don't know. Each field is
dumped on its own line. If "json" is passed as an optional argument then information provided by
"typed" output is provided in JSON format as a list of JSON objects. By default, the format contains
only two columns delimited by a colon (':'). The left one is the field name and the right one is the
value. It is very important to note that in typed output format, the dump for a single object is
contiguous so that there is no need for a consumer to store everything at once. If "float" is passed
as an optional argument, some fields usually emitted as integers may switch to floats for higher
accuracy. It is purposely unspecified which ones are concerned as this might evolve over time. Using
this option implies that the consumer is able to process floats. The output format used is
sprintf("%f").

When using the typed output format, each line is made of 4 columns delimited by colons (':'). The
first column is a dot-delimited series of 3 elements. The first element is the numeric position of
the field in the list (starting at zero). This position shall not change over time, but holes are to
be expected, depending on build options or if some fields are deleted in the future. The second
element is the field name as it appears in the default "show info" output. The third element is the
relative process number starting at 1.

The rest of the line starting after the first colon follows the "typed output format" described in
the section above. In short, the second column (after the first ':') indicates the origin, nature
and scope of the variable. The third column indicates the type of the field, among "s32", "s64",
"u32", "u64" and "str". Then the fourth column is the value itself, which the consumer knows how to
parse thanks to column 3 and how to process thanks to column 2.

Thus the overall line format in typed mode is:

```text
<field_pos>.<field_name>.<process_num>:<tags>:<type>:<value>
```

When "desc" is appended to the command, one extra colon followed by a quoted string is appended with
a description for the metric. At the time of writing, this is only supported for the "typed" and
default output formats.

Example:

```shell
> show info
Name: HAProxy
Version: 1.7-dev1-de52ea-146
Release_date: 2016/03/11
Nbproc: 1
Process_num: 1
Pid: 28105
Uptime: 0d 0h00m04s
Uptime_sec: 4
Memmax_MB: 0
PoolAlloc_MB: 0
PoolUsed_MB: 0
PoolFailed: 0
(...)

> show info typed
0.Name.1:POSV:str:HAProxy
1.Version.1:POSV:str:3.1-dev0-7c653d-2466
2.Release_date.1:POSV:str:2025/07/01
3.Nbthread.1:CGSV:u32:1
4.Nbproc.1:CGSV:u32:1
5.Process_num.1:KGPV:u32:1
6.Pid.1:SGPV:u32:638069
7.Uptime.1:MDPV:str:0d 0h00m07s
8.Uptime_sec.1:MDPV:u32:7
9.Memmax_MB.1:CLPV:u32:0
10.PoolAlloc_MB.1:MGPV:u32:0
11.PoolUsed_MB.1:MGPV:u32:0
12.PoolFailed.1:MCPV:u32:0
(...)
```

In the typed format, the presence of the process ID at the end of the first column makes it very
easy to visually aggregate outputs from multiple processes. Example:

```shell
$ ( echo show info typed | socat /var/run/haproxy.sock1;    \
    echo show info typed | socat /var/run/haproxy.sock2 ) |  \
  sort -t . -k 1,1n -k 2,2 -k 3,3n
0.Name.1:POS:str:HAProxy
0.Name.2:POS:str:HAProxy
1.Version.1:POS:str:1.7-dev1-868ab3-148
1.Version.2:POS:str:1.7-dev1-868ab3-148
2.Release_date.1:POS:str:2016/03/11
2.Release_date.2:POS:str:2016/03/11
3.Nbproc.1:CGS:u32:2
3.Nbproc.2:CGS:u32:2
4.Process_num.1:KGP:u32:1
4.Process_num.2:KGP:u32:2
5.Pid.1:SGP:u32:30120
5.Pid.2:SGP:u32:30121
6.Uptime.1:MDP:str:0d 0h01m28s
6.Uptime.2:MDP:str:0d 0h01m28s
(...)
```

The format of JSON output is described in a schema which may be output using "show schema json".

The JSON output contains no extra whitespace in order to reduce the volume of output. For human
consumption passing the output through a pretty printer may be helpful. Example:

\$ echo "show info json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

The JSON output contains no extra whitespace in order to reduce the volume of output. For human
consumption passing the output through a pretty printer may be helpful. Example:

\$ echo "show info json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

<a id="entry-9-3-show-libs"></a>

**`show libs`**

```haproxy
show libs
```

Dump the list of loaded shared dynamic libraries and object files, on systems that support it. When
available, for each shared object the range of virtual addresses will be indicated, the size and the
path to the object. This can be used for example to try to estimate what library provides a function
that appears in a dump. Note that on many systems, addresses will change upon each restart (address
space randomization), so that this list would need to be retrieved upon startup if it is expected to
be used to analyse a core file. This command may only be issued on sockets configured for levels
"operator" or "admin". Note that the output format may vary between operating systems, architectures
and even haproxy versions, and ought not to be relied on in scripts.

<a id="entry-9-3-show-map"></a>

**`show map [[@<ver>] <map>]`**

```haproxy
show map [[@<ver>] <map>]
```

Dump info about map converters. Without argument, the list of all available maps is returned. If a
`<map>` is specified, its contents are dumped. `<map>` is the \#`<id>` or `<name>`. By default the
current version of the map is shown (the version currently being matched against and reported as
'curr_ver' in the map list). It is possible to instead dump other versions by prepending '@`<ver>`'
before the map's identifier. The version works as a filter and non-existing versions will simply
report no result. The 'entry_cnt' value represents the count of all the map entries, not just the
active ones, which means that it also includes entries currently being added.

In the output, the first column is a unique entry identifier, which is usable as a reference for
operations "del map" and "set map". The second column is the pattern and the third column is the
sample if available. The data returned are not directly a list of available maps, but are the list
of all patterns composing any map. Many of these patterns can be shared with ACL.

<a id="entry-9-3-show-peers"></a>

**`show peers [dict|-] [<peers section>]`**

```haproxy
show peers [dict|-] [<peers section>]
```

Dump info about the peers configured in "peers" sections. Without argument, the list of the peers
belonging to all the "peers" sections are listed. If `<peers section>` is specified, only the
information about the peers belonging to this "peers" section are dumped. When "dict" is specified
before the peers section name, the entire Tx/Rx dictionary caches will also be dumped (very large).
Passing "-" may be required to dump a peers section called "dict".

Here are two examples of outputs where hostA, hostB and hostC peers belong to "sharedlb" peers
sections. Only hostA and hostB are connected. Only hostA has sent data to hostB.

\$ echo "show peers" \| socat - /tmp/hostA 0x55deb0224320: [15/Apr/2019:11:28:01] id=sharedlb
state=0 flags=0x3 &#92; resync_timeout=`<PAST>` task_calls=45122
0x55deb022b540: id=hostC(remote) addr=127.0.0.12:10002 status=CONN &#92;
reconnect=4s confirm=0 flags=0x0 0x55deb022a440: id=hostA(local) addr=127.0.0.10:10000 status=NONE
&#92; reconnect=`<NEVER>` confirm=0 flags=0x0 0x55deb0227d70: id=hostB(remote)
addr=127.0.0.11:10001 status=ESTA reconnect=2s confirm=0 flags=0x20000200 appctx:0x55deb028fba0
st0=7 st1=0 task_calls=14456 &#92; state=EST xprt=RAW src=127.0.0.1:37257
addr=127.0.0.10:10000 remote_table:0x55deb0224a10 id=stkt local_id=1 remote_id=1
last_local_table:0x55deb0224a10 id=stkt local_id=1 remote_id=1 shared tables:

```text
0x55deb0224a10 local_id=1 remote_id=1 flags=0x0 remote_data=0x65
  last_acked=0 last_pushed=3 last_get=0 teaching_origin=0 update=3
  table:0x55deb022d6a0 id=stkt update=3 localupdate=3 \
    commitupdate=3 syncing=0
```

\$ echo "show peers" \| socat - /tmp/hostB 0x55871b5ab320: [15/Apr/2019:11:28:03] id=sharedlb
state=0 flags=0x3 &#92; resync_timeout=`<PAST>` task_calls=3 0x55871b5b2540:
id=hostC(remote) addr=127.0.0.12:10002 status=CONN &#92; reconnect=3s
confirm=0 flags=0x0 0x55871b5b1440: id=hostB(local) addr=127.0.0.11:10001 status=NONE
&#92; reconnect=`<NEVER>` confirm=0 flags=0x0 0x55871b5aed70: id=hostA(remote)
addr=127.0.0.10:10000 status=ESTA &#92; reconnect=2s confirm=0
flags=0x20000200 appctx:0x7fa46800ee00 st0=7 st1=0 task_calls=62356 &#92;
state=EST remote_table:0x55871b5ab960 id=stkt local_id=1 remote_id=1 last_local_table:0x55871b5ab960
id=stkt local_id=1 remote_id=1 shared tables:

```text
0x55871b5ab960 local_id=1 remote_id=1 flags=0x0 remote_data=0x65
  last_acked=3 last_pushed=0 last_get=3 teaching_origin=0 update=0
  table:0x55871b5b46a0 id=stkt update=1 localupdate=0 \
    commitupdate=0 syncing=0
```

<a id="entry-9-3-show-pools"></a>

**`show pools [byname|bysize|byusage] [detailed] [match <pfx>] [<nb>]`**

```haproxy
show pools [byname|bysize|byusage] [detailed] [match <pfx>] [<nb>]
```

Dump the status of internal memory pools. This is useful to track memory usage when suspecting a
memory leak for example. It does exactly the same as the SIGQUIT when running in foreground except
that it does not flush the pools. The output is not sorted by default. If "byname" is specified, it
is sorted by pool name; if "bysize" is specified, it is sorted by item size in reverse order; if
"byusage" is specified, it is sorted by total usage in reverse order, and only used entries are
shown. It is also possible to limit the output to the `<nb>` first entries (e.g. when sorting by
usage). It is possible to also dump more internal details, including the list of all pools that were
merged together, by specifying "detailed". Finally, if "match" followed by a prefix is specified,
then only pools whose name starts with this prefix will be shown. The reported total only concerns
pools matching the filtering criteria. Example:

```shell
$ socat - /tmp/haproxy.sock <<< "show pools match quic byusage"
Dumping pools usage. Use SIGQUIT to flush them.
  - Pool quic_conn_r (65560 bytes): 1337 allocated (87653720 bytes), ...
  - Pool quic_crypto (1048 bytes): 6685 allocated (7005880 bytes), ...
  - Pool quic_conn (4056 bytes): 1337 allocated (5422872 bytes), ...
  - Pool quic_rxbuf (262168 bytes): 8 allocated (2097344 bytes), ...
  - Pool quic_conne (184 bytes): 9359 allocated (1722056 bytes), ...
  - Pool quic_frame (184 bytes): 7938 allocated (1460592 bytes), ...
  - Pool quic_tx_pac (152 bytes): 6454 allocated (981008 bytes), ...
  - Pool quic_tls_ke (56 bytes): 12033 allocated (673848 bytes), ...
  - Pool quic_rx_pac (408 bytes): 1596 allocated (651168 bytes), ...
  - Pool quic_tls_se (88 bytes): 6685 allocated (588280 bytes), ...
  - Pool quic_cstrea (88 bytes): 4011 allocated (352968 bytes), ...
  - Pool quic_tls_iv (24 bytes): 12033 allocated (288792 bytes), ...
  - Pool quic_dgram (344 bytes): 732 allocated (251808 bytes), ...
  - Pool quic_arng (56 bytes): 4011 allocated (224616 bytes), ...
  - Pool quic_conn_c (152 bytes): 1337 allocated (203224 bytes), ...
Total: 15 pools, 109578176 bytes allocated, 109578176 used ...
```

<a id="entry-9-3-show-profiling"></a>

**`show profiling [{all | status | tasks | memory}] [byaddr|bytime|byctx|aggr|<max_lines>]*`**

```haproxy
show profiling [{all | status | tasks | memory}] [byaddr|bytime|byctx|aggr|<max_lines>]*
```

Dumps the current profiling settings, one per line, as well as the command needed to change them.
When tasks profiling is enabled, some per-function statistics collected by the scheduler will also
be emitted, with a summary covering the number of calls, total/avg CPU time and total/avg latency.
When memory profiling is enabled, some information such as the number of allocations/releases and
their sizes will be reported. It is possible to limit the dump to only the profiling status, the
tasks, or the memory profiling by specifying the respective keywords; by default all profiling
information are dumped. It is also possible to limit the number of lines of of output of each
category by specifying a numeric limit. If is possible to request that the output is sorted by
address, by total execution time, or by calling context instead of usage, e.g. to ease comparisons
between subsequent calls or to check what needs to be optimized, and to aggregate task activity by
called function instead of seeing the details. Please note that profiling is essentially aimed at
developers since it gives hints about where CPU cycles or memory are wasted in the code. There is
nothing useful to monitor there.

<a id="entry-9-3-show-resolvers"></a>

**`show resolvers [<resolvers section id>]`**

```haproxy
show resolvers [<resolvers section id>]
```

Dump statistics for the given resolvers section, or all resolvers sections if no section is
supplied.

For each name server, the following counters are reported:

```text
sent: number of DNS requests sent to this server
valid: number of DNS valid responses received from this server
update: number of DNS responses used to update the server's IP address
cname: number of CNAME responses
cname_error: CNAME errors encountered with this server
any_err: number of empty response (IE: server does not support ANY type)
nx: non existent domain response received from this server
timeout: how many time this server did not answer in time
refused: number of requests refused by this server
other: any other DNS errors
invalid: invalid DNS response (from a protocol point of view)
too_big: too big response
outdated: number of response arrived too late (after another name server)
```

<a id="entry-9-3-show-quic"></a>

**`show quic [<format>] [<filter>]`**

```haproxy
show quic [<format>] [<filter>]
```

Dump information on all active QUIC frontend connections. This command is restricted and can only be
issued on sockets configured for levels "operator" or "admin".

An optional argument can be specified to control the verbosity. Its value can be interpreted in
different way. The first possibility is to used predefined values, "oneline" for the default format,
"stream" to list every active streams and "full" to display all information. Alternatively, a list
of comma-delimited fields can be specified to restrict output. Currently supported values are "tp",
"sock", "pktns", "cc" and "mux". Finally, "help" in the format will instead show a more detailed
help message.

The final argument is used to restrict or extend the connection list. By default, active frontend
connections only are displayed. Use the extra argument "clo" to list instead closing frontend
connections, "be" for backend connections or "all" for every categories. It's also possible to
restrict to a single connection by specifying its hexadecimal address.

<a id="entry-9-3-show-servers-conn"></a>

**`show servers conn [<backend>]`**

```haproxy
show servers conn [<backend>]
```

Dump the current and idle connections state of the servers belonging to the designated backend (or
all backends if none specified). A backend name or identifier may be used.

The output consists in a header line showing the fields titles, then one server per line with for
each, the backend name and ID, server name and ID, the address, port and a series or values. The
number of fields varies depending on thread count. The exact format of the output may vary slightly
across versions and depending on the number of threads. One needs to pay attention to the header
line to match columns when extracting output values, and to the number of threads as the last
columns are per-thread:

```text
bkname/svname         Backend name '/' server name
bkid/svid             Backend ID '/' server ID
addr                  Server's IP address
port                  Server's port (or zero if none)
-                     Unused field, serves as a visual delimiter
purge_delay           Interval between connection purges, in milliseconds
served                Number of connections currently in use
used_cur              Number of connections currently in use
                      note that this excludes conns attached to a session
used_max              Highest value of used_cur since the process started
need_est              Floating estimate of total needed connections
idle_sess             Number of idle connections flagged as private
unsafe_nb             Number of idle connections considered as "unsafe"
safe_nb               Number of idle connections considered as "safe"
idle_lim              Configured maximum number of idle connections
idle_cur              Total of the per-thread currently idle connections
idle_per_thr[NB]      Idle conns per thread for each one of the NB threads
```

HAProxy will kill a portion of `<idle_cur>` every `<purge_delay>` when the total of `<idle_cur>` +
`<used_cur>` exceeds the estimate `<need_est>`. This estimate varies based on connection activity.

Given the threaded nature of idle connections, it's important to understand that some values may
change once read, and that as such, consistency within a line isn't granted. This output is mostly
provided as a debugging tool and is not relevant to be routinely monitored nor graphed.

<a id="entry-9-3-show-servers-state"></a>

**`show servers state [<backend>]`**

```haproxy
show servers state [<backend>]
```

Dump the state of the servers found in the running configuration. A backend name or identifier may
be provided to limit the output to this backend only.

The dump has the following format:

- first line contains the format version (1 in this specification);
- second line contains the column headers, prefixed by a sharp ('#');
- third line and next ones contain data;
- each line starting by a sharp ('#') is considered as a comment.

Since multiple versions of the output may co-exist, below is the list of fields and their order per
file format version:

```text
1:
  be_id:                       Backend unique id.
  be_name:                     Backend label.
  srv_id:                      Server unique id (in the backend).
  srv_name:                    Server label.
  srv_addr:                    Server IP address.
  srv_op_state:                Server operational state (UP/DOWN/...).
                                 0 = SRV_ST_STOPPED
                                   The server is down.
                                 1 = SRV_ST_STARTING
                                   The server is warming up (up but
                                   throttled).
                                 2 = SRV_ST_RUNNING
                                   The server is fully up.
                                 3 = SRV_ST_STOPPING
                                   The server is up but soft-stopping
                                   (eg: 404).
  srv_admin_state:             Server administrative state (MAINT/DRAIN/...).
                               The state is actually a mask of values:
                                 0x01 = SRV_ADMF_FMAINT
                                   The server was explicitly forced into
                                   maintenance.
                                 0x02 = SRV_ADMF_IMAINT
                                   The server has inherited the maintenance
                                   status from a tracked server.
                                 0x04 = SRV_ADMF_CMAINT
                                   The server is in maintenance because of
                                   the configuration.
                                 0x08 = SRV_ADMF_FDRAIN
                                   The server was explicitly forced into
                                   drain state.
                                 0x10 = SRV_ADMF_IDRAIN
                                   The server has inherited the drain status
                                   from a tracked server.
                                 0x20 = SRV_ADMF_RMAINT
                                   The server is in maintenance because of an
                                   IP address resolution failure.
                                 0x40 = SRV_ADMF_HMAINT
                                   The server FQDN was set from stats socket.

  srv_uweight:                 User visible server's weight.
  srv_iweight:                 Server's initial weight.
  srv_time_since_last_change:  Time since last operational change.
  srv_check_status:            Last health check status.
  srv_check_result:            Last check result (FAILED/PASSED/...).
                                 0 = CHK_RES_UNKNOWN
                                   Initialized to this by default.
                                 1 = CHK_RES_NEUTRAL
                                   Valid check but no status information.
                                 2 = CHK_RES_FAILED
                                   Check failed.
                                 3 = CHK_RES_PASSED
                                   Check succeeded and server is fully up
                                   again.
                                 4 = CHK_RES_CONDPASS
                                   Check reports the server doesn't want new
                                   sessions.
  srv_check_health:            Checks rise / fall current counter.
  srv_check_state:             State of the check (ENABLED/PAUSED/...).
                               The state is actually a mask of values:
                                 0x01 = CHK_ST_INPROGRESS
                                   A check is currently running.
                                 0x02 = CHK_ST_CONFIGURED
                                   This check is configured and may be
                                   enabled.
                                 0x04 = CHK_ST_ENABLED
                                   This check is currently administratively
                                   enabled.
                                 0x08 = CHK_ST_PAUSED
                                   Checks are paused because of maintenance
                                   (health only).
  srv_agent_state:             State of the agent check (ENABLED/PAUSED/...).
                               This state uses the same mask values as
                               "srv_check_state", adding this specific one:
                                 0x10 = CHK_ST_AGENT
                                   Check is an agent check (otherwise it's a
                                   health check).
  bk_f_forced_id:              Flag to know if the backend ID is forced by
                               configuration.
  srv_f_forced_id:             Flag to know if the server's ID is forced by
                               configuration.
  srv_fqdn:                    Server FQDN.
  srv_port:                    Server port.
  srvrecord:                   DNS SRV record associated to this SRV.
  srv_use_ssl:                 use ssl for server connections.
  srv_check_port:              Server health check port.
  srv_check_addr:              Server health check address.
  srv_agent_addr:              Server health agent address.
  srv_agent_port:              Server health agent port.
```

<a id="entry-9-3-show-sess"></a>

**`show sess [<options>*]`**

```haproxy
show sess [<options>*]
```

Dump all known active streams (formerly called "sessions"). Avoid doing this on slow connections as
this can be huge. This command is restricted and can only be issued on sockets configured for levels
"operator" or "admin". Note that on machines with quickly recycled connections, it is possible that
this output reports less entries than really exist because it will dump all existing streams up to
the last one that was created before the command was entered; those which die in the mean time will
not appear. For supported options, see below.

<a id="entry-9-3-show-sess-2"></a>

**`show sess [<id> | all | help] [<options>*]`**

```haproxy
show sess [<id> | all | help] [<options>*]
```

Display a lot of internal information about the matching streams. The command knows two output
formats: a short one, which is the default when not asking for a specific stream identifier, and an
extended one when listing designated streams. The short format, used by default with "show sess",
only dumps one stream per line with a few info, and the stream identifier at the beginning of the
line in hexadecimal (it corresponds to the pointer to the stream).

In the extended form, used by "show sess `<id>`" or "show sess all", streams are dumped with a huge
amount of debugging details over multiple lines (around 20 each), and still start with their
identifier. The delimiter between streams here is the identifier at the beginning of the line; extra
lines belonging to the same stream start with one or multiple spaces (the stream is dumped
indented). Dumping many streams can produce a huge output, take a lot of time and be CPU intensive,
so it's always better to only dump the minimum needed. Those information are useless to most users
but may be used by HAProxy developers to troubleshoot a complex bug. The exact output format is
intentionally not documented so that it can freely evolve depending on requirements, including in
stable branches. This output is meant to be interpreted while checking function
strm_dump_to_buffer() in src/stream.c to figure the exact meaning of certain fields.

The "help" argument will show the detailed usage of the command instead of dumping streams.

It is possible to set some options to customize the dump or apply some filters. Here are the
supported options: - backend `<b>` only display streams attached to this backend - frontend `<f>`
only display streams attached to this frontend - older `<age>` only display streams older than
`<age>` seconds - server `<b/s>` only show streams attached to this backend+server - show-uri dump
the transaction URI, as captured during the request analysis. It is only displayed if it was
captured. - susp only show streams considered as suspicious by the developers based on criteria that
may in time or vary along versions.

<a id="entry-9-3-show-stat"></a>

**`show stat [domain <resolvers|proxy>] [{<iid>|<proxy>} <type> <sid>] \`**

```haproxy
show stat [domain <resolvers|proxy>] [{<iid>|<proxy>} <type> <sid>] \
          [typed|json] [desc] [up|no-maint]
```

Dump statistics. The domain is used to select which statistics to print; resolvers and proxy are
available for now. By default, the CSV format is used; you can activate the extended typed output
format described in the section above if "typed" is passed after the other arguments; or in JSON if
"json" is passed after the other arguments. By passing `<id>`, `<type>` and `<sid>`, it is possible
to dump only selected items: - `<iid>` is a proxy ID, -1 to dump everything. Alternatively, a proxy
name `<proxy>` may be specified. In this case, this proxy's ID will be used as the ID selector. -
`<type>` selects the type of dumpable objects: 1 for frontends, 2 for backends, 4 for servers, -1
for everything. These values can be ORed, for example:

```text
1 + 2     = 3   -> frontend + backend.
1 + 2 + 4 = 7   -> frontend + backend + server.
```

    - `<sid>` is a server ID, -1 to dump everything from the selected proxy.

Example:

```shell
    $ echo "show info;show stat" | socat stdio unix-connect:/tmp/sock1
>>> Name: HAProxy
    Version: 1.4-dev2-49
    Release_date: 2009/09/23
    Nbproc: 1
    Process_num: 1
    (...)

    # pxname,svname,qcur,qmax,scur,smax,slim,stot,bin,bout,dreq,  (...)
    stats,FRONTEND,,,0,0,1000,0,0,0,0,0,0,,,,,OPEN,,,,,,,,,1,1,0, (...)
    stats,BACKEND,0,0,0,0,1000,0,0,0,0,0,,0,0,0,0,UP,0,0,0,,0,250,(...)
    (...)
    www1,BACKEND,0,0,0,0,1000,0,0,0,0,0,,0,0,0,0,UP,1,1,0,,0,250, (...)

    $
```

In this example, two commands have been issued at once. That way it's easy to find which process the
stats apply to in multi-process mode. This is not needed in the typed output format as the process
number is reported on each line. Notice the empty line after the information output which marks the
end of the first block. A similar empty line appears at the end of the second block (stats) so that
the reader knows the output has not been truncated.

When "typed" is specified, the output format is more suitable to monitoring tools because it
provides numeric positions and indicates the type of each output field. Each value stands on its own
line with process number, element number, nature, origin and scope. This same format is available
via the HTTP stats by passing ";typed" after the URI. It is very important to note that in typed
output format, the dump for a single object is contiguous so that there is no need for a consumer to
store everything at once.

The "up" modifier will result in listing only servers which reportedly up or not checked. Those
down, unresolved, or in maintenance will not be listed. This is analogous to the ";up" option on the
HTTP stats. Similarly, the "no-maint" modifier will act like the ";no-maint" HTTP modifier and will
result in disabled servers not to be listed. The difference is that those which are enabled but down
will not be evicted.

When using the typed output format, each line is made of 4 columns delimited by colons (':'). The
first column is a dot-delimited series of 5 elements. The first element is a letter indicating the
type of the object being described. At the moment the following object types are known: 'F' for a
frontend, 'B' for a backend, 'L' for a listener, and 'S' for a server. The second element The second
element is a positive integer representing the unique identifier of the proxy the object belongs to.
It is equivalent to the "iid" column of the CSV output and matches the value in front of the
optional "id" directive found in the frontend or backend section. The third element is a positive
integer containing the unique object identifier inside the proxy, and corresponds to the "sid"
column of the CSV output. ID 0 is reported when dumping a frontend or a backend. For a listener or a
server, this corresponds to their respective ID inside the proxy. The fourth element is the numeric
position of the field in the list (starting at zero). This position shall not change over time, but
holes are to be expected, depending on build options or if some fields are deleted in the future.
The fifth element is the field name as it appears in the CSV output. The sixth element is a positive
integer and is the relative process number starting at 1.

The rest of the line starting after the first colon follows the "typed output format" described in
the section above. In short, the second column (after the first ':') indicates the origin, nature,
scope and persistence state of the variable. The third column indicates the field type, among "s32",
"s64", "u32", "u64", "flt" and "str". Then the fourth column is the value itself, which the consumer
knows how to parse thanks to column 3 and how to process thanks to column 2.

When "desc" is appended to the command, one extra colon followed by a quoted string is appended with
a description for the metric. At the time of writing, this is only supported for the "typed" output
format.

Thus the overall line format in typed mode is:

```text
<obj>.<px_id>.<id>.<fpos>.<fname>.<process_num>:<tags>:<type>:<value>
```

Here's an example of typed output format:

```shell
$ echo "show stat typed" | socat stdio unix-connect:/tmp/sock1
F.2.0.0.pxname.1:KNSV:str:dummy
F.2.0.1.svname.1:KNSV:str:FRONTEND
F.2.0.4.scur.1:MGPV:u32:0
F.2.0.5.smax.1:MMPV:u32:0
F.2.0.6.slim.1:CLPV:u32:524269
F.2.0.7.stot.1:MCPP:u64:0
F.2.0.8.bin.1:MCPP:u64:0
F.2.0.9.bout.1:MCPP:u64:0
F.2.0.10.dreq.1:MCPP:u64:0
F.2.0.11.dresp.1:MCPP:u64:0
F.2.0.12.ereq.1:MCPP:u64:0
F.2.0.17.status.1:SGPV:str:OPEN
F.2.0.26.pid.1:KGPV:u32:1
F.2.0.27.iid.1:KGSV:u32:2
F.2.0.28.sid.1:KGSV:u32:0
F.2.0.32.type.1:CGSV:u32:0
F.2.0.33.rate.1:MRPP:u32:0
F.2.0.34.rate_lim.1:CLPV:u32:0
F.2.0.35.rate_max.1:MMPV:u32:0
F.2.0.46.req_rate.1:MRPP:u32:0
F.2.0.47.req_rate_max.1:MMPV:u32:0
F.2.0.48.req_tot.1:MCPP:u64:0
F.2.0.51.comp_in.1:MCPP:u64:0
F.2.0.52.comp_out.1:MCPP:u64:0
F.2.0.53.comp_byp.1:MCPP:u64:0
F.2.0.54.comp_rsp.1:MCPP:u64:0
(...)
```

In the typed format, the presence of the process ID at the end of the first column makes it very
easy to visually aggregate outputs from multiple processes, as show in the example below where each
line appears for each process:

```shell
$ ( echo show stat typed | socat /var/run/haproxy.sock1 -; \
    echo show stat typed | socat /var/run/haproxy.sock2 - ) | \
  sort -t . -k 1,1 -k 2,2n -k 3,3n -k 4,4n -k 5,5 -k 6,6n
B.3.0.0.pxname.1:KNSV:str:private-backend
B.3.0.0.pxname.2:KNSV:str:private-backend
B.3.0.1.svname.1:KNSV:str:BACKEND
B.3.0.1.svname.2:KNSV:str:BACKEND
B.3.0.2.qcur.1:MGPV:u32:0
B.3.0.2.qcur.2:MGPV:u32:0
B.3.0.3.qmax.1:MMPV:u32:0
B.3.0.3.qmax.2:MMPV:u32:0
B.3.0.4.scur.1:MGPV:u32:0
B.3.0.4.scur.2:MGPV:u32:0
B.3.0.5.smax.1:MMPV:u32:0
B.3.0.5.smax.2:MMPV:u32:0
B.3.0.6.slim.1:CLPV:u32:1000
B.3.0.6.slim.2:CLPV:u32:1000
(...)
```

The format of JSON output is described in a schema which may be output using "show schema json".

The JSON output contains no extra whitespace in order to reduce the volume of output. For human
consumption passing the output through a pretty printer may be helpful. Example:

\$ echo "show stat json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

The JSON output contains no extra whitespace in order to reduce the volume of output. For human
consumption passing the output through a pretty printer may be helpful. Example:

\$ echo "show stat json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

<a id="entry-9-3-show-ssl-ca-file"></a>

**`show ssl ca-file [[*][\]<cafile>[:<index>]]`**

```haproxy
show ssl ca-file [[*][\]<cafile>[:<index>]]
```

Display the list of CA files loaded into the process and their respective certificate counts. The
certificates are not used by any frontend or backend until their status is "Used". A "@system-ca"
entry can appear in the list, it is loaded by the httpclient by default. It contains the list of
trusted CA of your system returned by OpenSSL. If a filename is prefixed by an asterisk, it is a
transaction which is not committed yet. If a `<cafile>` is specified without `<index>`, it will show
the status of the CA file ("Used"/"Unused") followed by details about all the certificates contained
in the CA file. The details displayed for every certificate are the same as the ones displayed by a
"show ssl cert" command. If a `<cafile>` is specified followed by an `<index>`, it will only display
the details of the certificate having the specified index. Indexes start from 1. If the index is
invalid (too big for instance), nothing will be displayed. This command can be useful to check if a
CA file was properly updated. You can also display the details of an ongoing transaction by
prefixing the filename by a '*'. If the first character of the filename is a '*', it can be escaped
with '&#92;\*'.

Example:

```shell
$ echo "show ssl ca-file" | socat /var/run/haproxy.master -
# transaction
*cafile.crt - 2 certificate(s)
# filename
cafile.crt - 1 certificate(s)

$ echo "show ssl ca-file cafile.crt" | socat /var/run/haproxy.master -
Filename: /home/tricot/work/haproxy/reg-tests/ssl/set_cafile_ca2.crt
Status: Used

Certificate #1:
Serial: 11A4D2200DC84376E7D233CAFF39DF44BF8D1211
notBefore: Apr  1 07:40:53 2021 GMT
notAfter: Aug 17 07:40:53 2048 GMT
Subject Alternative Name:
Algorithm: RSA4096
SHA1 FingerPrint: A111EF0FEFCDE11D47FE3F33ADCA8435EBEA4864
Subject: /C=FR/ST=Some-State/O=HAProxy Technologies/CN=HAProxy Technologies CA
Issuer: /C=FR/ST=Some-State/O=HAProxy Technologies/CN=HAProxy Technologies CA

$ echo "show ssl ca-file *cafile.crt:2" | socat /var/run/haproxy.master -
Filename: */home/tricot/work/haproxy/reg-tests/ssl/set_cafile_ca2.crt
Status: Unused

Certificate #2:
Serial: 587A1CE5ED855040A0C82BF255FF300ADB7C8136
[...]
```

<a id="entry-9-3-show-ssl-cert"></a>

**`show ssl cert [[*][\]<filename>]`**

```haproxy
show ssl cert [[*][\]<filename>]
```

Display the list of certificates loaded into the process. They are not used by any frontend or
backend until their status is "Used". If a filename is prefixed by an asterisk, it is a transaction
which is not committed yet. If a filename is specified, it will show details about the certificate.
This command can be useful to check if a certificate was well updated. You can also display details
on a transaction by prefixing the filename by a '*'. If the first character of the filename is a
'*', it can be escaped with '&#92;\*'. This command can also be used to
display the details of a certificate's OCSP response by suffixing the filename with a ".ocsp"
extension. It works for committed certificates as well as for ongoing transactions. On a committed
certificate, this command is equivalent to calling "show ssl ocsp-response" with the certificate's
corresponding OCSP response ID.

Example:

```shell
$ echo "@1 show ssl cert" | socat /var/run/haproxy.master -
# transaction
*test.local.pem
# filename
test.local.pem

$ echo "@1 show ssl cert test.local.pem" | socat /var/run/haproxy.master -
Filename: test.local.pem
Status: Used
Serial: 03ECC19BA54B25E85ABA46EE561B9A10D26F
notBefore: Sep 13 21:20:24 2019 GMT
notAfter: Dec 12 21:20:24 2019 GMT
Issuer: /C=US/O=Let's Encrypt/CN=Let's Encrypt Authority X3
Subject: /CN=test.local
Subject Alternative Name: DNS:test.local, DNS:imap.test.local
Algorithm: RSA2048
SHA1 FingerPrint: 417A11CAE25F607B24F638B4A8AEE51D1E211477

$ echo "@1 show ssl cert *test.local.pem" | socat /var/run/haproxy.master -
Filename: *test.local.pem
Status: Unused
[...]

$ echo "@1 show ssl cert \*.local.pem" | socat /var/run/haproxy.master -
Filename: *.local.pem
Status: Used
[...]
```

<a id="entry-9-3-show-ssl-crl-file"></a>

**`show ssl crl-file [[*][\]<crlfile>[:<index>]]`**

```haproxy
show ssl crl-file [[*][\]<crlfile>[:<index>]]
```

Display the list of CRL files loaded into the process. They are not used by any frontend or backend
until their status is "Used". If a filename is prefixed by an asterisk, it is a transaction which is
not committed yet. If a `<crlfile>` is specified without `<index>`, it will show the status of the
CRL file ("Used"/"Unused") followed by details about all the Revocation Lists contained in the CRL
file. The details displayed for every list are based on the output of "openssl crl -text -noout -in
`<file>`". If a `<crlfile>` is specified followed by an `<index>`, it will only display the details
of the list having the specified index. Indexes start from 1. If the index is invalid (too big for
instance), nothing will be displayed. This command can be useful to check if a CRL file was properly
updated. You can also display the details of an ongoing transaction by prefixing the filename by a
'*'. If the first character of the filename is a '*', it can be escaped with
'&#92;\*'.

Example:

```shell
$ echo "show ssl crl-file" | socat /var/run/haproxy.master -
# transaction
*crlfile.pem
# filename
crlfile.pem

$ echo "show ssl crl-file crlfile.pem" | socat /var/run/haproxy.master -
Filename: /home/tricot/work/haproxy/reg-tests/ssl/crlfile.pem
Status: Used

Certificate Revocation List #1:
Version 1
Signature Algorithm: sha256WithRSAEncryption
Issuer: /C=FR/O=HAProxy Technologies/CN=Intermediate CA2
Last Update: Apr 23 14:45:39 2021 GMT
Next Update: Sep  8 14:45:39 2048 GMT
Revoked Certificates:
    Serial Number: 1008
        Revocation Date: Apr 23 14:45:36 2021 GMT

Certificate Revocation List #2:
Version 1
Signature Algorithm: sha256WithRSAEncryption
Issuer: /C=FR/O=HAProxy Technologies/CN=Root CA
Last Update: Apr 23 14:30:44 2021 GMT
Next Update: Sep  8 14:30:44 2048 GMT
No Revoked Certificates.
```

<a id="entry-9-3-show-ssl-crt-list"></a>

**`show ssl crt-list [-n] [<filename>]`**

```haproxy
show ssl crt-list [-n] [<filename>]
```

Display the list of crt-list and directories used in the HAProxy configuration. If a filename is
specified, dump the content of a crt-list or a directory. Once dumped the output can be used as a
crt-list file. The '-n' option can be used to display the line number, which is useful when combined
with the 'del ssl crt-list' option when a entry is duplicated. The output with the '-n' option is
not compatible with the crt-list format and not loadable by haproxy.

Example:

```shell
echo "show ssl crt-list -n localhost.crt-list" | socat /tmp/sock1 -
# localhost.crt-list
common.pem:1 !not.test1.com *.test1.com !localhost
common.pem:2
ecdsa.pem:3 [verify none allow-0rtt ssl-min-ver TLSv1.0 ssl-max-ver TLSv1.3] localhost !www.test1.com
ecdsa.pem:4 [verify none allow-0rtt ssl-min-ver TLSv1.0 ssl-max-ver TLSv1.3]
```

<a id="entry-9-3-show-ssl-ech"></a>

**`show ssl ech [<name>]`**

```haproxy
show ssl ech [<name>]
```

Display the list of ECH keys loaded in the HAProxy process.

When `<name>` is specified, displays the keys for a specific bind line. The bind line format is
`<frontend>`/@`<filename>`:`<linenum>` (Example: frontend1/@haproxy.conf:19) or
`<frontend>`/`<name>` if the bind line was named with the "name" keyword.

The 'age' entry represents the time, in seconds, since the key was loaded in the bind line. This
value is reset when HAProxy is started, reloaded, or restarted.

Necessitates an OpenSSL version that supports ECH, and HAProxy must be compiled with USE_ECH=1. This
command is only supported on a CLI connection running in experimental mode (see "experimental-mode
on").

See also "ech" in the [Section 5.1](/docs/haproxy/bind-and-server-options/#section-5-1) of the configuration manual.

Example:

```shell
$ echo "experimental-mode on; show ssl ech" | socat /tmp/haproxy.sock -
 ***
 frontend: frontend1

 bind: frontend1/@haproxy.conf:19

 ECH entry: 0 public_name: example.com age: 557 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

 ECH entry: 1 public_name: example.com age: 557 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]

 bind: frontend1/@haproxy.conf:20

 ECH entry: 0 public_name: example.com age: 557 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

 ECH entry: 1 public_name: example.com age: 557 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]

$ echo "experimental-mode on; show ssl ech frontend1/@haproxy.conf:19" | socat /tmp/haproxy.sock -
***
ECH for frontend1/@haproxy.conf:19
ECH entry: 0 public_name: example.com age: 786 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

ECH entry: 1 public_name: example.com age: 786 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]
```

<a id="entry-9-3-show-ssl-jwt"></a>

**`show ssl jwt`**

```haproxy
show ssl jwt
```

Display the list of certificates that can be used for JWT validation. See also "add ssl jwt" and
"del ssl jwt" commands. See "jwt" certificate option for more information.

Example:

```shell
echo "show ssl jwt"  | socat /tmp/sock1 -
#filename
jwt.pem
```

<a id="entry-9-3-show-ssl-ocsp-response"></a>

**`show ssl ocsp-response [[text|base64] <id|path>]`**

```haproxy
show ssl ocsp-response [[text|base64] <id|path>]
```

Display the IDs of the OCSP tree entries corresponding to all the OCSP responses used in HAProxy, as
well as the corresponding frontend certificate's path, the issuer's name and key hash and the serial
number of the certificate for which the OCSP response was built. If a valid `<id>` or the `<path>`
of a valid frontend certificate is provided, display the contents of the corresponding OCSP
response. When an `<id>` is provided, it it possible to define the format in which the data is
dumped. The 'text' option is the default one and it allows to display detailed information about the
OCSP response the same way as in an "openssl ocsp -respin `<ocsp-response>` -text" call. The
'base64' format allows to dump the contents of an OCSP response in base64.

Example:

```shell
$ echo "show ssl ocsp-response" | socat /var/run/haproxy.master -
# Certificate IDs
  Certificate ID key: 303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a0202100a
  Certificate path: /path_to_cert/foo.pem
    Certificate ID:
      Issuer Name Hash: 8A83E0060FAFF709CA7E9B95522A2E81635FDA0A
      Issuer Key Hash: F652B0E435D5EA923851508F0ADBE92D85DE007A
      Serial Number: 100A

$ echo "show ssl ocsp-response 303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a0202100a" | socat /var/run/haproxy.master -
OCSP Response Data:
  OCSP Response Status: successful (0x0)
  Response Type: Basic OCSP Response
  Version: 1 (0x0)
  Responder Id: C = FR, O = HAProxy Technologies, CN = ocsp.haproxy.com
  Produced At: May 27 15:43:38 2021 GMT
  Responses:
  Certificate ID:
    Hash Algorithm: sha1
    Issuer Name Hash: 8A83E0060FAFF709CA7E9B95522A2E81635FDA0A
    Issuer Key Hash: F652B0E435D5EA923851508F0ADBE92D85DE007A
    Serial Number: 100A
  Cert Status: good
  This Update: May 27 15:43:38 2021 GMT
  Next Update: Oct 12 15:43:38 2048 GMT
  [...]

$ echo "show ssl ocsp-response base64 /path_to_cert/foo.pem" | socat /var/run/haproxy.sock -
  MIIB8woBAKCCAewwggHoBgkrBgEFBQcwAQEEggHZMIIB1TCBvqE[...]
```

<a id="entry-9-3-show-ssl-ocsp-updates"></a>

**`show ssl ocsp-updates`**

```haproxy
show ssl ocsp-updates
```

Display information about the entries concerned by the OCSP update mechanism. The command will
output one line per OCSP response and will contain the expected update time of the response as well
as the time of the last successful update and counters of successful and failed updates. It will
also give the status of the last update (successful or not) in numerical form as well as text form.
See below for a full list of possible errors. The lines will be sorted by ascending 'Next Update'
time. The lines will also contain a path to the first frontend certificate that uses the OCSP
response. See "show ssl ocsp-response" command and "ocsp-update" option for more information on the
OCSP auto update.

The update error codes and error strings can be the following:

```text
  +----+-------------------------------------+
  | ID | message                             |
  +----+-------------------------------------+
  |  0 | "Unknown"                           |
  |  1 | "Update successful"                 |
  |  2 | "HTTP error"                        |
  |  3 | "Missing \"ocsp-response\" header"  |
  |  4 | "OCSP response check failure"       |
  |  5 | "Error during insertion"            |
  +----+-------------------------------------+
```

Example:

```shell
$ echo "show ssl ocsp-updates" | socat /tmp/haproxy.sock -
  OCSP Certid | Path | Next Update | Last Update | Successes | Failures | Last Update Status | Last Update Status (str)
      303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a02021015 | /path_to_cert/cert.pem | 30/Jan/2023:00:08:09 +0000 | - | 0 | 1 | 2 | HTTP error
      304b300906052b0e03021a0500041448dac9a0fb2bd32d4ff0de68d2f567b735f9b3c40414142eb317b75856cbae500940e61faf9d8b14c2c6021203e16a7aa01542f291237b454a627fdea9c1 | /path_to_cert/other_cert.pem | 30/Jan/2023:01:07:09 +0000 | 30/Jan/2023:00:07:09 +0000 | 1 | 0 | 1 | Update successful
```

<a id="entry-9-3-show-ssl-providers"></a>

**`show ssl providers`**

```haproxy
show ssl providers
```

Display the names of the providers loaded by OpenSSL during init. Provider loading can indeed be
configured via the OpenSSL configuration file and this option allows to check that the right
providers were loaded. This command is only available with OpenSSL v3.

Example:

```shell
$ echo "show ssl providers" | socat /var/run/haproxy.master -
Loaded providers:
    - fips
    - base
```

<a id="entry-9-3-show-ssl-sni"></a>

**`show ssl sni [-f <frontend>] [-A] [-t <offset>]`**

```haproxy
show ssl sni [-f <frontend>] [-A] [-t <offset>]
```

Dump every SNI configured for the designated frontend, or all frontends if no frontend was
specified. It allows to see what SNI are offered for a frontend, and to identify if a SNI is defined
multiple times by multiple certificates for the same frontend.

The -A option allows to filter the list and only displays the certificates that are past the
notAfter date, allowing to show only expired certificates.

The -t option takes an offset in seconds, or with a time unit (s, m, h, d), which is added to the
current time, allowing to check which certificates expired after the offset when combined with -A.
For example if you want to check which certificates would be expired in 30d, just do "show ssl sni
-A -t 30d".

Columns are separated by a single &#92;t, allowing to parse it simply.

The 'Frontend/Bind' column shows the frontend name followed by the bind line position in the
configuration (frontend/file:linenum).

The 'SNI' column shows the SNI, it can be either a CN, a SAN or a filter from a crt-list. The
default certificates of a bind line, (which are either declared explicitly by 'default-crt' or is
implicitly the first certificate of a bind line when no 'strict-sni' is used) shows the '\*'
character in the SNI column.

The 'Negative Filter' column is the list of negative filters associated to a wildcard, this will
show all negatives filters that are on the same crt-list line. A dash character is displayed if
there are none.

The 'Type' column shows the encryption algorithm type, it can be "rsa", "ecdsa" or "dsa".

The 'Filename' column can be either a filename from the configuration, or an alias declared in a
crt-store.

The 'NotAfter' and 'NotBefore' columns are directly extracted from the X509 leaf certificate.

Example:

```shell
$ echo "@1 show ssl sni -A -t 30d" | socat /var/run/haproxy-master.sock - | column -t -s $'\t'
# Frontend/Bind        SNI        Negative Filter  Type   Filename             NotAfter                  NotBefore
li1/haproxy.cfg:10021  *.ex.lan   !m1.ex.lan       rsa    example.lan.pem      Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                ecdsa  machine10.pem.ecdsa  Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                rsa    machine10.pem.rsa    Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                ecdsa  machine10.pem.ecdsa  Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  localhost  -                rsa    localhost.pem.rsa    Jun 13 13:37:11 2024 GMT  May 14 13:37:11 2024 GMT
li1/haproxy.cfg:10021  localhost  -                ecdsa  localhost.pem.ecdsa  Jun 13 13:37:10 2024 GMT  May 14 13:37:10 2024 GMT
li1/haproxy.cfg:10021  *          -                rsa    localhost.pem.rsa    Jun 13 13:37:11 2024 GMT  May 14 13:37:11 2024 GMT
```

<a id="entry-9-3-show-startup-logs"></a>

**`show startup-logs`**

```haproxy
show startup-logs
```

Dump all messages emitted during the startup of the current haproxy process, each startup-logs
buffer is unique to its haproxy worker.

This keyword also exists on the master CLI, which shows the latest startup or reload tentative.

<a id="entry-9-3-show-table"></a>

**`show table`**

```haproxy
show table
```

Dump general information on all known stick-tables. Their name is returned (the name of the proxy
which holds them), their type (currently zero, always IP), their size in maximum possible number of
entries, and the number of entries currently in use.

Example:

```shell
    $ echo "show table" | socat stdio /tmp/sock1
>>> # table: front_pub, type: ip, size:204800, used:171454
>>> # table: back_rdp, type: ip, size:204800, used:0
```

<a id="entry-9-3-show-table-2"></a>

**`show table <name> [ data.<type> <operator> <value> [data.<type> ...]] |`**

```haproxy
show table <name> [ data.<type> <operator> <value> [data.<type> ...]] |
                  [ key <key> ] | [ ptr <ptr> ]
```

Dump contents of stick-table `<name>`. In this mode, a first line of generic information about the
table is reported as with "show table", then all entries are dumped. Since this can be quite heavy,
it is possible to specify a filter in order to specify what entries to display.

When the "data." form is used the filter applies to the stored data (see "stick-table" in section
4.2). A stored data type must be specified in `<type>`, and this data type must be stored in the
table otherwise an error is reported. The data is compared according to `<operator>` with the 64-bit
integer `<value>`. Operators are the same as with the ACLs:

    - eq: match entries whose data is equal to this value
    - ne: match entries whose data is not equal to this value
    - le: match entries whose data is less than or equal to this value
    - ge: match entries whose data is greater than or equal to this value
    - lt: match entries whose data is less than this value
    - gt: match entries whose data is greater than this value

In this form, you can use multiple data filter entries, up to a maximum defined during build time (4
by default).

When the key form is used the entry `<key>` is shown. The key must be of the same type as the table,
which currently is limited to IPv4, IPv6, integer, and string.

When the ptr form is used the entry `<ptr>` is shown. `<ptr>` is written in the form 0xffff and must
correspond to the address returned by a previous "show table" command. Matching an entry using its
pointer may be relevant if the entry cannot be matched using the key due empty key or incompatible
characters on the cli.

If data.`<type>` is an array type, "[]" may be used to access a specific index in the array, like
so: data.gpt[1]

Example:

```shell
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a4c: key=127.0.0.1 use=0 exp=3594729 gpc0=0 conn_rate(30000)=1  \
      bytes_out_rate(60000)=187
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy data.gpc0 gt 0" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy data.conn_rate gt 5" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy key 127.0.0.2" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy ptr 0x80e6a80" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191
```

When the data criterion applies to a dynamic value dependent on time such as a bytes rate, the value
is dynamically computed during the evaluation of the entry in order to decide whether it has to be
dumped or not. This means that such a filter could match for some time then not match anymore
because as time goes, the average event rate drops.

It is possible to use this to extract lists of IP addresses abusing the service, in order to monitor
them or even blacklist them in a firewall. Example:

```shell
$ echo "show table http_proxy data.gpc0 gt 0" \
  | socat stdio /tmp/sock1 \
  | fgrep 'key=' | cut -d' ' -f2 | cut -d= -f2 > abusers-ip.txt
  ( or | awk '/key/{ print a[split($2,a,"=")]; }' )
```

When the stick-table is synchronized to a peers section supporting sharding, the shard number will
be displayed for each key (otherwise '0' is reported). This allows to know which peers will receive
this key. Example:

```shell
$ echo "show table http_proxy" | socat stdio /tmp/sock1 | fgrep shard=
  0x7f23b0c822a8: key=10.0.0.2 use=0 exp=296398 shard=9 gpc0=0
  0x7f23a063f948: key=10.0.0.6 use=0 exp=296075 shard=12 gpc0=0
  0x7f23b03920b8: key=10.0.0.8 use=0 exp=296766 shard=1 gpc0=0
  0x7f23a43c09e8: key=10.0.0.12 use=0 exp=295368 shard=8 gpc0=0
```

<a id="entry-9-3-show-tasks"></a>

**`show tasks`**

```haproxy
show tasks
```

Dumps the number of tasks currently in the run queue, with the number of occurrences for each
function, and their average latency when it's known (for pure tasks with task profiling enabled).
The dump is a snapshot of the instant it's done, and there may be variations depending on what tasks
are left in the queue at the moment it happens, especially in mono-thread mode as there's less
chance that I/Os can refill the queue (unless the queue is full). This command takes exclusive
access to the process and can cause minor but measurable latencies when issued on a highly loaded
process, so it must not be abused by monitoring bots.

<a id="entry-9-3-show-threads"></a>

**`show threads`**

```haproxy
show threads
```

Dumps some internal states and structures for each thread, that may be useful to help developers
understand a problem. The output tries to be readable by showing one block per thread. When haproxy
is built with USE_THREAD_DUMP=1, an advanced dump mechanism involving thread signals is used so that
each thread can dump its own state in turn. Without this option, the thread processing the command
shows all its details but the other ones are less detailed. A star ('\*') is displayed in front of
the thread handling the command. A right angle bracket ('\>') may also be displayed in front of
threads which didn't make any progress since last invocation of this command, indicating a bug in
the code which must absolutely be reported. When this happens between two threads it usually
indicates a deadlock. If a thread is alone, it's a different bug like a corrupted list. In all cases
the process needs is not fully functional anymore and needs to be restarted.

The output format is purposely not documented so that it can easily evolve as new needs are
identified, without having to maintain any form of backwards compatibility, and just like with "show
activity", the values are meaningless without the code at hand.

<a id="entry-9-3-show-tls-keys"></a>

**`show tls-keys [id|*]`**

```haproxy
show tls-keys [id|*]
```

Dump all loaded TLS ticket keys references. The TLS ticket key reference ID and the file from which
the keys have been loaded is shown. Both of those can be used to update the TLS keys using "set ssl
tls-key". If an ID is specified as parameter, it will dump the tickets, using \* it will dump every
keys from every references.

<a id="entry-9-3-show-schema-json"></a>

**`show schema json`**

```haproxy
show schema json
```

Dump the schema used for the output of "show info json" and "show stat json".

The contains no extra whitespace in order to reduce the volume of output. For human consumption
passing the output through a pretty printer may be helpful. Example:

\$ echo "show schema json" \| socat /var/run/haproxy.sock stdio \| &#92;
python -m json.tool

The schema follows "JSON Schema" (json-schema.org) and accordingly verifiers may be used to verify
the output of "show info json" and "show stat json" against the schema.

<a id="entry-9-3-show-trace"></a>

**`show trace [<source>]`**

```haproxy
show trace [<source>]
```

Show the current trace status. For each source a line is displayed with a single-character status
indicating if the trace is stopped, waiting, or running. The output sink used by the trace is
indicated (or "none" if none was set), as well as the number of dropped events in this sink,
followed by a brief description of the source. If a source name is specified, a detailed list of all
events supported by the source, and their status for each action (report, start, pause, stop),
indicated by a "+" if they are enabled, or a "-" otherwise. All these events are independent and an
event might trigger a start without being reported and conversely.

<a id="entry-9-3-show-version"></a>

**`show version`**

```haproxy
show version
```

Show the version of the current HAProxy process. This is available from master and workers CLI.
Example:

```shell
$ echo "show version" | socat /var/run/haproxy.sock stdio
2.4.9

$ echo "show version" | socat /var/run/haproxy-master.sock stdio
2.5.0
```

<a id="entry-9-3-shutdown-frontend"></a>

**`shutdown frontend <frontend>`**

```haproxy
shutdown frontend <frontend>
```

Completely delete the specified frontend. All the ports it was bound to will be released. It will
not be possible to enable the frontend anymore after this operation. This is intended to be used in
environments where stopping a proxy is not even imaginable but a misconfigured proxy must be fixed.
That way it's possible to release the port and bind it into another process to restore operations.
The frontend will not appear at all on the stats page once it is terminated.

The frontend may be specified either by its name or by its numeric ID, prefixed with a sharp ('#').

This command is restricted and can only be issued on sockets configured for level "admin".

<a id="entry-9-3-shutdown-session"></a>

**`shutdown session <id>`**

```haproxy
shutdown session <id>
```

Immediately terminate the stream matching the specified stream identifier. This identifier is the
first field at the beginning of the lines in the dumps of "show sess" (it corresponds to the stream
pointer). This can be used to terminate a long-running stream without waiting for a timeout or when
an endless transfer is ongoing. Such terminated streams are reported with a 'K' flag in the logs.

<a id="entry-9-3-shutdown-sessions-server"></a>

**`shutdown sessions server <backend>/<server>`**

```haproxy
shutdown sessions server <backend>/<server>
```

Immediately terminate all the streams attached to the specified server. This can be used to
terminate long-running streams after a server is put into maintenance mode, for instance. Such
terminated streams are reported with a 'K' flag in the logs.

Backend connections are left in idle state, unless the server is already in maintenance mode, in
which case they will be immediately scheduled for deletion.

<a id="entry-9-3-trace"></a>

**`trace`**

```haproxy
trace
```

The "trace" command alone lists the trace sources, their current status, and their brief
descriptions. It is only meant as a menu to enter next levels, see other "trace" commands below.

<a id="entry-9-3-trace-0"></a>

**`trace 0`**

```haproxy
trace 0
```

Immediately stops all traces. This is made to be used as a quick solution to terminate a debugging
session or as an emergency action to be used in case complex traces were enabled on multiple sources
and impact the service.

<a id="entry-9-3-trace-2"></a>

**`trace <source> [<args...>]`**

```haproxy
trace <source> [<args...>]
```

Configure traces for the source `<source>`. Without argument, this will list all supported
sub-commands to the given source. Multiple sub-commands can be chained. Following sub-commands are
supported:

event [ [+\|-\|!]`<name>` ] Without argument, this will list all the events supported by the
designated source. They are prefixed with a "-" if they are not enabled, or a "+" if they are
enabled. It is important to note that a single trace may be labelled with multiple events, and as
long as any of the enabled events matches one of the events labelled on the trace, the event will be
passed to the trace subsystem. For example, receiving an HTTP/2 frame of type HEADERS may trigger a
frame event and a stream event since the frame creates a new stream. If either the frame event or
the stream event are enabled for this source, the frame will be passed to the trace framework.

    With an argument, it is possible to toggle the state of each event and
    individually enable or disable them. Two special keywords are supported,
    "none", which matches no event, and is used to disable all events at once,
    and "any" which matches all events, and is used to enable all events at
    once. Other events are specific to the event source. It is possible to
    enable one event by specifying its name, optionally prefixed with '+' for
    better readability. It is possible to disable one event by specifying its
    name prefixed by a '-' or a '!'.

    One way to completely disable a trace source is to pass "event none", and
    this source will instantly be totally ignored.

follow `<other_source>` This permits the source `<source>` to also emit traces when the other source
`<other_source>` is locked on a criteria and the same criteria matches for the current source as
well. For example, if a source is locked on a session, following that source from another one will
make that other one emit traces for all events related to this session. This may be used to some
extents to track backend requests along with the associated frontend connections. The "session"
source makes this easier by providing a "new" and an "end" events that are usable for lock-on
processing. Note that the source `<source>` does not need to have its traces enabled in this case,
and its tracing state will not be affected either. It is, however, possible that some events may be
missing if they do not contain information that allow to correlate them with the tracked element.
The meta-source "all" may also be used with this command: in this case, all sources will follow
`<other_source>`.

Example:

```text
trace h1 lock session start sess_new pause sess_end follow session
```

level [`<level>`] Without argument, this will list all trace levels for this source, and the
current one will be indicated by a star ('\*') prepended in front of it. With an argument, this will
change the trace level to the specified level. Detail levels are a form of filters that are applied
before reporting the events. These filters are used to selectively include or exclude events
depending on their level of importance. For example a developer might need to know precisely where
in the code an HTTP header was considered invalid while the end user may not even care about this
header's validity at all. There are currently 5 distinct levels for a trace:

```text
user       this will report information that are suitable for use by a
           regular haproxy user who wants to observe his traffic.
           Typically some HTTP requests and responses will be reported
           without much detail. Most sources will set this as the
           default level to ease operations.

proto      in addition to what is reported at the "user" level, it also
           displays protocol-level updates. This can for example be the
           frame types or HTTP headers after decoding.

state      in addition to what is reported at the "proto" level, it
           will also display state transitions (or failed transitions)
           which happen in parsers, so this will show attempts to
           perform an operation while the "proto" level only shows
           the final operation.

data       in addition to what is reported at the "state" level, it
           will also include data transfers between the various layers.

developer  it reports everything available, which can include advanced
           information such as "breaking out of this loop" that are
           only relevant to a developer trying to understand a bug that
           only happens once in a while in field. Function names are
           only reported at this level.
```

    It is highly recommended to always use the "user" level only and switch to
    other levels only if instructed to do so by a developer. Also it is a good
    idea to first configure the events before switching to higher levels, as it
    may save from dumping many lines if no filter is applied. The meta-source
    "all" may also be used with this command: in this case, the level will be
    applied to all existing sources at once.

lock [criterion] Without argument, this will list all the criteria supported by this source for
lock-on processing, and display the current choice by a star ('\*') in front of it. Lock-on means
that the source will focus on the first matching event and only stick to the criterion which
triggered this event, and ignore all other ones until the trace stops. This allows for example to
take a trace on a single connection or on a single stream. The following criteria are supported by
some traces, though not necessarily all, since some of them might not be available to the source:

```text
backend      lock on the backend that started the trace
connection   lock on the connection that started the trace
frontend     lock on the frontend that started the trace
listener     lock on the listener that started the trace
nothing      do not lock on anything
server       lock on the server that started the trace
session      lock on the session that started the trace
thread       lock on the thread that started the trace
```

    In addition to this, each source may provide up to 4 specific criteria such
    as internal states or connection IDs. For example in HTTP/2 it is possible
    to lock on the H2 stream and ignore other streams once a strace starts.

    When a criterion is passed in argument, this one is used instead of the
    other ones and any existing tracking is immediately terminated so that it
    can restart with the new criterion. The special keyword "nothing" is
    supported by all sources to permanently disable tracking.

{ pause \| start \| stop } [ [+\|-\|!]event] Without argument, this will list the events enabled
to automatically pause, start, or stop a trace for this source. These events are specific to each
trace source. With an argument, this will either enable the event for the specified action (if
optionally prefixed by a '+') or disable it (if prefixed by a '-' or '!'). The special keyword "now"
is not an event and requests to take the action immediately. The keywords "none" and "any" are
supported just like in "trace event".

    The 3 supported actions are respectively "pause", "start" and "stop". The
    "pause" action enumerates events which will cause a running trace to stop
    and wait for a new start event to restart it. The "start" action enumerates
    the events which switch the trace into the waiting mode until one of the
    start events appears. And the "stop" action enumerates the events which
    definitely stop the trace until it is manually enabled again. In practice it
    makes sense to manually start a trace using "start now" without caring about
    events, and to stop it using "stop now". In order to capture more subtle
    event sequences, setting "start" to a normal event (like receiving an HTTP
    request) and "stop" to a very rare event like emitting a certain error, will
    ensure that the last captured events will match the desired criteria. And
    the pause event is useful to detect the end of a sequence, disable the
    lock-on and wait for another opportunity to take a capture. In this case it
    can make sense to enable lock-on to spot only one specific criterion (e.g. a
    stream), and have "start" set to anything that starts this criterion
    (e.g. all events which create a stream), "stop" set to the expected anomaly,
    and "pause" to anything that ends that criterion (e.g. any end of stream
    event). In this case the trace log will contain complete sequences of
    perfectly clean series affecting a single object, until the last sequence
    containing everything from the beginning to the anomaly.

sink [`<sink>`] Without argument, this will list all event sinks available for this source, and
the currently configured one will have a star ('\*') prepended in front of it. Sink "none" is always
available and means that all events are simply dropped, though their processing is not ignored (e.g.
lock-on does occur). Other sinks are available depending on configuration and build options, but
typically "stdout" and "stderr" will be usable in debug mode, and in-memory ring buffers should be
available as well. When a name is specified, the sink instantly changes for the specified source.
Events are not changed during a sink change. In the worst case some may be lost if an invalid sink
is used (or "none"), but operations do continue to a different destination. The meta-source "all"
may also be used with this command: in this case, the sink will be applied to all existing sources
at once.

verbosity [`<level>`] Without argument, this will list all verbosity levels for this source, and
the current one will be indicated by a star ('\*') prepended in front of it. With an argument, this
will change the verbosity level to the specified one.

    Verbosity levels indicate how far the trace decoder should go to provide
    detailed information. It depends on the trace source, since some sources
    will not even provide a specific decoder. Level "quiet" is always available
    and disables any decoding. It can be useful when trying to figure what's
    happening before trying to understand the details, since it will have a very
    low impact on performance and trace size. When no verbosity levels are
    declared by a source, level "default" is available and will cause a decoder
    to be called when specified in the traces. It is an opportunistic decoding.
    When the source declares some verbosity levels, these ones are listed with a
    description of what they correspond to. In this case the trace decoder
    provided by the source will be as accurate as possible based on the
    information available at the trace point. The first level above "quiet" is
    set by default.

<a id="entry-9-3-update-ssl-ocsp-response"></a>

**`update ssl ocsp-response <certfile>`**

```haproxy
update ssl ocsp-response <certfile>
```

Create an OCSP request for the specified `<certfile>` and send it to the OCSP responder whose URI
should be specified in the "Authority Information Access" section of the certificate. Only the first
URI is taken into account. The OCSP response that we should receive in return is then checked and
inserted in the local OCSP response tree. This command will only work for certificates that already
had a stored OCSP response, either because it was provided during init or if it was previously set
through the "set ssl cert" or "set ssl ocsp-response" commands. If the received OCSP response is
valid and was properly inserted into the local tree, its contents will be displayed on the standard
output. The format is the same as the one described in "show ssl ocsp-response".

<a id="entry-9-3-wait"></a>

**`wait { -h | <delay> } [<condition> [<args>...]]`**

```haproxy
wait { -h | <delay> } [<condition> [<args>...]]
```

In its simplest form without any condition, this simply waits for the requested delay before
continuing. This can be used to collect metrics around a specific interval.

With a condition and optional arguments, the command will wait for the specified condition to be
satisfied, to unrecoverably fail, or to remain unsatisfied for the whole `<delay>` duration. The
supported conditions are:

- be-removable `<proxy>`: this will wait for the specified proxy backend to be removable by the "del
  backend" command. Some conditions will never be accepted (e.g. backend not yet unpublished or with
  servers in it) and will cause the report of a specific error message indicating what condition is
  not met. If everything is OK before the delay, a success is returned and the operation is
  terminated.

- srv-removable `<proxy>`/`<server>`: this will wait for the specified server to be removable by the
  "del server" command, i.e. be in maintenance and no longer have any connection on it (neither
  active or idle). Some conditions will never be accepted (e.g. not in maintenance) and will cause
  the report of a specific error message indicating what condition is not met. The server might even
  have been removed in parallel and no longer exit. If everything is OK before the delay, a success
  is returned and the operation is terminated.

The default unit for the delay is milliseconds, though other units are accepted if suffixed with the
usual timer units (us, ms, s, m, h, d). When used with the 'socat' utility, do not forget to extend
socat's close timeout to cover the wait time. Passing "-h" as the first or second argument provides
the command's usage. Example:

```shell
$ socat -t20 /path/to/socket - <<< "show activity; wait 10s; show activity"

$ socat -t5 /path/to/socket - <<< "
    disable server px/srv1
    shutdown sessions server px/srv1
    wait 2s srv-removable px/srv1
    del server px/srv1"
```

## 9.4. Master CLI {#section-9-4}

The master CLI is a socket bound to the master process in master-worker mode. This CLI gives access
to the unix socket commands in every running or leaving processes and allows a basic supervision of
those processes.

The master CLI is configurable only from the haproxy program arguments with the -S option. This
option also takes bind options separated by commas.

Example:

```haproxy
# haproxy -W -S 127.0.0.1:1234 -f test1.cfg
# haproxy -Ws -S /tmp/master-socket,uid,1000,gid,1000,mode,600 -f test1.cfg
# haproxy -W -S /tmp/master-socket,level,user -f test1.cfg
```

### 9.4.1. Master CLI commands {#section-9-4-1}

<a id="entry-9-4-1-entry"></a>

**`@<[!]pid>`**

```haproxy
@<[!]pid>
```

The master CLI uses a special prefix notation to access the multiple processes. This notation is
easily identifiable as it begins by a @.

A @ prefix can be followed by a relative process number or by an exclamation point and a PID. (e.g.
@1 or @!1271). A @ alone could be use to specify the master. Leaving processes are only accessible
with the PID as relative process number are only usable with the current processes.

This prefix may be used as a wrapper before a command, indicating that this command and only this
one will be sent to the designated process. In this case the full command ends at the end of line or
semi-colon like any regular command.

Bugs: the sockpair@ protocol used to implement communication between the master and the worker is
known to not be reliable on macOS because of an issue in the macOS sendmsg(2) implementation. A
command might end up without response because of that.

Examples:

```shell
$ socat /var/run/haproxy-master.sock readline
prompt
master> @1 show info; @2 show info
[...]
Process_num: 1
Pid: 1271
[...]
Process_num: 2
Pid: 1272
[...]
master>

$ echo '@!1271 show info; @!1272 show info' | socat /var/run/haproxy-master.sock -
[...]
```

The prefix may also be use as a standalone command to switch the default execution context to the
designated process, indicating that all subsequent commands will all be executed in that process,
until a new '@' command changes the execution context again.

Examples:

```shell
$ socat /var/run/haproxy-master.sock readline
prompt
master> @1
1271> show info
[...]
1271> show stat
[...]
1271> @
master>

$ echo '@1; show info; show stat; @2; show info; show stat' | socat /var/run/haproxy-master.sock -
[...]
```

Note about limitations: a few rare commands alter a CLI session's state (e.g. "set anon", "set
timeout") and may not behave exactly similarly once run from the master CLI due to commands being
sent one at a time on their own CLI session. Similarly, a few rare commands ("show events", "wait")
actively monitor the CLI for input or closure and are immediately interrupted when the CLI is
closed. These commands will not work as expected through the master CLI because the command's input
is closed after each command. For such rare casesn the "@@" variant below might be more suited.

<a id="entry-9-4-1-entry-2"></a>

**`@@<[!]pid> [command...]`**

```haproxy
@@<[!]pid> [command...]
```

This prefix or command is very similar to the "@" prefix documented above except that it enters the
worker process, delivers the whole command line into it as-is and stays there until the command
finishes. Semi-colons are delivered as well, allowing to execute a full pipelined command in a
worker process. The connection with the work remains open until the list of commands completes. Any
data sent after the commands will be forwarded to the worker process' CLI and may be consumed by the
commands being executed and will be lost for the master process' CLI, offering a truly bidirectional
connection with the worker process. As such, users of such commands must be very careful to wait for
the command's completion before sending new commands to the master CLI.

Instead of executing a single command, it is also possible to open a fully interactive session on
the worker process by not specifying any command (i.e. "@@1" on its own line). This session can be
terminated either by closing the connection or by quitting the worker process (using the "quit"
command). In this case, the prompt mode of the master socket (interactive, prompt, timed) is
propagated into the worker process.

Bugs: the sockpair@ protocol used to implement communication between the master and the worker is
known to not be reliable on macOS because of an issue in the macOS sendmsg(2) implementation. A
command might end up without response because of that.

Examples:

```shell
# gracefully close connections and delete a server once idle (wait max 10s)
$ socat -t 11 /var/run/haproxy-master.sock - <<< \
   "@@1 disable server app2/srv36; \
   wait 10000 srv-removable app2/srv36; \
   del server app2/srv36"

# forcefully close connections and quickly delete a server
$ socat /var/run/haproxy-master.sock - <<< \
   "@@1 disable server app2/srv36; \
   shutdown sessions server app2/srv36; \
   wait 100 srv-removable app2/srv36; \
   del server app2/srv36"

# show messages arriving to this ring in real time ("tail -f" equivalent)
$ (echo "show events buf0 -w"; read) | socat /var/run/haproxy-master.sock -
```

<a id="entry-9-4-1-expert-mode"></a>

**`expert-mode [on|off]`**

```haproxy
expert-mode [on|off]
```

This command activates the "expert-mode" for every worker accessed from the master CLI. Combined
with "mcli-debug-mode" it also activates the command on the master. Display the flag "e" in the
master CLI prompt.

See also "expert-mode" in [Section 9.3](/docs/haproxy/statistics-and-monitoring/#section-9-3) and "mcli-debug-mode" in 9.4.1.

<a id="entry-9-4-1-experimental-mode"></a>

**`experimental-mode [on|off]`**

```haproxy
experimental-mode [on|off]
```

This command activates the "experimental-mode" for every worker accessed from the master CLI.
Combined with "mcli-debug-mode" it also activates the command on the master. Display the flag "x" in
the master CLI prompt.

See also "experimental-mode" in [Section 9.3](/docs/haproxy/statistics-and-monitoring/#section-9-3) and "mcli-debug-mode" in 9.4.1.

<a id="entry-9-4-1-hard-reload"></a>

**`hard-reload`**

```haproxy
hard-reload
```

This command does the same as the "reload" command over the master CLI with the exception that it
does a hard-stop (-st) instead of a stop-stop (-sf) of the previous process. This means the previous
process does not wait to achieve anything before exiting, so all connections will be closed.

See also the "reload" command.

<a id="entry-9-4-1-mcli-debug-mode"></a>

**`mcli-debug-mode [on|off]`**

```haproxy
mcli-debug-mode [on|off]
```

This keyword allows a special mode in the master CLI which enables every keywords that were meant
for a worker CLI on the master CLI, allowing to debug the master process. Once activated, you list
the new available keywords with "help". Combined with "experimental-mode" or "expert-mode" it
enables even more keywords. Display the flag "d" in the master CLI prompt.

<a id="entry-9-4-1-prompt"></a>

**`prompt`**

```haproxy
prompt
```

When the prompt is enabled (via the "prompt" command), the context the CLI is working on is
displayed in the prompt. The master is identified by the "master" string, and other processes are
identified with their PID. In case the last reload failed, the master prompt will be changed to
"master[ReloadFailed]\>" so that it becomes visible that the process is still running on the
previous configuration and that the new configuration is not operational.

The prompt of the master CLI is able to display several flags which are the enable modes. "d" for
mcli-debug-mode, "e" for expert-mode, "x" for experimental-mode.

Example:

```shell
$ socat /var/run/haproxy-master.sock -
prompt
master> expert-mode on
master(e)> experimental-mode on
master(xe)> mcli-debug-mode on
master(xed)> @1
95191(xed)>
```

<a id="entry-9-4-1-reload"></a>

**`reload`**

```haproxy
reload
```

You can also reload the HAProxy master process with the "reload" command which does the same as a
`kill -USR2` on the master process, provided that the user has at least "operator" or "admin"
privileges.

This command allows you to perform a synchronous reload, the command will return a reload status,
once the reload was performed. Be careful with the timeout if a tool is used to parse it, it is only
returned once the configuration is parsed and the new worker is forked. The "socat" command uses a
timeout of 0.5s by default so it will quit before showing the message if the reload is too long.
"ncat" does not have a timeout by default. When compiled with USE_SHM_OPEN=1, the reload command is
also able to dump the startup-logs of the master.

Example:

```shell
$ echo "reload" | socat -t300 /var/run/haproxy-master.sock stdin
Success=1
--
[NOTICE]   (482713): haproxy version is 2.7-dev7-4827fb-69
[NOTICE]   (482713): path to executable is ./haproxy
[WARNING]  (482713): config: 'http-request' rules ignored for proxy 'frt1' as they require HTTP mode.
[NOTICE]   (482713): New worker (482720) forked
[NOTICE]   (482713): Loading success.

$ echo "reload" | socat -t300 /var/run/haproxy-master.sock stdin
Success=0
--
[NOTICE]   (482886): haproxy version is 2.7-dev7-4827fb-69
[NOTICE]   (482886): path to executable is ./haproxy
[ALERT]    (482886): config: parsing [test3.cfg:1]: unknown keyword 'Aglobal' out of section.
[ALERT]    (482886): config: Fatal errors found in configuration.
[WARNING]  (482886): Loading failure!

$
```

The reload command is the last executed on the master CLI, every other command after it are ignored.
Once the reload command returns its status, it will close the connection to the CLI.

Note that a reload will close all connections to the master CLI. See also the "hard-reload" command.

<a id="entry-9-4-1-show-proc"></a>

**`show proc [debug]`**

```haproxy
show proc [debug]
```

The master CLI introduces a 'show proc' command to surpervise the processe.

Example:

```shell
$ echo 'show proc' | socat /var/run/haproxy-master.sock -
#<PID>          <type>          <reloads>       <uptime>        <version>
1162            master          5 [failed: 0]   0d00h02m07s     2.5-dev13
# workers
1271            worker          1               0d00h00m00s     2.5-dev13
# old workers
1233            worker          3               0d00h00m43s     2.0-dev3-6019f6-289
```

In this example, the master has been reloaded 5 times but one of the old worker is still running and
survived 3 reloads. You could access the CLI of this worker to understand what's going on.

The 'debug' parameter is useful to show debug details, it currently shows the FDs for IPC
communication. Note that the debug output is not guaranteed to be stable between haproxy versions.

<a id="entry-9-4-1-show-startup-logs"></a>

**`show startup-logs`**

```haproxy
show startup-logs
```

HAProxy needs to be compiled with USE_SHM_OPEN=1 to be used correctly on the master CLI or all
messages won't be visible.

Like its counterpart on the stats socket, this command is able to show the startup messages of
HAProxy. However it does not dump the startup messages of the current worker, but the startup
messages of the latest startup or reload, which means it is able to dump the parsing messages of a
failed reload.

Those messages are also dumped with the "reload" command.

## 9.5. Stats-file {#section-9-5}

A so-called stats-file can be used to preload internal haproxy counters on process startup with
non-null values. Its main purpose is to preserve statistics for worker processes across reloads.
Only an excerpt of all the exposed haproxy statistics is present in a stats-file as it only makes
sense to preload metric-type values.

For the moment, only proxy counters are supported in stats-file. This allows to preload values for
frontends, backends, servers and listeners. However only objects instances with a non-empty GUID are
stored in a stats-file. This guarantees that value will be preloaded for object with matching type
and GUID, even if other parameters differ.

The CLI command "dump stats-file" purpose is to generate a stats-file. Format of the stats-file is
internally defined and freely subject to future changes and extension. It is designed to be
compatible at least across adjacent haproxy stable branch releases, but may require optional extra
configuration when loading a stats-file to a process running on an older version.
