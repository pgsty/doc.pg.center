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

Le fichier doc.pg.center republie la documentation rédigée par six projets amont. Chaque page de documentation comporte une mention d’un seul trait à la fin, indiquant l’œuvre dont elle est issue, son titulaire du droit d’auteur, sa licence, ainsi qu’un lien renvoyant à la section de cette page qui la traite.

Cette page est cet enregistrement. Elle indique ce qui a été importé, à quelle date, à partir de quelle révision verrouillée, selon quelle licence, et où la notice complète du projet amont est conservée.

> [!NOTE]
> doc.pg.center est un projet de documentation indépendant de la communauté. Il n'est affilié à, approuvé par ni une publication officielle de l'un quelconque des projets ci-dessous, ni du PostgreSQL Global Development Group.
>
>

## Résumé {#summary}

| Composant | Travail du projet amont | Verrouillé à | Licence | Avis conservé |
|---|---|---|---|---|
| [Patroni](/fr/docs/patroni/) | [documentation de Patroni](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [Projet amont `LICENSE`](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/fr/docs/pgbackrest/) | [documentation de pgBackRest](https://pgbackrest.org/) | v2.59.3 | [MIT](https://opensource.org/license/mit) | [Projet amont `LICENSE`](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/fr/docs/pgbouncer/) | [documentation de PgBouncer](https://www.pgbouncer.org/) | v1.26.0 | [ISC](https://opensource.org/license/isc-license-txt) | [Projet amont `COPYRIGHT`](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT) |
| [pgBadger](/fr/docs/pgbadger/) | [documentation de pgBadger](https://pgbadger.darold.net/) | v13.2, commit `a1ad95a` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/fr/docs/haproxy/) | [manuels HAProxy 3.4](https://docs.haproxy.org/3.4/) | instantané 3.4.6-66, commit `16acce1` ; version stable 3.4.6 | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/fr/docs/etcd/) | [documentation etcd v3.7](https://etcd.io/docs/v3.7/) | v3.7, commit `d20f8ae` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Projet amont `LICENSE`](https://github.com/etcd-io/website/blob/main/LICENSE) |

Chaque collection est **adaptée**, et non miroirée. Les titres, ancres, liens croisés, signatures de code, regroupement des pages et navigation sont révisés pour cette édition ; le texte original du projet amont est lui-même conservé. Le crédit en fin de page le précise et fournit un lien vers l'historique des modifications de cette page sur le site.

## Patroni {#patroni}

Importé le 2026-08-15 depuis la [documentation de Patroni](https://patroni.readthedocs.io/en/latest/)
pour **v4.1.5**.

Patroni est protégé par le droit d'auteur (c) 2025 Compose, Zalando SE, contributeurs de Patroni, et est distribué sous la licence [MIT License](https://opensource.org/license/mit). Le texte intégral de la licence est conservé [en amont](https://github.com/patroni/patroni/blob/master/LICENSE).

## pgBackRest {#pgbackrest}

Importé le 2026-08-15 depuis le [site de documentation pgBackRest](https://pgbackrest.org/)
et mis à jour le 2026-10-13 vers **v2.59.3**.

pgBackRest est protégé par le droit d'auteur (c) 2015-2026 le Groupe de développement mondial de PostgreSQL et David Steele,
et est distribué sous la licence [MIT License](https://opensource.org/license/mit). Le texte complet de la licence est conservé [en amont](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE).

## PgBouncer {#pgbouncer}

Importé le 2026-08-15 depuis le [site de documentation PgBouncer](https://www.pgbouncer.org/)
pour **v1.25.2** et mis à jour le 2026-10-13 vers
[**v1.26.0**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_0).

PgBouncer est protégé par le droit d'auteur (c) 2007-2009 Marko Kreen, Skype Technologies OÜ,
et est distribué sous la licence [ISC License](https://opensource.org/license/isc-license-txt).
Le texte intégral de la licence est conservé
[en amont](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT).

## pgBadger {#pgbadger}

Importé le 2026-08-15 depuis <https://pgbadger.darold.net/> et depuis [`darold/pgbadger`](https://github.com/darold/pgbadger) au commit [`a1ad95a`](https://github.com/darold/pgbadger/commit/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae), dont la dernière version publiée à ce moment était la v13.2.

pgBadger est protégé par le droit d'auteur (c) 2012-2026 Gilles Darold et est distribué sous la licence [PostgreSQL License](https://opensource.org/license/postgresql). Le texte intégral de la licence est conservé à côté des exemples hors ligne sous le nom [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) et dans `static/third_party/pgbadger/LICENSE` du dépôt du site.

> [!IMPORTANT]
> pgBadger intègre un module `SQL::Beautify` modifié sous Artistic License 2.0 ; les ressources
> de ses rapports générés comprennent aussi des composants sous licence MIT, GPL-2.0 et SIL Open
> Font License 1.1. L'inventaire complet des ressources en amont est conservé dans
> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES).
> Les [rapports d'exemple](/fr/docs/pgbadger/sample-reports/) publiés ici sont des artefacts historiques
> générés qui conservent leurs mentions d'origine.

## HAProxy {#haproxy}

Importé le 2026-08-16, puis mis à jour le 2026-08-30 et le 2026-10-13 à partir du dépôt officiel de maintenance HAProxy 3.4. Cette édition suit la documentation anglaise à l’instantané **3.4.6-66**, fixé au commit [`16acce1dac1d`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=16acce1dac1dcf1ad5d654204af3a5d45d0e3de8). La dernière version stable est **3.4.6**, au tag `v3.4.6` ; l’instantané comprend des modifications de documentation postérieures à cette version.
Le texte provient des manuels complets `doc/intro.txt`, `doc/configuration.txt` et `doc/management.txt` — au total 40 216 lignes — réorganisés en 34 pages de lecture.

HAProxy est protégé par le droit d'auteur de 2000 à 2026 par Willy Tarreau et est distribué sous la licence [GNU General Public License version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
L'explication de la licence propre à HAProxy, son exception OpenSSL et le texte complet de la GPLv2 sont publiés dans [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) et [`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0).

> [!WARNING]
> Les pages dérivées de HAProxy ne sont **pas** couvertes par la licence CC BY 4.0 de ce site. Elles sont soumises aux termes de la licence GPLv2 de HAProxy.
>

## etcd {#etcd}

Importé de la documentation officielle etcd v3.7 et mis à jour le 2026-10-13 à l’issue du commit
[`d20f8ae346da`](https://github.com/etcd-io/website/commit/d20f8ae346da60ab6eb6f24f200753b328aa9fcc).
L’arborescence source verrouillée est
[`content/en/docs/v3.7`](https://github.com/etcd-io/website/tree/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7).

La documentation etcd est protégée par le droit d'auteur 2013-présent par les auteurs etcd. Son contenu est sous licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), tandis que le code et les exemples de code sont sous licence [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). La notice complète est conservée [en amont](https://github.com/etcd-io/website/blob/main/LICENSE).

## Ce site {#site}

Le texte original rédigé pour doc.pg.center est publié sous [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), sauf lorsqu'une licence amont s'applique à la page.


L'éléphant PostgreSQL (Slonik) présenté sur la page d'accueil est la marque propre du projet PostgreSQL,
extraite du dépôt du site [postgresql.org](https://git.postgresql.org/gitweb/?p=pgweb.git)
et republiée ici sans modification selon
[la politique de marque et de logo de PostgreSQL](https://www.postgresql.org/about/policies/trademarks/)
en tant que référence à PostgreSQL. Il s'agit d'une marque de l'Association communautaire PostgreSQL du Canada et
son utilisation ici n'implique aucune approbation.

Le site est basé sur [OINK](https://oink.pgsty.com/) v1.2.0, un thème Hugo distribué sous licence [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), qui inclut ses propres mentions relatives au projet amont et aux dépendances intégrées dans la source du module.

Les corrections concernant toute attribution sur cette page sont les bienvenues via le dépôt [site repository](https://github.com/pgsty/doc.pg.center/issues).
