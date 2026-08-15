---
title: "License and Credits"
linkTitle: "License"
weight: 110
description: "PostgreSQL License terms, authorship, and bundled third-party components"
icon: fa-solid fa-scale-balanced
module: [PGBADGER]
categories: [Reference]
---

> Source: upstream [`LICENSE`](https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/LICENSE), `README.md`, and `resources/LICENSE` at the pinned source commit.

pgBadger is free and open-source software distributed under the PostgreSQL License. It may be used, copied, modified, and distributed without a fee, subject to retaining the copyright and license notices.

## PostgreSQL License {#postgresql-license}

Copyright (c) 2012-2026, Gilles Darold

Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and this paragraph and the following two paragraphs appear in all copies.

IN NO EVENT SHALL Darold BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF Darold HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Darold SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN “AS IS” BASIS, AND Darold HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

## Authors and design credits {#credits}

- pgBadger is an original work by Gilles Darold.
- The pgBadger logo is an original creation by Damien Cazeils.
- The pgBadger v4.x design came from the “Art is code” company.
- The website is a work of Gilles Darold.
- Contributors are credited throughout the upstream ChangeLog.

## Embedded and report resources {#third-party-resources}

A modified version of the `SQL::Beautify` Perl module is embedded in pgBadger. It is copyright © 2009 Jonas Kramer and published under the Artistic License 2.0.

Generated-report resources have their own notices, including:

| Component | License |
|---|---|
| bean.js, Bootstrap, jQuery, Underscore | MIT |
| jqPlot | MIT or GPL-2.0, at the user's choice |
| Font Awesome font | SIL Open Font License 1.1 |
| Font Awesome CSS | MIT |

The local source snapshot retains the complete upstream `resources/LICENSE`. The bundled example reports are historical generated artifacts and retain their original embedded notices and resource versions.

## Documentation snapshot {#documentation-snapshot}

This pgsql.cc edition reorganizes the upstream documentation into Hugo pages, adds navigation and Chinese reading aids, and preserves exact command help and ChangeLog text where fidelity matters. The pgBadger source documentation remains under the PostgreSQL License; original project names, authorship, and upstream links are retained.

