---
title: الكتابة إلى etcd
description: إضافة زوج مفتاح-قيمة إلى عنقود etcd
weight: 250
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
---

## المتطلبات الأساسية {#prerequisites}

- ثبّت `etcdctl`

## الإجراء {#procedure}

استخدم الأمر الفرعي `put` لكتابة زوج مفتاح-قيمة:

```shell
etcdctl --endpoints=$ENDPOINTS put foo "Hello World!"
```
حيث:
- `foo` هو اسم المفتاح
- `"Hello World!"` هي القيمة المحاطة بعلامات اقتباس
