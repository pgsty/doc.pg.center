---
title: "Documentation PgBouncer 1.25.2"
linkTitle: PgBouncer
weight: 30
description: >
  PgBouncer - Pooler de connexions léger pour PostgreSQL
icon: fa-solid fa-arrows-turn-to-dots
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBOUNCER]
categories: [Concept]
aliases: [/pgbouncer/]
upstream_source: pgbouncer
upstream_link: "https://www.pgbouncer.org/"
cascade:
  upstream_source: pgbouncer
  type: docs
  module: [PGBOUNCER]
---

**pgbouncer** est un pooler de connexions PostgreSQL. Toute application cliente peut se connecter à **pgbouncer** comme s’il était un serveur PostgreSQL, et **pgbouncer** établira une connexion vers le serveur réel, ou réutilisera l’une de ses connexions existantes.

L'objectif de **pgbouncer** est de réduire l'impact sur les performances lié à l'ouverture de nouvelles connexions vers PostgreSQL.

Afin de ne pas compromettre la sémantique transactionnelle pour le pooling de connexions, **pgbouncer** prend en charge plusieurs types de pooling lors de la rotation des connexions :

- **Pooling de sessions** : Méthode la moins intrusive. Lorsqu’un client se connecte, une connexion serveur lui est attribuée pour toute la durée de sa connexion. Lorsque le client se déconnecte, la connexion serveur est remise dans le pool. Il s’agit de la méthode par défaut.
- **Pooling de transactions** : Une connexion serveur est attribuée à un client uniquement pendant une transaction. Lorsque PgBouncer détecte la fin de la transaction, la connexion serveur est remise dans le pool.
- **Pooling d'instructions** : Méthode la plus agressive. La connexion serveur est remise dans le pool immédiatement après la fin d’une requête. Les transactions à plusieurs instructions sont interdites en ce mode.
