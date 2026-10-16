---
title: كيفية حذف المفاتيح
description: يصف طريقة لحذف مفاتيح etcd
weight: 400
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-delete-keys.md"
---

## المتطلبات الأساسية {#prerequisites}

* تثبيت [`etcd` و`etcdctl`](/ar/etcd/install/)

## إضافة المفاتيح أو حذفها {#add-or-delete-keys}

`del` لحذف المفتاح المحدد أو نطاق من المفاتيح:

```bash
etcdctl del $KEY [$END_KEY]
```

### الخيارات {#options}

```bash
--prefix[=false]: delete keys with matching prefix
--prev-kv[=false]: return deleted key-value pairs
--from-key[=false]: delete keys that are greater than or equal to the given key using byte compare
--range[=false]: delete range of keys without delay
```

### الخيارات الموروثة من الأوامر الأصلية {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### الأمثلة {#examples}

![04_etcdctl_delete_2016050601](/etcd/tasks/img/delete-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put key myvalue
etcdctl --endpoints=$ENDPOINTS del key

etcdctl --endpoints=$ENDPOINTS put k1 value1
etcdctl --endpoints=$ENDPOINTS put k2 value2
etcdctl --endpoints=$ENDPOINTS del k --prefix
```
