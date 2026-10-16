---
title: كيفية مراقبة المفاتيح
description: دليل لمراقبة مفاتيح etcd
weight: 600
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-watch-keys.md"
---

## المتطلبات الأساسية {#prerequisites}

* تثبيت [`etcd` و`etcdctl`](/ar/etcd/install/)

## مراقبة المفاتيح {#watching-keys}
`watch` للحصول على إشعارات بالتغييرات المستقبلية:

```bash
etcdctl watch $KEY [$END_KEY]
```

### الخيارات {#options}

```bash
-i, --interactive[=false]: interactive mode
--prefix[=false]: watch on a prefix if prefix is set
--rev=0: Revision to start watching
--prev-kv[=false]: get the previous key-value pair before the event happens
--progress-notify[=false]: get periodic watch progress notification from server
```

### الخيارات الموروثة من الأوامر الأصلية {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### الأمثلة {#examples}
![06_etcdctl_watch_2016050501](/etcd/tasks/img/watch-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS watch stock1
etcdctl --endpoints=$ENDPOINTS put stock1 1000

etcdctl --endpoints=$ENDPOINTS watch stock --prefix
etcdctl --endpoints=$ENDPOINTS put stock1 10
etcdctl --endpoints=$ENDPOINTS put stock2 20
```
