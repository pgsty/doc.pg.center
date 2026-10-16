---
title: كيفية إنشاء الأقفال
description: دليل لإنشاء أقفال موزعة في etcd
weight: 800
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-create-locks.md"
---

يكتسب LOCK كائن مزامنة (mutex) موزعًا بالاسم المحدد. وبمجرد اكتساب القفل، يظل محتفظًا به حتى يتم إنهاء etcdctl.

## المتطلبات الأساسية {#prerequisites}

* تثبيت [`etcd` و`etcdctl`](/ar/etcd/install/)

## إنشاء قفل {#creating-a-lock}

`lock` لإنشاء قفل موزع:

![08_etcdctl_lock_2016050501](/etcd/tasks/img/create-lock.gif)

```shell
etcdctl --endpoints=$ENDPOINTS lock mutex1
```

### الخيارات {#options}
- endpoints - يحدد قائمة عناوين الأجهزة في العنقود مفصولة بفواصل.
- ttl - المهلة بالثواني لجلسة القفل.
