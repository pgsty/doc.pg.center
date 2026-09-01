---
title: "Rapports incrémentiels"
linkTitle: "Rapports incrémentiels"
weight: 60
description: "Générer des rapports quotidiens et hebdomadaires, contrôler la rétention, reconstruire la sortie et ajouter des synthèses mensuelles"
icon: fa-solid fa-calendar-days
module: [PGBADGER]
categories: [Tâche]
aliases: [/docs/pgbadger/incremental-reports/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

Le mode incrémentiel stocke les statistiques analysées sous forme binaire, puis génère un rapport HTML par jour, un rapport cumulatif par semaine et un index au format calendrier reliant ces rapports. Il est destiné à un traitement répété des journaux tournés sans compter deux fois les mêmes entrées.

## Générer des rapports quotidiens et hebdomadaires {#daily-and-weekly}

Exécutez pgBadger après la rotation quotidienne des journaux et spécifiez un répertoire de sortie persistant :

```cron {title="crontab"}
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

`-I` active le mode incrémentiel et `-O` sélectionne le répertoire contenant l'état binaire, l'index calendrier et les rapports générés. pgBadger conserve son propre état incrémentiel dans ce répertoire, donc `--last-parsed` est inutile sauf si vous souhaitez délibérément placer le fichier d'état ailleurs.

Utilisez un répertoire HTML séparé tout en conservant l’état binaire dans le répertoire d’origine :

```console
$ pgbadger -I -O /var/lib/pgbadger/data -H /var/www/pg_reports postgresql.log.1
```

Traitez les fichiers binaires comme des données sources pour des reconstructions ultérieures. Sauvegardez-les ou conservez les journaux d'origine si la régénération du rapport est importante.

## Rétention {#retention}

Gardez uniquement un nombre choisi de semaines :

```console
$ pgbadger --incremental --retention 8 \
    --outdir /var/www/pg_reports \
    /var/log/postgresql/postgresql.log.1
```

Les répertoires semaine et jour plus anciens sont supprimés automatiquement. Testez la politique sur une copie non productive avant de l’activer autour de votre historique de rapports unique.

## Écrire les ressources partagées séparément {#shared-assets}

Par défaut, les rapports HTML intègrent leur JavaScript et leur CSS. Dans un répertoire contenant de nombreux rapports incrémentiels, `-X` / `--extra-files` écrit les ressources partagées séparément et réduit la duplication de sortie :

```console
$ pgbadger -X -I -O /var/www/pg_reports postgresql.log.1
```

Tous les rapports ainsi que leur répertoire de ressources versionnées doivent être déplacés ensemble.

## Reconstruire les rapports existants {#rebuild}

Après une mise à jour de pgBadger ou l'application d'une correction de génération de rapport, reconstruisez le HTML à partir des données binaires conservées :

```console
$ rm /var/www/pg_reports/*.js
$ rm /var/www/pg_reports/*.css
$ pgbadger -X -I -O /var/www/pg_reports --rebuild
```

Utilisez `-E` / `--explode` à nouveau si les rapports originaux ont été générés par base de données.

> Utilisez l'option longue `--rebuild`. Dans la référence actuelle des commandes, `-R` signifie `--retention` ; traiter `-R` comme un raccourci de reconstruction appliquerait l'option incorrecte.

## Ajouter un rapport mensuel {#monthly-reports}

Les rapports quotidiens et hebdomadaires sont automatiques. L’agrégation mensuelle est explicite, car elle peut être coûteuse pour un historique important :

```console
$ pgbadger -X --month-report 2026-07 /var/www/pg_reports/
```

Le mois généré est ajouté à l'index du calendrier. Exécuter à nouveau la commande reconstruit ce mois à partir des données binaires disponibles. Pour l'historique par base de données, répétez `-E` :

```console
$ pgbadger -E -X --month-report 2026-07 /var/www/pg_reports/
```

La référence complète des commandes fournit également `--day-report YYYY-MM-DD`, `--no-week`, `--noreport`, `--start-monday`, et `--iso-week-number` pour des plans plus spécialisés.

Ouvrez l'exemple de rapport incrémental [incremental-report](/third_party/pgbadger/examples/report/index.html) inclus pour examiner le calendrier, les liens par semaine et la hiérarchie des rapports journaliers sans connexion réseau.
