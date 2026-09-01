---
title: "Téléchargement et installation"
linkTitle: "Télécharger et installer"
weight: 20
description: "Versions officielles, paquets, exigences et installation à partir de la source"
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [Tutoriel]
aliases: [/docs/pgbadger/download/]
upstream_link: "https://pgbadger.darold.net/#download"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

## Choisissez un canal de distribution {#distribution-channels}

| Channel | Utilisation | Emplacement |
|---|---|---|
| Version officielle | Archives sources et notes de version | [GitHub Releases](https://github.com/darold/pgbadger/releases) |
| Paquet RPM | Distributions Linux basées sur RPM | [PostgreSQL Yum Repository](https://yum.postgresql.org/packages/) |
| Paquet Debian/Ubuntu | Distributions Linux basées sur APT | [PostgreSQL Apt Repository](https://wiki.postgresql.org/wiki/Apt) |
| Code source de développement | Code actuel non encore publié | [darold/pgbadger](https://github.com/darold/pgbadger) |

La version de documentation disponible sur ce site est basée sur l'arbre source 13.2. Vérifiez toujours la page de publication avant de télécharger : la version locale est intentionnellement figée, tandis que les versions upstream évoluent continuellement.

## Conditions requises {#requirements}

Le chemin du rapport HTML doit uniquement :

- une distribution Perl moderne ;
- un navigateur web pour afficher les graphiques JavaScript intégrés.

Les fonctionnalités facultatives ajoutent les dépendances suivantes :

| Fonctionnalité | Dépendance |
|---|---|
| Analyse des journaux CSV de PostgreSQL | `Text::CSV_XS` |
| Écriture de sortie au format JSON | `JSON::XS` |
| Lecture d'entrée `.gz`, `.bz2`, `.lz4`, `.xz`, `.zip`, ou `.zst` | l'utilitaire correspondant `zcat`, `bzcat`, `lz4cat`, `xz`, `unzip`, ou `zstdcat` |

Installez le support JSON sur Debian ou Ubuntu :

```console
$ sudo apt-get install libjson-xs-perl
```

Sur un système basé sur RPM :

```console
$ sudo yum install perl-JSON-XS
```

Utilisez `--zcat` pour remplacer le chemin du décompresseur. Fournir une commande personnalisée désactive la possibilité d'utiliser plusieurs formats compressés dans la même invocation.

## Installer à partir d'un tarball officiel {#install-from-tarball}

Téléchargez une archive de version, puis générez et installez-la à l'aide de la chaîne d'outils standard de Perl :

```console
$ tar xzf pgbadger-13.2.tar.gz
$ cd pgbadger-13.2
$ perl Makefile.PL
$ make
$ sudo make install
```

Le schéma par défaut `site` installe le programme sous le nom `/usr/local/bin/pgbadger` et la page de manuel sous le nom `/usr/local/share/man/man1/pgbadger.1`.

Pour une installation au style distribution sous `/usr`, générez le fichier Makefile avec :

```console
$ perl Makefile.PL INSTALLDIRS=vendor
$ make
$ sudo make install
```

`INSTALLDIRS=perl` est une autre disposition prise en charge par le projet principal. Vérifiez les chemins générés avant d'installer dans un système géré.

## Installer le code de développement {#install-development-code}

```console
$ git clone https://github.com/darold/pgbadger.git
$ cd pgbadger
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

Le code en développement peut contenir des modifications non encore documentées dans les notes de version. Privilégiez une archive étiquetée pour un conditionnement en production reproductible.

## Vérifier l'installation {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

Poursuivez avec la [référence de la ligne de commande](command-line/) et la [configuration de la journalisation PostgreSQL](postgresql-logging/).
