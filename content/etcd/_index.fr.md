---
title: "Documentation etcd 3.7"
linkTitle: "etcd 3.7"
description: "Guides officiels etcd 3.7 pour développeurs, opérateurs, mises à jour, API et fonctionnement interne."
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
weight: 60
icon: fa-solid fa-gear
sidebar_root_for: self
sidebar_root_link_self: true
section_index: cards
section_index_columns: 3
upstream_source: etcd
categories: [Concept]
search_keywords: [v3.7.3, "Go 1.26.10", NewJournalWriter]
upstream_link: "https://github.com/etcd-io/website/tree/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7"
cascade:
  upstream_source: etcd
  type: docs
  module: [ETCD]
---

etcd est un magasin clé-valeur distribué à cohérence forte. Ces guides traitent de l'installation et de l'exploitation d'etcd, de la mise en œuvre d'applications basées sur ses API, de sa conception, de la mesure des performances, ainsi que de la mise à jour ou de la rétrogradation des clusters dans la branche de version 3.7.

Commencez par [Démarrage rapide](/fr/etcd/quickstart/) pour un cluster local à membre unique, [Installation](/fr/etcd/install/) pour les chemins d'installation pris en charge, ou [Guide des opérations](/fr/etcd/op-guide/) pour les déploiements en production.

## etcd v3.7.3 {#etcd-v3-7-3}

La version de maintenance actuelle est [v3.7.3](https://github.com/etcd-io/etcd/releases/tag/v3.7.3). Les exemples d’installation, Docker et Kubernetes de cette édition ciblent cette version.

- Corrige des accès concurrents non synchronisés entre `Hash` et `Restore` dans le stockage MVCC et dans les opérations `RangeStream` limitées aux clés, ainsi qu’une régression des performances de réplication causée par l’envoi des messages `MsgApp` dans l’ordre inverse par le leader.
- Utilise Go 1.26.10 pour la compilation et met à jour les dépendances OpenTelemetry et `golang.org/x/net` afin de corriger les problèmes de sécurité signalés.
- Déclare obsolète `NewJournalWriter` dans `client/pkg/v3/logutil` ; sa suppression est prévue pour la version v3.8.

Consultez le [journal des modifications en amont](https://github.com/etcd-io/etcd/blob/f164b70fdf458a17aba05dfefc685d7de4c9ca37/CHANGELOG/CHANGELOG-3.7.md#v373-2026-10-22) pour la liste complète des changements.
