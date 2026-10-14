---
title: Upgrades von etcd-Clustern und -Anwendungen
weight: 6500
description: Dokumentationsübersicht zu Upgrades von etcd-Clustern und -Anwendungen
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrading-etcd.md"
---

Dieser Abschnitt enthält Dokumente speziell zu Upgrades von etcd-Clustern und -Anwendungen.

## Upgrade-Richtlinie {#upgrade-policy}

Beachten Sie vor einem Upgrade, dass etcd nur die folgenden beiden Upgrade-Fälle unterstützt:

* **Patch-Upgrade:** Upgrade zwischen Patch-Releases innerhalb derselben Nebenversion (z. B. 3.7.0 - 3.7.1).
* **Upgrade der Nebenversion:** Upgrade um jeweils eine Nebenversion (z. B. 3.6 - 3.7). Upgrades, die eine Nebenversion überspringen, werden nicht unterstützt und schlagen wahrscheinlich fehl. Aktualisieren Sie auf die neueste Patch-Version, bevor Sie auf die nächste Nebenversion aktualisieren.

## Upgrade eines etcd-v3.x-Clusters {#upgrading-an-etcd-v3x-cluster}

* [Upgrade von etcd 3.0 auf 3.1](/de/etcd/upgrades/upgrade_3_1/)
* [Upgrade von etcd 3.1 auf 3.2](/de/etcd/upgrades/upgrade_3_2/)
* [Upgrade von etcd 3.2 auf 3.3](/de/etcd/upgrades/upgrade_3_3/)
* [Upgrade von etcd 3.3 auf 3.4](/de/etcd/upgrades/upgrade_3_4/)
* [Upgrade von etcd 3.4 auf 3.5](/de/etcd/upgrades/upgrade_3_5/)
* [Upgrade von etcd 3.5 auf 3.6](/de/etcd/upgrades/upgrade_3_6/)
* [Upgrade von etcd 3.6 auf 3.7](/de/etcd/upgrades/upgrade_3_7/)

## Upgrade von etcd v2.3 {#upgrading-from-etcd-v23}

* [Upgrade eines v2.3-Clusters auf v3.0](/de/etcd/upgrades/upgrade_3_0/)
