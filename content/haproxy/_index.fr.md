---
title: "Documentation HAProxy 3.4.8"
linkTitle: HAProxy
weight: 50
description: "Édition Markdown complète en français des manuels HAProxy 3.4 : Démarrage, Configuration et Gestion"
icon: fa-solid fa-network-wired
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
no_list: true
module: [HAPROXY]
categories: [Référence]
upstream_source: haproxy-20261121
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
cascade:
  upstream_source: haproxy-20261121
  type: docs
  module: [HAPROXY]
---

**HAProxy** est un proxy inverse gratuit, rapide et fiable pour la haute disponibilité, la répartition de charge TCP et HTTP, ainsi que la gestion du trafic applicatif. Ce composant propose la traduction française intégrale des trois manuels principaux de HAProxy 3.4, réorganisés en une séquence de pages Markdown destinée à OINK.

Cette édition suit la version officielle **3.4.8 LTS** publiée le 18 novembre 2026, fixée à [tag v3.4.8](https://git.haproxy.org/?p=haproxy-3.4.git;a=tag;h=v3.4.8). Les traductions vérifiées incluent les mises à jour 3.4.8.

## Choisissez un manuel {#choose-a-manual}

- [Guide de démarrage](/fr/haproxy/load-balancing/) — 9 sujets sur les concepts de répartition de charge, l'architecture HAProxy, les fonctionnalités, le dimensionnement, les versions et l'écosystème.
- [Manuel de configuration](/fr/haproxy/http-fundamentals/) — 12 chapitres couvrant les proxies, les ACL, les échantillons, la journalisation, les filtres et chaque famille d'options.
- [Guide de gestion](/fr/haproxy/prerequisites/) — 13 chapitres sur le démarrage, les rechargements, les ressources, la journalisation, les statistiques, la CLI d'exécution, le débogage et la sécurité.
{.cards}

## Couverture édition {#edition-coverage}

| Manuel | Source amont | Organisation locale |
| --- | ---: | ---: |
| Guide de démarrage | 1 695 lignes | 9 pages plates de sujets |
| Manuel de configuration | 33 277 lignes | 12 pages plates de chapitres |
| Guide de gestion | 5 305 lignes | 13 pages plates de chapitres |

Les 34 pages de lecture sont directement situées sous la racine du composant HAProxy. Trois espaces réservés séparateurs non liés divisent les manuels dans la barre latérale sans ajouter de niveaux de répertoire ni d'arrêts de pagination.

Les manuels originaux complets sont disponibles à la révision amont indiquée ci-dessus. La [notice de licence amont](/third_party/haproxy/LICENSE) et le [texte GPLv2](/third_party/haproxy/GPL-2.0) sont publiés avec les manuels. L'édition complémentaire en chinois simplifié inclut les mises à jour 3.4.8 relues.
