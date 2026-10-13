---
title: System limits
weight: 3625
description: "etcd limits: requests and storage"
categories: [Reference]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/limit.md"
aliases: [/etcd/dev-guide/limit/]
---

## Request size limit

etcd is designed to handle small key value pairs typical for metadata. Larger requests will work, but may increase the latency of other requests. By default, the maximum size of any request is 1.5 MiB. This limit is configurable through `--max-request-bytes` flag for etcd server.

## Storage size limit

The default storage size limit is 2 GiB, configurable with `--quota-backend-bytes` flag. 8 GiB is a suggested maximum size for normal environments and etcd warns at startup if the configured value exceeds it.
