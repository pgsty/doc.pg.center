---
title: "11. Bekannte Fallstricke vermeiden"
linkTitle: "11. Häufige Fallstricke"
weight: 350
description: "Zu vermeidende Bedienfehler und unerwartete Verhaltensweisen"
icon: fa-solid fa-triangle-exclamation
module: [HAPROXY]
categories: [Aufgabe]
aliases:
  - /haproxy/management/traps/
  - /docs/haproxy/management/traps/
  - /haproxy/traps/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 11"
---

Gelegentlich wird berichtet, dass der haproxy-Dienst nach einem Systemneustart nicht gestartet wurde, sich aber von Hand problemlos starten lässt. Meist wird dabei eine Lösung wie keepalived eingesetzt, die die Dienst-IP-Adresse nur dem Master-Knoten eines Clusters zuweist. Solange haproxy an 0.0.0.0 gebunden war, funktionierte dies; nach der Bindung an die virtuelle IP-Adresse nicht mehr. Beim Dienststart gehört die virtuelle IP-Adresse noch nicht zum lokalen Knoten. Wenn HAProxy sich daran binden möchte, lehnt das System dies ab, weil es keine lokale IP-Adresse ist. Die Lösung besteht nicht darin, den Start des haproxy-Dienstes zu verzögern, da dies bei einem Neustart nicht zuverlässig funktionieren würde. Stattdessen muss das System so konfiguriert werden, dass es die Bindung an nicht lokale Adressen erlaubt. Unter Linux lässt sich dies einfach erreichen, indem der sysctl-Parameter net.ipv4.ip_nonlocal_bind auf 1 gesetzt wird. Das ist auch nötig, um den IP-Datenverkehr, der HAProxy für eine bestimmte Zieladresse durchläuft, transparent abzufangen.

Konfigurationen mit mehreren Prozessen und Quellportbereichen scheinen zunächst zu funktionieren, führen unter hoher Last aber zu sporadischen Fehlern: Mehrere Prozesse können versuchen, denselben Quellport für eine Verbindung zum selben Server zu verwenden, was nicht möglich ist. Das System meldet einen Fehler, woraufhin ein erneuter Versuch mit einem anderen Port erfolgt. Ein hoher Wert für den Parameter "retries" kann diesen Effekt bis zu einem gewissen Grad verdecken, erhöht jedoch auch CPU-Auslastung und Verarbeitungszeit. Die Protokolle weisen ebenfalls eine gewisse Anzahl von Wiederholungsversuchen aus. Deshalb sollten Portbereiche in Konfigurationen mit mehreren Prozessen vermieden werden.

Da HAProxy SO_REUSEPORT verwendet und mehrere unabhängige Prozesse an dieselbe Kombination IP:port binden kann, kommt es bei der Fehlerbehebung vor, dass ein alter Prozess noch läuft, wenn ein neuer gestartet wird. Das führt zu widersinnigen Testergebnissen, die den Eindruck erwecken, Konfigurationsänderungen würden ignoriert. Selbst wenn der neue Prozess mit einer neuen Konfiguration neu gestartet wird, erhält und verarbeitet auch der alte Prozess noch eingehende Verbindungen und liefert unerwartete Ergebnisse. Im Zweifelsfall den neuen Prozess stoppen und erneut testen. Funktioniert der Dienst weiterhin, ist sehr wahrscheinlich noch ein alter Prozess aktiv, der gestoppt werden muss. Unter Linux hilft dabei "netstat -lntp".

Beim Hinzufügen von ACL-Einträgen über die Befehlszeile, etwa zum Sperren einer Quelladresse, ist zu beachten, dass diese Einträge nicht mit der Datei synchronisiert werden. Lädt jemand die Konfiguration neu, gehen die Änderungen verloren. Beim Sperren ist dies oft erwünscht, kann aber den Erwartungen widersprechen, wenn die Änderung ein Problem beheben sollte. Siehe dazu die Aktion "add acl" der CLI-Schnittstelle.
