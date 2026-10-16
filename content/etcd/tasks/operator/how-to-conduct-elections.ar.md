---
title: كيفية إجراء انتخاب القائد في عنقود etcd
description: خطوات إجراء انتخاب القائد عبر عميل etcdctl
weight: 900
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-conduct-elections.md"
---

## المتطلبات الأساسية {#prerequisites}

- تأكد من تثبيت [`etcd`](/ar/etcd/install/) و [`etcdctl`](/ar/etcd/install/).
- تحقق من وجود عنقود etcd نشط.

## إجراء انتخاب القائد {#conduct-leader-election}

يُستخدَم الأمر `etcdctl` لإجراء انتخابات القائد في عنقود etcd. وهو يضمن ألا يصبح سوى عميل واحد قائدًا في الوقت نفسه.

`etcdctl --endpoints=$ENDPOINTS elect <election-name> [proposal]`

```shell
etcdctl --endpoints=$ENDPOINTS elect election-name p1
```

### الخيارات {#options}

- `--endpoints : $ENDPOINTS`

عنوان كل عضو من أعضاء عنقود etcd.

- `election-name` سلسلة نصية

معرّف نصي للانتخاب. يجب على جميع المشاركين المتنافسين على القيادة استخدام اسم الانتخاب نفسه.

- `leader-name` سلسلة نصية

قيمة المقترح للقائد الجديد.

### مثال {#example}

```shell
./etcdctl elect my-election proposal1
my-election/694d99fafea88404
proposal1

another election:
./etcdctl elect new-election proposal1
new-election/694d99fafea8840f
proposal1
```
