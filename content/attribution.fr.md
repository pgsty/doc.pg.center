---
title: "Attribution et licence"
linkTitle: "Attribution"
description: "D’où provient chaque page de ce site, qui en est le titulaire, quelle licence elle porte et où la notice complète est conservée."
icon: fa-solid fa-copyright
page_width: wide
type: docs
sidebar_enabled: false
breadcrumb: false
translation_notice: false
outputs: [HTML, markdown]
---

Le fichier pig.center republie la documentation rédigée par six projets amont. Chaque page de documentation comporte une mention d’un seul trait à la fin, indiquant l’œuvre dont elle est issue, son titulaire du droit d’auteur, sa licence, ainsi qu’un lien renvoyant à la section de cette page qui la traite.

Cette page est cet enregistrement. Elle indique ce qui a été importé, à quelle date, à partir de quelle révision verrouillée, selon quelle licence, et où la notice complète du projet amont est conservée.

> [!NOTE]
> L’anglais, le chinois simplifié et le français couvrent les six collections. Le japonais,
> l’allemand et le russe publient les traductions déjà terminées ; les liens manquants
> renvoient vers la page anglaise correspondante.

> [!NOTE]
> pig.center est un projet de documentation indépendant de la communauté. Il n'est affilié à, approuvé par ni une publication officielle de l'un quelconque des projets ci-dessous, ni du PostgreSQL Global Development Group.
>
>

## Résumé {#summary}

| Composant | Travail du projet amont | Verrouillé à | Licence | Avis conservé |
|---|---|---|---|---|
| [Patroni](/fr/docs/patroni/) | [documentation de Patroni](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [Projet amont `LICENSE`](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/fr/docs/pgbackrest/) | [documentation de pgBackRest](https://pgbackrest.org/) | v2.59.2 (anglais / chinois simplifié) ; v2.59.1 (autres traductions) | [MIT](https://opensource.org/license/mit) | [Projet amont `LICENSE`](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/fr/docs/pgbouncer/) | [documentation de PgBouncer](https://www.pgbouncer.org/) | v1.26.0 (anglais / chinois simplifié) | [ISC](https://opensource.org/license/isc-license-txt) | [Projet amont `COPYRIGHT`](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT) |
| [pgBadger](/fr/docs/pgbadger/) | [documentation de pgBadger](https://pgbadger.darold.net/) | v13.2, commit `a1ad95a` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/fr/docs/haproxy/) | [manuels HAProxy 3.4](https://docs.haproxy.org/3.4/) | v3.4.4, commit `7f03ae6` | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/fr/docs/etcd/) | [documentation etcd v3.7](https://etcd.io/docs/v3.7/) | v3.7, commit `8245979` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Projet amont `LICENSE`](https://github.com/etcd-io/website/blob/main/LICENSE) |

Chaque collection est **adaptée**, et non miroirée. Les titres, ancres, liens croisés, signatures de code, regroupement des pages et navigation sont révisés pour cette édition ; le texte original du projet amont est lui-même conservé. Le crédit en fin de page le précise et fournit un lien vers l'historique des modifications de cette page sur le site.

## Patroni {#patroni}

Importé le 2026-08-15 depuis la documentation [Patroni](https://patroni.readthedocs.io/en/latest/) pour **v4.1.5**, accompagné d'une traduction simplifiée en chinois.

Patroni est protégé par le droit d'auteur (c) 2025 Compose, Zalando SE, contributeurs de Patroni, et est distribué sous la licence [MIT License](https://opensource.org/license/mit). Le texte intégral de la licence est conservé [en amont](https://github.com/patroni/patroni/blob/master/LICENSE).

## pgBackRest {#pgbackrest}

Importé le 2026-08-15 depuis le [site de documentation pgBackRest](https://pgbackrest.org/).
Les éditions anglaise et en chinois simplifié ont été mises à jour le 2026-10-04 vers **v2.59.2**.
Les autres traductions existantes restent à **v2.59.1**, leur dernière mise à jour datant du 2026-08-30.

pgBackRest est protégé par le droit d'auteur (c) 2015-2026 le Groupe de développement mondial de PostgreSQL et David Steele,
et est distribué sous la licence [MIT License](https://opensource.org/license/mit). Le texte complet de la licence est conservé [en amont](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE).

## PgBouncer {#pgbouncer}

Importé le 2026-08-15 depuis le site de documentation [PgBouncer](https://www.pgbouncer.org/) pour **v1.25.2**, accompagné d'une traduction en chinois simplifié.

Les éditions anglaise et en chinois simplifié ont été mises à jour le 2026-10-04 vers
[**v1.26.0**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_0),
à partir des manuels relus de `pigsty.io` et de `pigsty.cc`, respectivement.
Les descriptions de référence ont été vérifiées par rapport à l'implémentation de cette version,
avec la correction de quatre types d'erreurs dans la documentation amont.
Les autres éditions linguistiques conservent la documentation v1.25.2.

PgBouncer est protégé par le droit d'auteur (c) 2007-2009 Marko Kreen, Skype Technologies OÜ, et est distribué sous la licence [ISC License](https://opensource.org/license/isc-license-txt). Le texte intégral de la licence est conservé [en amont](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT).

## pgBadger {#pgbadger}

Importé le 2026-08-15 depuis <https://pgbadger.darold.net/> et depuis [`darold/pgbadger`](https://github.com/darold/pgbadger) au commit [`a1ad95a`](https://github.com/darold/pgbadger/commit/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae), dont la dernière version publiée à ce moment était la v13.2.

pgBadger est protégé par le droit d'auteur (c) 2012-2026 Gilles Darold et est distribué sous la licence [PostgreSQL License](https://opensource.org/license/postgresql). Le texte intégral de la licence est conservé à côté des exemples hors ligne sous le nom [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) et dans `sources/pgbadger/upstream/LICENSE` du dépôt du site.

> [!IMPORTANT]
> pgBadger intègre un module `SQL::Beautify` modifié sous Artistic License 2.0 ; les ressources
> de ses rapports générés comprennent aussi des composants sous licence MIT, GPL-2.0 et SIL Open
> Font License 1.1. L'inventaire complet des ressources en amont est conservé dans
> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES).
> Les [rapports d'exemple](/fr/docs/pgbadger/sample-reports/) publiés ici sont des artefacts historiques
> générés qui conservent leurs mentions d'origine.

## HAProxy {#haproxy}

Importé le 2026-08-16 et mis à jour le 2026-08-30 à partir du dépôt officiel de maintenance HAProxy 3.4 à l'étiquette `v3.4.4`, commit [`7f03ae65c286`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=7f03ae65c28605152c7a1a9ba7d9d0bcfb50f8b0).
Le texte français provient des manuels complets `doc/intro.txt`, `doc/configuration.txt` et `doc/management.txt` — au total 40 128 lignes — réorganisés en 34 pages de lecture.

HAProxy est protégé par le droit d'auteur de 2000 à 2026 par Willy Tarreau et est distribué sous la licence [GNU General Public License version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
L'explication de la licence propre à HAProxy, son exception OpenSSL et le texte complet de la GPLv2 sont publiés dans [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) et [`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0).

> [!WARNING]
> Les pages dérivées de HAProxy ne sont **pas** couvertes par la licence CC BY 4.0 de ce site. Elles sont soumises aux termes de la licence GPLv2 de HAProxy.
>

## etcd {#etcd}

Importé de la documentation officielle etcd v3.7 et mis à jour le 2026-08-30 à l’issue du commit
[`824597935df6`](https://github.com/etcd-io/website/commit/824597935df6e95992ef61c07e3222f4f796ca6c).
L’arborescence source verrouillée est
[`content/en/docs/v3.7`](https://github.com/etcd-io/website/tree/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7).

La documentation etcd est protégée par le droit d'auteur 2013-présent par les auteurs etcd. Son contenu est sous licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), tandis que le code et les exemples de code sont sous licence [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). La notice complète est conservée [en amont](https://github.com/etcd-io/website/blob/main/LICENSE).

## Ce site {#site}

Le texte original rédigé pour pig.center — les pages d'orientation, les éditions complètes en chinois simplifié et en français, les traductions publiées en japonais, allemand et russe, les notes éditoriales et les pages d'accueil localisées — est publié sous [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), sauf lorsqu'une licence amont s'applique à la page.


L'éléphant PostgreSQL (Slonik) présenté sur la page d'accueil est la marque propre du projet PostgreSQL,
extraite du dépôt du site [postgresql.org](https://git.postgresql.org/gitweb/?p=pgweb.git)
et republiée ici sans modification selon
[la politique de marque et de logo de PostgreSQL](https://www.postgresql.org/about/policies/trademarks/)
en tant que référence à PostgreSQL. Il s'agit d'une marque de l'Association communautaire PostgreSQL du Canada et
son utilisation ici n'implique aucune approbation.

Le site est basé sur [OINK](https://oink.pgsty.com/) v1.2.0, un thème Hugo distribué sous licence [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), qui inclut ses propres mentions relatives au projet amont et aux dépendances intégrées dans la source du module.

Les corrections concernant toute attribution sur cette page sont les bienvenues via le dépôt [site repository](https://github.com/pgsty/pig.center/issues).
