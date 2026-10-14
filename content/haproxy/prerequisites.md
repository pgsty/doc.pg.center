---
title: "1. Prerequisites"
linkTitle: "1. Prerequisites"
weight: 250
description: "Expected UNIX administration and troubleshooting knowledge"
icon: fa-solid fa-list-check
module: [HAPROXY]
categories: [Task]
aliases:
  - /haproxy/management/prerequisites/
  - /haproxy/management/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 1"
---

This document describes how to start, stop, manage, and troubleshoot HAProxy, as well as some known
limitations and traps to avoid. It does not describe how to configure it (for this please read
[`configuration.txt`](/haproxy/http-fundamentals/)).

In this document it is assumed that the reader has sufficient administration skills on a UNIX-like
operating system, uses the shell on a daily basis and is familiar with troubleshooting utilities
such as strace and tcpdump.
