---
title: "Unterstützte Plattformen"
weight: 4800
description: "etcd-Unterstützung für gängige Architekturen und Betriebssysteme"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/supported-platform.md"
---

## Unterstützungsstufen {#support-tiers}

etcd läuft auf verschiedenen Plattformen. Die gewährten Garantien hängen jedoch von der Unterstützungsstufe der jeweiligen Plattform ab:

- **Stufe 1**: vollständig von den [etcd-Maintainern][etcd maintainers] unterstützt; etcd besteht garantiert
  alle Tests einschließlich Funktions- und Robustheitstests.
- **Stufe 2**: etcd besteht garantiert Integrations- und Ende-zu-Ende-Tests, aber
  nicht unbedingt Funktions- oder Robustheitstests.
- **Stufe 3**: etcd lässt sich garantiert bauen, wird möglicherweise nur wenig oder gar nicht getestet
  und sollte daher als _instabil_ betrachtet werden.

## Aktuelle Unterstützung {#current-support}

Die folgende Tabelle führt die derzeit unterstützten Plattformen und ihre jeweilige etcd-Unterstützungsstufe auf:

| Architektur | Betriebssystem | Unterstützungsstufe | Maintainer |
|:------------:|:----------------:|:------------:|:--------------------:|
| AMD64 | Linux | 1 | [etcd-Maintainer][etcd maintainers] |
| ARM64 | Linux | 1 | [etcd-Maintainer][etcd maintainers] |
| AMD64 | Darwin | 3 | |
| ARM64 | Darwin | 3 | |
| AMD64 | Windows | 3 | |
| ppc64le | Linux | 3 | |
| s390x | Linux | 3 | |

Nicht aufgeführte Plattformen werden nicht unterstützt.

## Eine neue Plattform unterstützen {#supporting-a-new-platform}

Möchten Sie als „offizieller“ Maintainer einer neuen Plattform zu etcd beitragen? Neben der Zusage, die Plattform zu unterstützen, müssen Sie eine kontinuierliche Integration (CI) für etcd einrichten, die abhängig von der Unterstützungsstufe die folgenden Anforderungen erfüllt:

| Kontinuierliche Integration für etcd | Stufe 1 | Stufe 2 | Stufe 3 |
|---------------------------------------|:-------:|:-------:|:-------:|
| Build erfolgreich | &check; | &check; | &check; |
| Unittests bestanden | &check; | &check; | |
| Integrations- und Ende-zu-Ende-Tests bestanden | &check; | &check; | |
| Robustheitstests bestanden | &check; | | |

Ein Beispiel zur Einrichtung einer CI der Stufe 2 für ARM64 bietet [etcd PR #12928][].

## Nicht unterstützte Plattformen {#unsupported-platforms}

Um den unbeabsichtigten Betrieb eines etcd-Servers auf einer nicht unterstützten Plattform zu vermeiden, gibt etcd eine Warnung aus und beendet sich sofort, sofern die Umgebungsvariable `ETCD_UNSUPPORTED_ARCH` nicht auf die Zielarchitektur gesetzt ist.

> [!WARNING]
> **32-Bit-Systeme**
>   Auf 32-Bit-Systemen hat etcd aufgrund eines Fehlers in der Go-Laufzeitumgebung **bekannte Probleme**.
>   Weitere Informationen bieten das [Go-Issue #599][go-issue] und der [Fehlerhinweis zum Paket
>   atomic][go-atomic].
>
>   [go-atomic]: https://golang.org/pkg/sync/atomic/#pkg-note-BUG
>   [go-issue]: https://github.com/golang/go/issues/599

[etcd maintainers]: https://github.com/etcd-io/etcd/blob/main/OWNERS
[etcd PR #12928]: https://github.com/etcd-io/etcd/pull/12928
