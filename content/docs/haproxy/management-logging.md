---
title: "8. Logging"
linkTitle: "8. Logging"
weight: 320
description: "Syslog integration, startup logs, runtime logs, and log troubleshooting"
icon: fa-solid fa-file-lines
module: [HAPROXY]
categories: [Task]
aliases:
  - /haproxy/management/logging/
  - /docs/haproxy/management/logging/
  - /haproxy/management-logging/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 8"
---

For logging, HAProxy always relies on a syslog server since it does not perform any file-system
access. The standard way of using it is to send logs over UDP to the log server (by default on port
514). Very commonly this is configured to 127.0.0.1 where the local syslog daemon is running, but
it's also used over the network to log to a central server. The central server provides additional
benefits especially in active-active scenarios where it is desirable to keep the logs merged in
arrival order. HAProxy may also make use of a UNIX socket to send its logs to the local syslog
daemon, but it is not recommended at all, because if the syslog server is restarted while haproxy
runs, the socket will be replaced and new logs will be lost. Since HAProxy will be isolated inside a
chroot jail, it will not have the ability to reconnect to the new socket. It has also been observed
in field that the log buffers in use on UNIX sockets are very small and lead to lost messages even
at very light loads. But this can be fine for testing however.

It is recommended to add the following directive to the "global" section to make HAProxy log to the
local daemon using facility "local0":

```text
log 127.0.0.1:514 local0
```

and then to add the following one to each "defaults" section or to each frontend and backend
section:

```text
log global
```

This way, all logs will be centralized through the global definition of where the log server is.

Some syslog daemons do not listen to UDP traffic by default, so depending on the daemon being used,
the syntax to enable this will vary:

- on sysklogd, you need to pass argument "-r" on the daemon's command line so that it listens to a
  UDP socket for "remote" logs; note that there is no way to limit it to address 127.0.0.1 so it
  will also receive logs from remote systems;

- on rsyslogd, the following lines must be added to the configuration file:

```shell
$ModLoad imudp
$UDPServerAddress *
$UDPServerRun 514
```

- on syslog-ng, a new source can be created the following way, it then needs to be added as a valid
  source in one of the "log" directives:

```text
source s_udp {
  udp(ip(127.0.0.1) port(514));
};
```

Please consult your syslog daemon's manual for more information. If no logs are seen in the system's
log files, please consider the following tests:

- restart haproxy. Each frontend and backend logs one line indicating it's starting. If these logs
  are received, it means logs are working.

- run "strace -tt -s100 -etrace=sendmsg -p \<haproxy's pid\>" and perform some activity that you
  expect to be logged. You should see the log messages being sent using sendmsg() there. If they
  don't appear, restart using strace on top of haproxy. If you still see no logs, it definitely
  means that something is wrong in your configuration.

- run tcpdump to watch for port 514, for example on the loopback interface if the traffic is being
  sent locally: "tcpdump -As0 -ni lo port 514". If the packets are seen there, it's the proof
  they're sent then the syslogd daemon needs to be troubleshooted.

While traffic logs are sent from the frontends (where the incoming connections are accepted),
backends also need to be able to send logs in order to report a server state change consecutive to a
health check. Please consult HAProxy's configuration manual for more information regarding all
possible log settings.

It is convenient to chose a facility that is not used by other daemons. HAProxy examples often
suggest "local0" for traffic logs and "local1" for admin logs because they're never seen in field. A
single facility would be enough as well. Having separate logs is convenient for log analysis, but
it's also important to remember that logs may sometimes convey confidential information, and as such
they must not be mixed with other logs that may accidentally be handed out to unauthorized people.

For in-field troubleshooting without impacting the server's capacity too much, it is recommended to
make use of the "halog" utility provided with HAProxy. This is sort of a grep-like utility designed
to process HAProxy log files at a very fast data rate. Typical figures range between 1 and 2 GB of
logs per second. It is capable of extracting only certain logs (eg: search for some classes of HTTP
status codes, connection termination status, search by response time ranges, look for errors only),
count lines, limit the output to a number of lines, and perform some more advanced statistics such
as sorting servers by response time or error counts, sorting URLs by time or count, sorting client
addresses by access count, and so on. It is pretty convenient to quickly spot anomalies such as a
bot looping on the site, and block them.
