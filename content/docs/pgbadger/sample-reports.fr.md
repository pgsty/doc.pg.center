---
title: "Rapports d'exemple"
linkTitle: "Rapports d'exemple"
weight: 80
description: "Ouvrir des rapports complets, erreur uniquement et incrémentaux pgBadger à partir de l'instantané du site local"
icon: fa-solid fa-chart-column
module: [PGBADGER]
categories: [Référence]
aliases: [/pgbadger/sample-reports/]
upstream_link: "https://pgbadger.darold.net/#reports"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

Le contenu d'exemple a été généré par pgBadger 11.8 en mai 2022. Les exemples originaux sont stockés avec ce site, de sorte que la navigation dans le rapport, les graphiques, les styles et les scripts restent disponibles sans avoir à interroger le serveur d'origine.

| Exemple | Ce qu'il illustre | Copie locale |
|---|---|---|
| Rapport complet | Activité PostgreSQL ainsi que les statistiques de PgBouncer | [Ouvrir le rapport complet](/third_party/pgbadger/examples/sample.html) |
| Rapport incrémentiel | Index calendrier, agrégation hebdomadaire et pages quotidiennes | [Ouvrir l'index incrémentiel](/third_party/pgbadger/examples/report/index.html) |
| Erreurs et événements | Un rapport limité aux erreurs et aux événements opérationnels | [Ouvrir le rapport d'erreurs](/third_party/pgbadger/examples/errors.html) |

## Rapport complet {#complete-report}

Le rapport complet est un document HTML autonome. Utilisez la navigation en haut pour examiner les statistiques globales, les requêtes, les sessions, les connexions, les fichiers temporaires, les points de contrôle, l'activité d'autovacuum, les verrous et les graphiques spécifiques à PgBouncer.

Les données constituent un exemple de démonstration, non une référence de benchmark actuelle. Les valeurs, les versions de PostgreSQL et l'interface utilisateur pgBadger intégrée reflètent la date de génération du rapport.

## Hiérarchie incrémentale {#incremental-hierarchy}

L'exemple incrémental préserve la structure de lien complète :

```text
report/
├── index.html
├── 2012/
│   ├── week-49/index.html
│   ├── week-50/index.html
│   └── 12/06 … 12/index.html
└── 11/
    ├── pgbadger.min.css
    ├── pgbadger.min.js
    └── bundled chart and UI assets
```

L'index principal pointe vers deux rapports hebdomadaires et sept rapports quotidiens. Tous les liens relatifs ont été conservés, donc déplacer uniquement `index.html` romprait l'exemple ; conservez l'arborescence complète.

## Sécurité et vie privée {#security-and-privacy}

Les rapports réels peuvent exposer du texte SQL, des valeurs liées, des noms de base de données et d'utilisateurs, des noms d'applications, des adresses clientes, des détails d'erreurs et des modèles de charge. Avant de publier un rapport :

- utilisez `--anonymize` lorsque les littéraux ne sont pas nécessaires ;
- appliquez les filtres d'inclusion/exclusion avant la génération du rapport ;
- inspectez le rapport HTML final ou les données exportées, et non seulement la ligne de commande ;
- protégez l'emplacement du rapport avec le même soin que les journaux opérationnels.
