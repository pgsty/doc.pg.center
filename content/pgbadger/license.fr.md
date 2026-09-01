---
title: "Licence et crédits"
linkTitle: "Licence"
weight: 110
description: "Conditions de licence PostgreSQL, auteur et composants tiers intégrés"
icon: fa-solid fa-scale-balanced
module: [PGBADGER]
categories: [Référence]
aliases: [/docs/pgbadger/license/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/LICENSE"
upstream_name: "pgBadger LICENSE"
---

pgBadger est un logiciel libre et open source distribué sous la licence PostgreSQL. Il peut être utilisé, copié, modifié et redistribué sans frais, sous réserve du maintien des mentions de copyright et de licence.

## Licence PostgreSQL {#postgresql-license}

Copyright (c) 2012-2026, Gilles Darold

Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and this paragraph and the following two paragraphs appear in all copies.

IN NO EVENT SHALL Darold BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF Darold HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Darold SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN “AS IS” BASIS, AND Darold HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

## Auteurs et crédits de conception {#credits}

- pgBadger est une œuvre originale de Gilles Darold.
- Le logo de pgBadger est une création originale de Damien Cazeils.
- La conception de pgBadger v4.x a été réalisée par l'entreprise « Art is code ».
- Le site web est une œuvre de Gilles Darold.
- Les contributeurs sont remerciés tout au long du fichier ChangeLog du projet principal.

## Ressources embarquées et de rapport {#third-party-resources}

Une version modifiée du module Perl `SQL::Beautify` est intégrée à pgBadger. Elle est protégée par le droit d'auteur © 2009 Jonas Kramer et publiée sous la Licence Artistic 2.0.

Les ressources du rapport généré ont leurs propres mentions, notamment :

| Composant | Licence |
|---|---|
| bean.js, Bootstrap, jQuery, Underscore | MIT |
| jqPlot | MIT ou GPL-2.0, au choix de l'utilisateur |
| police Font Awesome | SIL Open Font License 1.1 |
| CSS Font Awesome | MIT |

La capture source locale conserve l'intégralité du `resources/LICENSE` d'origine. Les rapports d'exemple intégrés sont des artefacts historiques et conservent leurs notices et versions de ressources d'origine.

## Capture de documentation {#documentation-snapshot}

Cette édition pgsql.cc réorganise la documentation d'origine en pages Hugo, ajoute une navigation et des aides à la lecture en chinois, et conserve intégralement le texte d'aide des commandes et le journal des modifications là où la fidélité est essentielle. La documentation source du projet pgBadger reste soumise à la Licence PostgreSQL ; les noms d'origine du projet, l'auteur et les liens vers les sources d'origine sont conservés.
