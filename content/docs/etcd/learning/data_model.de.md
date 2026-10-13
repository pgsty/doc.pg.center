---
title: Datenmodell
weight: 2125
description: Verfahren zur Datenspeicherung in etcd
categories: [Konzept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/data_model.md"
aliases: [/etcd/learning/data_model/]
---

etcd ist darauf ausgelegt, selten aktualisierte Daten zuverlässig zu speichern und zuverlässige Watch-Abfragen bereitzustellen. etcd macht frühere Versionen von Schlüssel-Wert-Paaren zugänglich, um kostengünstige Snapshots und die Beobachtung historischer Ereignisse zu ermöglichen („Zeitreiseabfragen“). Ein persistentes Datenmodell mit Mehrversions-Nebenläufigkeitskontrolle eignet sich gut für diese Anwendungsfälle.

etcd speichert Daten in einem [persistenten][persistent-ds] Schlüssel-Wert-Speicher mit mehreren Versionen. Dieser bewahrt die vorherige Version eines Schlüssel-Wert-Paars auf, wenn dessen Wert durch neue Daten ersetzt wird. Der Schlüssel-Wert-Speicher ist praktisch unveränderlich: Seine Operationen aktualisieren die Struktur nicht an Ort und Stelle, sondern erzeugen stets eine neue, aktualisierte Struktur. Alle früheren Versionen von Schlüsseln bleiben nach einer Änderung zugänglich und können beobachtet werden. Damit der Datenspeicher nicht unbegrenzt wächst und alte Versionen dauerhaft vorhält, kann er kompaktiert werden, um die ältesten Versionen ersetzter Daten zu entfernen.

### Logische Sicht {#logical-view}

Die logische Sicht auf den Speicher ist ein flacher binärer Schlüsselraum. Ein lexikalisch sortierter Index über Schlüssel aus Bytefolgen ermöglicht kostengünstige Bereichsabfragen.

Der Schlüsselraum verwaltet mehrere **Revisionen**. Beim Anlegen des Speichers ist die erste Revision 1. Jede atomare ändernde Operation erzeugt eine neue Revision des Schlüsselraums; eine Transaktionsoperation kann beispielsweise mehrere Operationen enthalten. Alle Daten früherer Revisionen bleiben unverändert. Alte Schlüsselversionen sind über frühere Revisionen weiterhin zugänglich. Auch die Revisionen sind indiziert, sodass Watcher effizient Revisionsbereiche durchlaufen können. Wird der Speicher zur Platzersparnis kompaktiert, werden die Revisionen vor der Kompaktierungsrevision entfernt. Revisionen steigen während der gesamten Lebensdauer eines Clusters monoton an.

Das Leben eines Schlüssels umfasst eine Generation von der Erstellung bis zur Löschung. Jeder Schlüssel kann eine oder mehrere Generationen haben. Das Anlegen eines Schlüssels erhöht seine **Version**, beginnend bei 1, falls der Schlüssel in der aktuellen Revision nicht existiert. Das Löschen erzeugt einen Tombstone für den Schlüssel und beendet dessen aktuelle Generation, indem seine Version auf 0 zurückgesetzt wird. Jede Änderung eines Schlüssels erhöht seine Version. Versionen steigen daher innerhalb einer Schlüsselgeneration monoton an. Bei einer Kompaktierung werden alle Generationen entfernt, die vor der Kompaktierungsrevision endeten. Auch alle vor dieser Revision gesetzten Werte außer dem jeweils neuesten werden entfernt.

### Physische Sicht {#physical-view}

etcd speichert die physischen Daten als Schlüssel-Wert-Paare in einem persistenten [B+-Baum][b+tree]. Aus Effizienzgründen enthält jede Revision des Speicherzustands nur die Differenz zur vorherigen Revision. Einer einzelnen Revision können mehrere Schlüssel im Baum entsprechen.

Der Schlüssel eines Schlüssel-Wert-Paars ist ein 3-Tupel (major, sub, type). Major ist die Speicherrevision, die den Schlüssel enthält. Sub unterscheidet Schlüssel innerhalb derselben Revision. Type ist ein optionales Suffix für besondere Werte, etwa `t`, wenn der Wert einen Tombstone enthält. Der Wert des Schlüssel-Wert-Paars enthält die Änderung gegenüber der vorherigen Revision, also eine Differenz zu ihr. Der B+-Baum ist lexikalisch nach den Bytes der Schlüssel sortiert. Bereichssuchen über Revisionsdifferenzen sind schnell; so lassen sich Änderungen zwischen zwei bestimmten Revisionen rasch ermitteln. Die Kompaktierung entfernt veraltete Schlüssel-Wert-Paare.

etcd hält außerdem einen sekundären [B-Baum][btree]-Index im Arbeitsspeicher, um Bereichsabfragen über Schlüssel zu beschleunigen. Die Schlüssel in diesem Index sind die für Benutzer sichtbaren Schlüssel des Speichers. Der Wert ist ein Zeiger auf die Änderung im persistenten B+-Baum. Die Kompaktierung entfernt ungültig gewordene Zeiger.

etcd ermittelt also die Revisionsinformationen aus dem B-Baum und verwendet anschließend die Revision als Schlüssel, um den Wert aus dem B+-Baum abzurufen (siehe unten).
<p align="center">
  ![MVCC-Datenmodell](/docs/etcd/learning/img/data-model-figure-01.png)
</p>

[b+tree]: https://en.wikipedia.org/wiki/B%2B_tree
[btree]: https://en.wikipedia.org/wiki/B-tree
[persistent-ds]: https://en.wikipedia.org/wiki/Persistent_data_structure
