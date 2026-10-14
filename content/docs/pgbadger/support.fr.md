---
title: "Assistance et contribution"
linkTitle: "Assistance"
weight: 100
description: "Signalez des bogues, demandez des fonctionnalités, contribuez à des correctifs et trouvez un support professionnel PostgreSQL"
search_keywords: [--help, help]
icon: fa-solid fa-life-ring
module: [PGBADGER]
categories: [Tâche]
aliases: [/pgbadger/support/]
upstream_link: "https://pgbadger.darold.net/#support"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

pgBadger est maintenu dans le cadre d'un projet open source. Les rapports de bogues, les propositions de fonctionnalités, les corrections de documentation et les correctifs sont gérés via le dépôt GitHub du projet amont.

## Signalements de bogues et demandes de fonctionnalités {#bugs-and-features}

1. Passez à la dernière version publiée et vérifiez que le comportement persiste.
2. Recherchez dans les [problèmes ouverts](https://github.com/darold/pgbadger/issues) et les [problèmes fermés](https://github.com/darold/pgbadger/issues?q=is%3Aissue+is%3Aclosed) une réponse existante.
3. Réduisez le problème au plus petit extrait de journal partageable et à la ligne de commande minimale qui permettent encore de le reproduire.
4. Supprimez les identifiants, les requêtes SQL sensibles, les valeurs liées, les noms d’hôtes, les adresses et les données métier.
5. Ouvrez un [nouveau problème](https://github.com/darold/pgbadger/issues/new) avec la version de pgBadger, le système d’exploitation, le format d’entrée, les options exactes, le résultat observé et le résultat attendu.

En cas de plantage ou d'erreur d'analyse, incluez uniquement les lignes de journal minimales et expurgées nécessaires pour reproduire le cas limite. Un journal de production complet ou un rapport généré convient rarement à un ticket public.

## Contribuez à un correctif {#contribute-a-patch}

Le projet inclut un fichier `.editorconfig` pour un espacement cohérent. Veillez à aligner l’aide des commandes, la documentation POD et la documentation Markdown générée lorsqu'un changement affecte un comportement visible pour l’utilisateur.

Le processus de génération de la documentation du projet amont est :

```console
$ perl Makefile.PL
$ make README
```

`doc/pgBadger.pod` est la source principale de la documentation détaillée. `pgbadger --help` fournit la syntaxe et les options, tandis que les fichiers README sont des vues générées. Exécutez les tests pertinents avant de soumettre une demande de fusion.

- [Dépôt source](https://github.com/darold/pgbadger)
- [Demandes de fusion](https://github.com/darold/pgbadger/pulls)
- [Guide de contribution](https://github.com/darold/pgbadger/blob/master/CONTRIBUTING.md)
- [Notes de développement](https://github.com/darold/pgbadger/blob/master/HACKING.md)

## Support commercial {#commercial-support}

Le projet pgBadger ne garantit ni maintenance ni support selon sa licence. Pour obtenir une aide payante concernant la journalisation PostgreSQL, l'analyse de performance ou l'automatisation des rapports, consultez le [répertoire des services professionnels PostgreSQL](https://www.postgresql.org/support/professional_support/).
