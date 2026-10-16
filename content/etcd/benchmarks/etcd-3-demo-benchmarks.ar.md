---
title: قياس أداء etcd v3
weight: 5375
description: قياسات أداء لـ etcd v3
categories: [مرجع]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-3-demo-benchmarks.md"
---

## الأجهزة الفعلية {#physical-machines}

نوع الجهاز GCE n1-highcpu-2

- 1x قرص SSD محلي مخصص مثبت تحت /var/lib/etcd
- 1x قرص بطيء مخصص لنظام التشغيل
- ذاكرة بسعة 1.8 GB
- معالجان (2x CPUs)
- إصدار etcd 2.2.0

## عنقود etcd {#etcd-cluster}

عضو etcd واحد يعمل في وضع العرض التجريبي v3

## الاختبار {#testing}

استخدم [أداة قياس أداء etcd v3][etcd-v3-benchmark].

## الأداء {#performance}

### قراءة مفتاح واحد {#reading-one-single-key}

| حجم المفتاح بالبايت | عدد العملاء | قراءة QPS | زمن الاستجابة للمئين 90 (ms) |
|-------------------|-------------------|----------|---------------|
| 256               | 1                 | 2716  | 0.4      |
| 256               | 64                | 16623 | 6.1      |
| 256               | 256               | 16622 | 21.7     |

الأداء هو تقريبًا نفس الأداء المحقق مع معالج خادم فارغ.

### قراءة مفتاح واحد بعد عملية put {#reading-one-single-key-after-putting}

| حجم المفتاح بالبايت | عدد العملاء | قراءة QPS | زمن الاستجابة للمئين 90 (ms) |
|-------------------|-------------------|----------|---------------|
| 256               | 1                 | 2269  | 0.5      |
| 256               | 64                | 13582 | 8.6      |
| 256               | 256               | 13262 | 47.5     |

لا يتأثر الأداء مع معالج الخادم الفارغ بعملية put واحدة. لذا ينبغي أن يكون
تدهور الأداء ناتجًا عن حزمة التخزين.

[etcd-v3-benchmark]: https://github.com/etcd-io/etcd/tree/main/tools/benchmark
