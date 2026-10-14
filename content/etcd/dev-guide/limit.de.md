---
title: Systemgrenzen
weight: 3625
description: "etcd-Grenzen: Anfragen und Speicher"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/limit.md"
---

## Maximale Anfragegröße {#request-size-limit}

etcd ist für kleine Schlüssel-Wert-Paare ausgelegt, wie sie für Metadaten typisch sind. Größere Anfragen funktionieren, können jedoch die Latenz anderer Anfragen erhöhen. Standardmäßig beträgt die maximale Größe einer Anfrage 1.5 MiB. Diese Grenze lässt sich über die Option `--max-request-bytes` des etcd-Servers konfigurieren.

## Maximale Speichergröße {#storage-size-limit}

Die standardmäßige Speichergrenze beträgt 2 GiB und lässt sich über die Option `--quota-backend-bytes` konfigurieren. Für normale Umgebungen werden maximal 8 GiB empfohlen. etcd gibt beim Start eine Warnung aus, wenn der konfigurierte Wert diese Größe überschreitet.
