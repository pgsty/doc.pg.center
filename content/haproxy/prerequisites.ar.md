---
title: "1. المتطلبات الأساسية"
linkTitle: "1. المتطلبات الأساسية"
weight: 250
description: "المعرفة المتوقعة بإدارة أنظمة UNIX واستكشاف الأخطاء وإصلاحها"
icon: fa-solid fa-list-check
module: [HAPROXY]
categories: [مهمة]
aliases:
  - /haproxy/management/prerequisites/
  - /haproxy/management/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 1"
---

يصف هذا المستند كيفية تشغيل HAProxy وإيقافه وإدارته واستكشاف أخطائه وإصلاحها، فضلًا عن بعض القيود المعروفة والفخاخ التي ينبغي تجنبها. وهو لا يصف كيفية تهيئته (لأجل ذلك يُرجى قراءة [`configuration.txt`](/ar/haproxy/http-fundamentals/)).

يفترض هذا المستند أن القارئ يمتلك مهارات إدارية كافية على نظام تشغيل شبيه بـ UNIX، وأنه يستخدم الصدفة (shell) بشكل يومي، وأنه معتاد على أدوات استكشاف الأخطاء وإصلاحها مثل strace و tcpdump.
