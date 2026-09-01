---
title: "Prise en charge et contribution"
linkTitle: "Prise en charge"
weight: 100
description: "Signalez des bogues, demandez des fonctionnalités, contribuez à des correctifs et trouvez un support professionnel PostgreSQL"
icon: fa-solid fa-life-ring
module: [PGBADGER]
categories: [Tâche]
aliases: [/docs/pgbadger/support/]
upstream_link: "https://pgbadger.darold.net/#support"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

pgBadger est maintenu dans le cadre d'un projet open source. Les rapports de bogues, les propositions de fonctionnalités, les corrections de documentation et les correctifs sont gérés via le dépôt GitHub principal.

## Signalements de bogues et demandes de fonctionnalités {#bugs-and-features}

1. Passez à la dernière version publiée et vérifiez que le comportement persiste.
2. Recherchez dans les [problèmes ouverts](https://github.com/darold/pgbadger/issues) et les [problèmes fermés](https://github.com/darold/pgbadger/issues?q=is%3Aissue+is%3Aclosed) une réponse existante.
3. Réduisez le problème à l’échantillon de journal le plus petit possible, qui reproduit encore le comportement.
4. Supprimez les identifiants, les requêtes SQL sensibles, les valeurs liées, les noms d’hôtes, les adresses et les données métier.
5. Ouvrez un [nouveau problème](https://github.com/darold/pgbadger/issues/new) avec la version de pgBadger, le système d’exploitation, le format d’entrée, les options exactes, le résultat observé et le résultat attendu.

En cas de plantage ou d'erreur de parsing, inclure uniquement les lignes de journalisation minimales et nettoyées nécessaires à la reproduction de la limite. Un journal de production complet ou un rapport généré est rarement adapté à une issue publique.

## Contribuez à un correctif {#contribute-a-patch}

Le projet inclut un fichier `.editorconfig` pour un espacement cohérent. Veillez à aligner l’aide en ligne des commandes, la documentation POD et la documentation Markdown générée lorsque un changement affecte un comportement visible pour l’utilisateur.

Le flux de documentation côté amont est :

```console
$ perl Makefile.PL
$ make README
```

`doc/pgBadger.pod` est la source principale en format long. `pgbadger --help` fournit le résumé, tandis que les fichiers README sont des visualisations générées. Exécutez les tests pertinents avant de soumettre une demande de fusion.

- [Dépôt source](https://github.com/darold/pgbadger)
- [Demandes de tirage](https://github.com/darold/pgbadger/pulls)
- [Guide de contribution](https://github.com/darold/pgbadger/blob/master/CONTRIBUTING.md)
- [Notes de développement](https://github.com/darold/pgbadger/blob/master/HACKING.md)

## Support commercial {#commercial-support}

Le projet pgBadger ne garantit ni maintenance ni support selon sa licence. Pour obtenir une aide payante concernant la journalisation PostgreSQL, l'analyse de performance ou l'automatisation des rapports, consultez le [répertoire des services professionnels PostgreSQL](https://www.postgresql.org/support/professional_support/).
