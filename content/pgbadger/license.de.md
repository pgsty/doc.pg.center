---
title: "Lizenz und Urhebernachweise"
linkTitle: "Lizenz"
weight: 110
description: "Bedingungen der PostgreSQL-Lizenz, Urheberschaft und eingebundene Drittanbieterkomponenten"
search_keywords: []
icon: fa-solid fa-scale-balanced
module: [PGBADGER]
categories: [Referenz]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/LICENSE"
upstream_name: "pgBadger LICENSE"
---

pgBadger ist freie Open-Source-Software, die unter der PostgreSQL-Lizenz verbreitet wird. Sie darf kostenlos genutzt, kopiert, verändert und verteilt werden, sofern die Urheberrechts- und Lizenzhinweise erhalten bleiben.

## PostgreSQL-Lizenz {#postgresql-license}

Copyright (c) 2012-2026, Gilles Darold

Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and this paragraph and the following two paragraphs appear in all copies.

IN NO EVENT SHALL Darold BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF Darold HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Darold SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN “AS IS” BASIS, AND Darold HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

## Autoren und Gestaltungsnachweise {#credits}

- pgBadger ist ein Originalwerk von Gilles Darold.
- Das pgBadger-Logo ist ein Originalentwurf von Damien Cazeils.
- Das Design von pgBadger v4.x stammt vom Unternehmen „Art is code“.
- Die Website ist ein Werk von Gilles Darold.
- Mitwirkende werden im gesamten ChangeLog des Originalprojekts genannt.

## Eingebettete und Berichtsressourcen {#third-party-resources}

Eine angepasste Version des Perl-Moduls `SQL::Beautify` ist in pgBadger eingebettet. Sie ist urheberrechtlich geschützt © 2009 Jonas Kramer und unter der Artistic License 2.0 veröffentlicht.

Für Ressourcen in erzeugten Berichten gelten eigene Lizenzhinweise, darunter:

| Komponente | Lizenz |
|---|---|
| bean.js, Bootstrap, jQuery, Underscore | MIT |
| jqPlot | wahlweise MIT oder GPL-2.0 |
| Schriftart von Font Awesome | SIL Open Font License 1.1 |
| Font Awesome CSS | MIT |

Die Datei `resources/LICENSE` enthält die Lizenzen der Ressourcen. Die Beispielberichte enthalten die Lizenzhinweise ihrer Komponenten.
