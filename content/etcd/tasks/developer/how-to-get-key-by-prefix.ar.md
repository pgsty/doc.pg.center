---
title: كيفية الحصول على المفاتيح بالبادئة
description: دليل لاستخراج مفاتيح etcd بحسب بادئتها
weight: 300
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-get-key-by-prefix.md"
---

## المتطلبات الأساسية {#pre-requisites}

* [تثبيت etcdctl](/ar/etcd/install/)
* [إعداد عنقود محلي](/ar/etcd/dev-guide/local_cluster/)

## الحصول على المفاتيح بالبادئة {#get-keys-by-prefix}

```bash
$ etcdctl --endpoints=$ENDPOINTS get PREFIX --prefix
```

### الخيارات العامة {#global-options}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

### الخيارات {#options}

```bash
--prefix, get a range of keys with matching prefix
```

### مثال {#example}

![03_etcdctl_get_by_prefix_2016050501](/etcd/tasks/img/get-by-prefix.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put web1 value1
etcdctl --endpoints=$ENDPOINTS put web2 value2
etcdctl --endpoints=$ENDPOINTS put web3 value3

etcdctl --endpoints=$ENDPOINTS get web --prefix
```
