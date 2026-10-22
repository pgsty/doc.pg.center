---
title: "6. Speicherverwaltung"
linkTitle: "6. Speicher"
weight: 300
description: "Speicherzuteilung, Grenzwerte, Pools, Puffer und Prozessdimensionierung"
icon: fa-solid fa-memory
module: [HAPROXY]
categories: [Aufgabe]
aliases:
  - /haproxy/management/memory/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 6"
---

HAProxy verwendet eine einfache und schnelle Speicherverwaltung mit Pools. Da nur wenige verschiedene Objekttypen benötigt werden, ist es wesentlich effizienter, neue Objekte aus einem Pool mit Objekten passender Größe zu entnehmen, als für jede Größe malloc() aufzurufen. Die Pools sind als Stapel nach dem LIFO-Prinzip organisiert. Neu zugeteilte Objekte stammen daher aus den zuletzt zurückgegebenen Objekten, die noch in den CPU-Caches liegen. Pools ähnlicher Größe werden zusammengelegt, um die Speicherfragmentierung zu begrenzen.

Da die Leistung im Vordergrund steht, wird standardmäßig jedes zurückgegebene Objekt wieder in seinen ursprünglichen Pool gelegt. Der zugeteilte Speicher wird nie freigegeben, weil eine baldige Wiederverwendung erwartet wird.

Über die CLI lässt sich die Speichernutzung der Pools mit dem Befehl "show pools" prüfen:

```shell
> show pools
Dumping pools usage. Use SIGQUIT to flush them.
  - Pool cache_st (16 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccc40=03 [SHARED]
  - Pool pipe (32 bytes): 5 allocated (160 bytes), 5 used, 0 failures, 2 users, @0x9ccac0=00 [SHARED]
  - Pool comp_state (48 bytes): 3 allocated (144 bytes), 3 used, 0 failures, 5 users, @0x9cccc0=04 [SHARED]
  - Pool filter (64 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 3 users, @0x9ccbc0=02 [SHARED]
  - Pool vars (80 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccb40=01 [SHARED]
  - Pool uniqueid (128 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9cd240=15 [SHARED]
  - Pool task (144 bytes): 55 allocated (7920 bytes), 55 used, 0 failures, 1 users, @0x9cd040=11 [SHARED]
  - Pool session (160 bytes): 1 allocated (160 bytes), 1 used, 0 failures, 1 users, @0x9cd140=13 [SHARED]
  - Pool h2s (208 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccec0=08 [SHARED]
  - Pool h2c (288 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cce40=07 [SHARED]
  - Pool spoe_ctx (304 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccf40=09 [SHARED]
  - Pool connection (400 bytes): 2 allocated (800 bytes), 2 used, 0 failures, 1 users, @0x9cd1c0=14 [SHARED]
  - Pool hdr_idx (416 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cd340=17 [SHARED]
  - Pool dns_resolut (480 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccdc0=06 [SHARED]
  - Pool dns_answer_ (576 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccd40=05 [SHARED]
  - Pool stream (960 bytes): 1 allocated (960 bytes), 1 used, 0 failures, 1 users, @0x9cd0c0=12 [SHARED]
  - Pool requri (1024 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cd2c0=16 [SHARED]
  - Pool buffer (8030 bytes): 3 allocated (24090 bytes), 2 used, 0 failures, 1 users, @0x9cd3c0=18 [SHARED]
  - Pool trash (8062 bytes): 1 allocated (8062 bytes), 1 used, 0 failures, 1 users, @0x9cd440=19
Total: 19 pools, 42296 bytes allocated, 34266 used.
```

Der Poolname dient nur als Hinweis: Er entspricht dem ersten Objekttyp, der diesen Pool verwendet. Die Größe in Klammern bezeichnet die Größe der Objekte im Pool. Objektgrößen werden immer auf das nächste Vielfache von 16 Bytes aufgerundet. Die Ausgabe zeigt die Anzahl der aktuell zugeteilten Objekte und die entsprechende Bytezahl, sodass sich der Pool mit dem höchsten Speicherverbrauch leicht ermitteln lässt. Das Feld "used" nennt zusätzlich die Anzahl der gerade verwendeten Objekte. Die Differenz zwischen "allocated" und "used" entspricht den zurückgegebenen Objekten, die sofort wieder verfügbar sind. Die Adresse am Zeilenende ist die Adresse des Pools. Die anschließende Zahl ist sein Index, sofern vorhanden; wurde kein Index zugewiesen, wird -1 ausgegeben.

Mit der Befehlszeilenoption "-m", gefolgt von einer Anzahl Megabytes, lässt sich die Speicherzuteilung pro Prozess begrenzen. Die Grenze erfasst den gesamten adressierbaren Speicher des Prozesses, einschließlich des von Bibliotheken verwendeten Speichers und des Stacks. Sie stellt einen zuverlässigen Grenzwert für Systeme mit begrenzten Ressourcen dar. Die Wirkung entspricht "ulimit -v" auf Systemen, die dies unterstützen, beziehungsweise "ulimit -d" auf anderen Systemen.

Schlägt eine Speicherzuteilung fehl, weil der Grenzwert erreicht ist oder das System nicht genügend Speicher hat, gibt haproxy zunächst alle verfügbaren Objekte aus sämtlichen Pools frei und versucht anschließend erneut, Speicher zuzuteilen. Diese Freigabe ungenutzten Speichers lässt sich auch durch das Signal SIGQUIT an den haproxy-Prozess auslösen.

Beim Neuladen gibt auch der Prozess, der in den Zustand des geordneten Herunterfahrens versetzt wurde, nach jeder Freigabe einer Verbindung automatisch Pool-Speicher frei. So wird möglichst viel Speicher für den neuen Prozess verfügbar.
