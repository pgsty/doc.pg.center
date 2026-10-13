---
title: "Benchmarks für etcd v2.2.0-rc-memory"
weight: 5500
description: "Leistungsmessungen für etcd v2.2.0-rc-memory"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-2-2-0-rc-memory-benchmarks.md"
aliases: [/etcd/benchmarks/etcd-2-2-0-rc-memory-benchmarks/]
---

## Physischer Rechner {#physical-machine}

GCE-Rechnertyp n1-standard-2

- 1x dedizierte lokale SSD, unter /var/lib/etcd eingebunden
- 1x dedizierter langsamer Datenträger für das Betriebssystem
- 7.5 GB Arbeitsspeicher
- 2x CPUs

## etcd {#etcd}

```
etcd Version: 2.2.0-rc.0+git
Git SHA: 103cb5c
Go Version: go1.5
Go OS/Arch: linux/amd64
```

## Testverfahren {#testing}

Einen etcd-Cluster mit 3 Mitgliedern starten, von denen jedes 2 Kerne verwendet.

Schlüsselnamen sind stets 64 Bytes lang, was einer angemessenen durchschnittlichen Schlüssellänge entspricht.

## Maximaler Speicherverbrauch {#memory-maximal-usage}

- etcd kann den maximalen Speicherverbrauch erreichen, wenn ein Follower ausgefallen ist und der Leader fortlaufend Snapshots sendet.
- `max RSS` ist der höchste in 3 Durchläufen gemessene Speicherverbrauch.

| Wertgröße in Bytes | Schlüsselanzahl  | Datenmenge(MB) | max. RSS(MB) | Verhältnis max. RSS/Datenmenge auf dem Leader |
|-------------|-------------|---------------|-------------|-----------------------------|
| 128  | 50000  | 6 | 433 | 72x |
| 128  | 100000 | 12 | 659 | 54x |
| 128  | 200000 | 24 | 1466 | 61x |
| 1024 | 50000  | 48 | 1253 | 26x |
| 1024 | 100000 | 96 | 2344 | 24x |
| 1024 | 200000 | 192 | 4361 | 22x |

## Schwellenwert für die Datenmenge {#data-size-threshold}

- Wenn etcd den Schwellenwert für die Datenmenge erreicht, kann es leicht zu einer Leader-Wahl kommen, und ein Teil der Vorschläge kann verworfen werden.
- In den meisten Fällen sollte der etcd-Cluster reibungslos arbeiten, solange er den Schwellenwert nicht erreicht. Arbeitet er wegen unzureichender Ressourcen nicht zuverlässig, die Datenmenge reduzieren.

| Wertgröße in Bytes | Begrenzung der Schlüsselanzahl | Empfohlener Schwellenwert für die Datenmenge(MB) | Verbrauchter RSS(MB) |
|-------------|-----------------------|-----------------------------------|------------------|
| 128 | 400K | 48 | 2400 |
| 1024 | 300K | 292 | 6500 |
