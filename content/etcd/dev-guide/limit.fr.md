---
title: Limites système
weight: 3625
description: "etcd limites : requêtes et stockage"
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-guide/limit.md"
---

## Limite de taille de requête {#request-size-limit}

etcd est conçu pour gérer des paires clé-valeur de petite taille, typiques des métadonnées. Les requêtes plus grandes fonctionnent, mais peuvent augmenter la latence des autres requêtes. Par défaut, la taille maximale de toute requête est de 1,5 MiB. Cette limite est configurable via le drapeau `--max-request-bytes` du serveur etcd.

## Limite de taille du stockage {#storage-size-limit}

La limite par défaut de taille de stockage est de 2 GiB, configurable à l'aide du drapeau `--quota-backend-bytes`. Une taille maximale de 8 GiB est recommandée pour les environnements normaux, et etcd émet un avertissement au démarrage si la valeur configurée la dépasse.
