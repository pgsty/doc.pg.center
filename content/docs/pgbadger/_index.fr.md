---
title: "pgBadger 13.2 Documentation"
linkTitle: pgBadger
weight: 40
description: "Analyse rapide des journaux PostgreSQL et PgBouncer avec des rapports détaillés et autonomes"
icon: fa-solid fa-otter
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBADGER]
categories: [Concept]
aliases: [/docs/pgbadger/documentation/, /pgbadger/]
upstream_source: pgbadger
upstream_link: "https://github.com/darold/pgbadger"
cascade:
  upstream_source: pgbadger
  type: docs
  module: [PGBADGER]
---

![logo pgBadger](/img/docs/pgbadger/logo.png "pgBadger")

**pgBadger** est un analyseur de journaux PostgreSQL rapide et autonome, écrit en Perl. Il lit les journaux PostgreSQL ou PgBouncer et génère des sorties détaillées au format HTML, texte, binaire, JSON ou CSV brut. Les rapports HTML sont autonomes, interactifs, zoomables et nécessitent uniquement un navigateur web pour être visualisés.

## Pourquoi pgBadger {#why-pgbadger}

pgBadger est conçu pour les gros volumes de journaux et une utilisation opérationnelle :

- un programme Perl, sans dépendance obligatoire à des modules Perl non essentiels ;
- détection automatique de `stderr`, `syslog`, `csvlog`, `jsonlog`, RDS, Cloud SQL, logplex, Redshift et PgBouncer en entrée ;
- lecture directe de fichiers locaux, de l'entrée standard, de fichiers distants via SSH, ainsi que d'URL HTTP, FTP ou SFTP ;
- entrée compressée avec gzip, bzip2, lz4, xz, zip ou zstd ;
- analyse parallèle d'un grand fichier ou de nombreux petits fichiers ;
- rapports incrémentiels quotidiens, hebdomadaires et mensuels à la demande ;
- filtres par heure, base de données, utilisateur, client, application, processus, session et motif de requête.

## Ce que contiennent les rapports {#report-coverage}

L'ensemble de rapports PostgreSQL couvre :

- activité globale et statistiques des requêtes ;
- requêtes lentes, fréquentes, longues, en attente et annulées ;
- fichiers temporaires, points de contrôle, verrous, sessions et connexions ;
- activité d'auto-vacuum et d'auto-analyse par table ;
- erreurs et événements par gravité et catégorie ;
- distributions par base de données, utilisateur, client, application et type de requête.

L'entrée PgBouncer ajoute des rapports sur le débit, la durée moyenne des requêtes, le nombre de sessions simultanées, la répartition des connexions et des sessions, l'utilisation du pool réservé, ainsi que des rapports fréquents sur les erreurs et événements.

## Documentation map {#documentation-map}

Lisez le manuel dans cet ordre, ou utilisez la barre latérale pour accéder directement à une tâche :

1. [Téléchargez et installez](/fr/docs/pgbadger/download/) pgBadger et ses modules optionnels.
2. Consultez la référence complète [de la ligne de commande](/fr/docs/pgbadger/command-line/).
3. Configurez [la journalisation de PostgreSQL](/fr/docs/pgbadger/postgresql-logging/) avec un préfixe analysable.
4. Choisissez le mode [traitement parallèle](/fr/docs/pgbadger/parallel-processing/) adapté.
5. Générez des [rapports incrémentiels](/fr/docs/pgbadger/incremental-reports/) de manière sécurisée.
6. Sélectionnez un [format de sortie](/fr/docs/pgbadger/output-formats/) et examinez les [exemples locaux](/fr/docs/pgbadger/sample-reports/).
7. Suivez l'[historique des versions](/fr/docs/pgbadger/releases/), le [support](/fr/docs/pgbadger/support/) et la [licence](/fr/docs/pgbadger/license/).

## Liens en amont {#upstream-links}

- [Site web du projet](https://pgbadger.darold.net/)
- [Code source](https://github.com/darold/pgbadger)
- [Versions](https://github.com/darold/pgbadger/releases)
- [Suivi des problèmes](https://github.com/darold/pgbadger/issues)
