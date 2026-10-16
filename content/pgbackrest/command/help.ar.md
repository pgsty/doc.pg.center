---
title: "أمر المساعدة (help)"
linkTitle: "help"
weight: 70
description: "مرجع لخيارات أمر `help` في pgBackRest وسلوكه."
icon: fa-solid fa-circle-question
module: [PGBACKREST]
categories: [مرجع]
upstream_link: "https://pgbackrest.org/command.html#command-help"
---

تُقدَّم ثلاثة مستويات من المساعدة. إذا لم يُحدَّد أي أمر فستُعرض مساعدة عامة. وإذا حُدِّد أمر (مثل `pgbackrest help backup`) فسيُعرض وصف كامل للأمر مع قائمة بالخيارات الصالحة. وإذا حُدِّد خيارٌ بالإضافة إلى أمر (مثل `pgbackrest help backup type`) فسيُعرض وصف كامل للخيار كما ينطبق على ذلك الأمر.

## خيارات الأمر {#command-options}

### خيار عرض المساعدة (`--help`) {#display-help-option---help}

عرض المساعدة.

يعرض المساعدة حتى لو لم يُحدَّد أمر `help`، ويتجاوز خيار `--version`.

```yaml
default: n
example: --help
```

### خيار عرض الإصدار (`--version`) {#display-version-option---version}

عرض الإصدار.

يعرض الإصدار حتى لو لم يُحدَّد أمر `version` أو `help`.

```yaml
default: n
example: --version
```
