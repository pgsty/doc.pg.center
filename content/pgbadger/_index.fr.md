---
title: "Documentation de l’instantané de développement de pgBadger 13.2"
linkTitle: pgBadger
weight: 40
description: "Analyse rapide des journaux PostgreSQL et PgBouncer avec des rapports détaillés et autonomes"
search_keywords: [csvlog, jsonlog, logplex, stderr, syslog]
icon: fa-solid fa-otter
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBADGER]
categories: [Concept]
aliases: [/pgbadger/documentation/]
upstream_source: pgbadger
upstream_ref: "v13.2 development snapshot, commit f373ac6 (unreleased)"
upstream_link: "https://github.com/darold/pgbadger/tree/f373ac678c756f66a785c5ab4773d1f05f468d67"
cascade:
  upstream_source: pgbadger
  upstream_ref: "v13.2 development snapshot, commit f373ac6 (unreleased)"
  type: docs
  module: [PGBADGER]
---

Ce manuel suit l’[instantané de développement non publié `f373ac6`](https://github.com/darold/pgbadger/tree/f373ac678c756f66a785c5ab4773d1f05f468d67), dont le commit date du 2026-10-21 (UTC), après la [version stable 13.2](https://github.com/darold/pgbadger/releases/tag/v13.2) publiée le 2025-12-29. Les fonctionnalités décrites pour cet instantané, notamment le filtrage distant en mode de surveillance et l’encodage des répertoires de rapports par base de données, ne font pas partie de l’archive de la version 13.2.

![logo pgBadger](/img/pgbadger/logo.png "pgBadger")

**pgBadger** est un analyseur de journaux PostgreSQL rapide et autonome, écrit en Perl. Il lit les journaux PostgreSQL ou PgBouncer et génère des sorties détaillées au format HTML, texte, binaire, JSON ou CSV brut. Les rapports HTML sont autonomes, interactifs, zoomables et nécessitent uniquement un navigateur web pour être visualisés.

## Pourquoi pgBadger {#why-pgbadger}

pgBadger est conçu pour les gros volumes de journaux et une utilisation opérationnelle :

- un seul programme Perl, sans module obligatoire en dehors de la bibliothèque standard de Perl ;
- détection automatique de `stderr`, `syslog`, `csvlog`, `jsonlog`, RDS, Cloud SQL, logplex, Redshift et PgBouncer en entrée ;
- lecture directe de fichiers locaux, de l'entrée standard, de fichiers distants via SSH, ainsi que d'URL HTTP, FTP ou SFTP ;
- entrée compressée avec gzip, bzip2, lz4, xz, zip ou zstd ;
- analyse parallèle d'un grand fichier ou de nombreux petits fichiers ;
- rapports incrémentiels quotidiens, hebdomadaires et mensuels à la demande ;
- filtres par date et heure, base de données, utilisateur, client, application, processus, session et motif de requête.

## Ce que contiennent les rapports {#report-coverage}

L'ensemble de rapports PostgreSQL couvre :

- activité globale et statistiques des requêtes ;
- requêtes lentes, fréquentes, longues, en attente et annulées ;
- fichiers temporaires, points de contrôle, verrous, sessions et connexions ;
- activité d'auto-vacuum et d'auto-analyse par table ;
- erreurs et événements par gravité et catégorie ;
- distributions par base de données, utilisateur, client, application et type de requête.

L'entrée PgBouncer ajoute des rapports sur le débit, la durée moyenne des requêtes, le nombre de sessions simultanées, la répartition des connexions et des sessions, l'utilisation du pool réservé, ainsi que des rapports sur les erreurs et événements les plus fréquents.

## Plan de la documentation {#documentation-map}

Lisez le manuel dans cet ordre, ou utilisez la barre latérale pour accéder directement à une tâche :

1. [Téléchargez et installez](/fr/pgbadger/download/) pgBadger et ses modules optionnels.
2. Consultez la référence complète [de la ligne de commande](/fr/pgbadger/command-line/).
3. Configurez [la journalisation de PostgreSQL](/fr/pgbadger/postgresql-logging/) avec un préfixe analysable.
4. Choisissez le mode de [traitement parallèle](/fr/pgbadger/parallel-processing/) adapté.
5. Générez des [rapports incrémentiels](/fr/pgbadger/incremental-reports/) de manière sécurisée.
6. Sélectionnez un [format de sortie](/fr/pgbadger/output-formats/) et examinez les [exemples locaux](/fr/pgbadger/sample-reports/).
7. Suivez l'[historique des versions](/fr/pgbadger/releases/), le [support](/fr/pgbadger/support/) et la [licence](/fr/pgbadger/license/).

## Liens vers le projet amont {#upstream-links}

- [Site web du projet](https://pgbadger.darold.net/)
- [Code source](https://github.com/darold/pgbadger)
- [Versions](https://github.com/darold/pgbadger/releases)
- [Suivi des problèmes](https://github.com/darold/pgbadger/issues)
