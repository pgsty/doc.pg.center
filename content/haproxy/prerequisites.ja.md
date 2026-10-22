---
title: "1. 前提条件"
linkTitle: "1. 前提条件"
weight: 250
description: "UNIX管理およびトラブルシューティングに関する知識を想定しています"
icon: fa-solid fa-list-check
module: [HAPROXY]
categories: [タスク]
aliases:
  - /haproxy/management/prerequisites/
  - /haproxy/management/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 1"
---

このドキュメントでは、HAProxyの起動、停止、管理、トラブルシューティングの方法について説明します。また、既知の制限や回避すべき落とし穴についても述べています。設定方法については記載していません（詳細は [`configuration.txt`](/ja/haproxy/http-fundamentals/) を参照してください）。

このドキュメントでは、読者がUNIX系オペレーティングシステムの十分な管理能力を持ち、日常的にシェルを使い、straceやtcpdumpなどのトラブルシューティングツールに精通していることを前提としています。
