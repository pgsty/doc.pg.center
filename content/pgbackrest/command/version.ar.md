---
title: "أمر الإصدار (version)"
linkTitle: "version"
weight: 200
description: "مرجع لخيارات الأمر `version` وسلوكه في pgBackRest."
icon: fa-solid fa-tag
module: [PGBACKREST]
categories: [مرجع]
upstream_link: "https://pgbackrest.org/command.html#command-version"
---

يعرض إصدار pgBackRest المثبت.

## خيارات الأمر {#command-options}

### خيار المخرجات (`--output`) {#output-option---output}

نوع المخرجات.

تُدعم أنواع المخرجات التالية:

- `text` - عرض إصدار pgBackRest المثبت كنص.
- `num` - عرض إصدار pgBackRest المثبت كعدد صحيح.

```yaml
default: text
example: --output=num
```
