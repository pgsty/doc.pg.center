---
title: "Rapports d'exemple"
linkTitle: "Rapports d'exemple"
weight: 80
description: "Consulter les rapports pgBadger complets, incrémentaux et limités aux erreurs"
search_keywords: [--anonymize, anonymize]
icon: fa-solid fa-chart-column
module: [PGBADGER]
categories: [Référence]
aliases: [/pgbadger/sample-reports/]
upstream_link: "https://pgbadger.darold.net/#reports"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

Le contenu d'exemple a été généré par pgBadger 11.8 en mai 2022. La navigation dans les rapports, les graphiques, les styles et les scripts sont disponibles hors ligne.

| Exemple | Ce qu'il illustre | Copie locale |
|---|---|---|
| Rapport complet | Activité PostgreSQL ainsi que les statistiques de PgBouncer | [Ouvrir le rapport complet](/third_party/pgbadger/examples/sample.html) |
| Rapport incrémentiel | Index calendrier, agrégation hebdomadaire et pages quotidiennes | [Ouvrir l'index incrémentiel](/third_party/pgbadger/examples/report/index.html) |
| Erreurs et événements | Un rapport limité aux erreurs et aux événements opérationnels | [Ouvrir le rapport d'erreurs](/third_party/pgbadger/examples/errors.html) |

## Rapport complet {#complete-report}

Le rapport complet est un document HTML autonome. Utilisez la navigation en haut pour examiner les statistiques globales, les requêtes, les sessions, les connexions, les fichiers temporaires, les points de contrôle, l'activité d'autovacuum, les verrous et les graphiques spécifiques à PgBouncer.

Les données constituent un exemple de démonstration, non une référence de benchmark actuelle. Les valeurs, les versions de PostgreSQL et l'interface utilisateur pgBadger intégrée reflètent la date de génération du rapport.

## Hiérarchie incrémentielle {#incremental-hierarchy}

Arborescence des rapports incrémentiels :

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
    └── ressources graphiques et d’interface intégrées
```

L'index principal pointe vers deux rapports hebdomadaires et sept rapports quotidiens. Déplacer uniquement `index.html` romprait les liens ; conservez l'arborescence complète.

## Sécurité et vie privée {#security-and-privacy}

Les rapports réels peuvent exposer du texte SQL, des valeurs liées, des noms de base de données et d'utilisateurs, des noms d'applications, des adresses clientes, des détails d'erreurs et des profils de charge. Avant de publier un rapport :

- utilisez `--anonymize` lorsque les littéraux ne sont pas nécessaires ;
- appliquez les filtres d'inclusion/exclusion avant la génération du rapport ;
- inspectez le rapport HTML final ou les données exportées, et non seulement la ligne de commande ;
- protégez l'emplacement du rapport avec le même soin que les journaux opérationnels.
