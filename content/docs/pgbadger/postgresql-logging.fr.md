---
title: "Configuration de journalisation de PostgreSQL"
linkTitle: "Journalisation PostgreSQL"
weight: 40
description: "Configurer la journalisation des requêtes, log_line_prefix, la locale et les statistiques associées pour pgBadger"
icon: fa-solid fa-database
module: [PGBADGER]
categories: [Tâche]
aliases: [/pgbadger/postgresql-logging/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger ne peut rapporter que les informations écrites par PostgreSQL dans les journaux. Commencez par un préfixe analysable et une politique de journalisation explicite des requêtes, puis ajoutez les événements opérationnels que vous souhaitez analyser.

## Journalisation minimale des requêtes {#minimum-query-logging}

Pour inclure le texte et la durée de la requête, activez la journalisation des instructions basée sur la durée :

```postgresql
log_min_duration_statement = 0
```

`0` enregistre chaque instruction terminée. Sur un serveur très sollicité, sélectionnez une valeur plus élevée en millisecondes afin de contrôler le volume des journaux. Mesurez la surcharge et la croissance du stockage avant d'activer une seuil faible en production.

Si vous avez besoin uniquement de la durée et du nombre de requêtes, et non du texte des requêtes, utilisez :

```postgresql
log_min_duration_statement = -1
log_duration = on
```

Privilégiez `log_min_duration_statement` lorsque vous avez besoin des rapports sur les requêtes les plus lentes et le temps total passé aux requêtes.

## Champs de préfixe requis {#required-prefix-fields}

Un `log_line_prefix` personnalisé doit inclure les deux éléments suivants :

-  un champ de type heure : `%t`, `%m` ou `%n` ;
-  un champ de type processus ou session : `%p` ou `%c`.

Un préfixe `stderr` minimal est :

```postgresql
log_line_prefix = '%t [%p]: '
```

Un préfixe plus utile enregistre l’utilisateur, la base de données, l’application et le client :

```postgresql
log_line_prefix = '%t [%p]: user=%u,db=%d,app=%a,client=%h '
```

Le préfixe équivalent pour une destination syslog omet l'horodatage et les champs processus déjà fournis par syslog :

```postgresql
log_line_prefix = 'user=%u,db=%d,app=%a,client=%h '
```

Un autre ordre de clés pris en charge est :

```postgresql
log_line_prefix = '%t [%p]: db=%d,user=%u,app=%a,client=%h '
```

Lorsque votre préfixe n'est pas l'une des formes reconnues par pgBadger, passez la valeur exacte avec `--prefix`. Ne la simplifiez ni ne la retapez différemment par rapport à `postgresql.conf`.

## Paramètres d'événement recommandés {#recommended-event-settings}

Activez les classes d'événements que vous souhaitez voir apparaître dans le rapport :

```postgresql
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_error_verbosity = default
```

Ces paramètres peuvent générer un trafic de journalisation important. En particulier, `log_temp_files = 0` et `log_autovacuum_min_duration = 0` journalisent chaque événement correspondant ; ajustez-les en fonction de la charge de travail et du budget de rétention.

## Garder les messages serveur en anglais {#message-locale}

Le parseur reconnaît les messages du serveur PostgreSQL en anglais. Utilisez l'une des options suivantes :

```postgresql
lc_messages = 'en_US.UTF-8'
```

ou :

```postgresql
lc_messages = 'C'
```

Les locales telles que `fr_FR.UTF-8` ne sont pas prises en charge par le parseur principal.

## Éviter les conflits entre les paramètres d'instruction {#statement-setting-conflicts}

N'activez pas simultanément `log_min_duration_statement`, `log_duration` et `log_statement = 'all'`. La même exécution peut être journalisée plus d'une fois, ce qui fausse les compteurs de pgBadger et augmente considérablement le volume des journaux.

| Objectif | Paramétrage recommandé |
|---|---|
| Texte de requête et chronométrage | `log_min_duration_statement = 0` ou une seuil choisi |
| Durée et comptage uniquement | `log_min_duration_statement = -1`, `log_duration = on` |
| Audit des énoncés généraux | Traiter `log_statement` comme une politique de journalisation distincte ; ne pas combiner les trois paramètres pour les statistiques de pgBadger |

Après avoir rechargé PostgreSQL, examinez plusieurs entrées de journal réelles avant d'exécuter une analyse importante. Vérifiez que les champs horodatage, identifiant de processus/session, utilisateur, base de données, application et client correspondent au format sélectionné.
