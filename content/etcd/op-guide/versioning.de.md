---
title: "Versionierung"
weight: 4900
description: "Versionierungsunterstützung in etcd"
categories: [Konzept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/versioning.md"
---

Dieses Dokument beschreibt die vom etcd-Projekt unterstützten Versionen.

## Dienstversionierung und unterstützte Versionen {#service-versioning-and-supported-versions}

etcd-Versionen werden als **x.y.z** angegeben. Dabei ist **x** die Hauptversion, **y** die Nebenversion und **z** die Patchversion, entsprechend der Terminologie der [semantischen Versionierung](https://semver.org/).
Neue Nebenversionen können der API zusätzliche Funktionen hinzufügen.

Das etcd-Projekt pflegt Release-Branches für die aktuelle und die vorherige Version. Ist beispielsweise v3.5 die aktuelle Version, wird v3.4 unterstützt. Mit der Veröffentlichung von v3.6 endet die Unterstützung für v3.4.

Geeignete Fehlerbehebungen, einschließlich Sicherheitskorrekturen, können abhängig von Schweregrad und Machbarkeit auf diese beiden Release-Branches zurückportiert werden.
Bei Bedarf werden daraus Patchversionen veröffentlicht.

Diese Entscheidung treffen die [Maintainer](https://github.com/etcd-io/etcd/blob/main/OWNERS) des Projekts.

Die Version eines laufenden etcd-Clusters lässt sich mit `etcdctl` prüfen:

```sh
etcdctl --endpoints=127.0.0.1:2379 endpoint status
```

## API-Versionierung {#api-versioning}

Die Antworten der `v3`-API sollten sich nach der Veröffentlichung von 3.0.0 nicht ändern; im Laufe der Zeit werden jedoch neue Funktionen hinzugefügt.
