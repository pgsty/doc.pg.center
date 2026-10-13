---
title: etcd-Funktionen
weight: 3750
description: etcd-Funktionen verwenden
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/features.md"
aliases: [/etcd/dev-guide/features/]
---

Dieses Dokument gibt einen Überblick über die Funktionen von etcd und das Verfahren, nach dem sie als veraltet eingestuft werden. Wie Funktionen in etcd entwickelt werden, erläutern diese [Entwicklungsrichtlinien](https://github.com/etcd-io/etcd/blob/main/Documentation/contributor-guide/features.md).

Die Funktionen von etcd werden in drei Stufen eingeteilt: experimentell, stabil und unsicher. Mit `etcd --help` lässt sich die Liste der Funktionen anzeigen.

## Experimentell {#experimental}

Um frühzeitig Rückmeldungen zu erhalten, werden neue Funktionen üblicherweise als experimentelle Funktionen eingeführt. Sie sind am Optionsnamen zu erkennen, der mit `--experimental` beginnen sollte. Bei der Verwendung einer experimentellen Funktion sind folgende Punkte zu beachten:
- Sie kann Fehler enthalten, da sie noch nicht ausreichend von Benutzern getestet wurde. Nach dem Aktivieren funktioniert sie möglicherweise nicht wie erwartet.
- Sie ist standardmäßig deaktiviert.
- Die Unterstützung einer solchen Funktion kann jederzeit ohne Ankündigung eingestellt werden
    - Sie kann in der nächsten Minor- oder Major-Version entfernt werden, ohne die [Richtlinie zur Einstufung als veraltet](#feature-deprecation) einzuhalten, sofern sie nicht in die stabile Stufe übergeht.
    - Das Projektteam freut sich über Fehlermeldungen zu experimentellen Funktionen. Diese Probleme können jedoch eine geringere Priorität erhalten als Probleme mit stabilen Funktionen.
- Eine experimentelle [Funktionsoption wird als veraltet eingestuft](#feature-deprecation), sobald die Funktion die stabile Stufe erreicht. Benutzer sollten möglichst bald auf die stabile Funktionsoption umsteigen.

## Stabil {#stable}

Dies ist die häufigste Stufe von Funktionen in etcd. Eine stabile Funktion zeichnet sich durch Folgendes aus:
- Sie wird im Rahmen der unterstützten etcd-Versionen unterstützt.
- Sie kann standardmäßig aktiviert sein.
- Die Einstellung der Unterstützung muss der [Richtlinie zur Einstufung als veraltet](#feature-deprecation) folgen.

## Unsicher {#unsafe}

Unsichere Funktionen sind selten und werden im Abschnitt `Unsafe feature:` der etcd-Nutzungsdokumentation aufgeführt. Sie sind standardmäßig deaktiviert. Sie sollten mit Vorsicht und gemäß der Dokumentation verwendet werden. Eine unsichere Funktion kann in der nächsten Minor- oder Major-Version entfernt werden, ohne die Richtlinie zur Einstufung als veraltet einzuhalten.

## Funktionen als veraltet einstufen {#feature-deprecation}

### Experimentell {#experimental-1}
Eine experimentelle Funktion wird als veraltet eingestuft, sobald sie die stabile Stufe erreicht.
- Die Dokumentation der experimentellen Funktion zeigt einen Hinweis auf die Einstufung als veraltet und empfiehlt die entsprechende stabile Funktionsoption, z. B. `DEPRECATED. Use <feature-name> instead.`
- Eine als veraltet eingestufte Funktion wird in der darauffolgenden Version entfernt.

### Stabil {#stable-1}
Im Zuge der Projektentwicklung kann es nötig werden, auch eine stabile Funktion als veraltet einzustufen und zu entfernen. In diesem Fall gilt:
- Die Dokumentation der Funktion zeigt vor der Version, für die die Einstufung als veraltet geplant ist, eine Warnmeldung, z. B. `To be deprecated in <release>.`. Ist bereits eine neue Funktion als Ersatz für die mit `To be deprecated` gekennzeichnete Funktion geplant, wird auch darauf hingewiesen, z. B. `Use <feature-name> instead.`.
- Die Funktion wird in der geplanten Version als veraltet eingestuft. Ab dann zeigt ihre Dokumentation einen entsprechenden Hinweis und empfiehlt eine verwandte stabile Funktion, z. B. `DEPRECATED. Use <feature-name> instead.`
- Eine als veraltet eingestufte Funktion wird in der darauffolgenden Version entfernt.
