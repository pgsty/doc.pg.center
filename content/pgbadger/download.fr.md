---
title: "Téléchargement et installation"
linkTitle: "Télécharger et installer"
weight: 20
description: "Versions officielles, paquets, prérequis et installation à partir du code source"
search_keywords: [--content-size, --help, --robot, --version, --zcat, JSON::XS, Text::CSV_XS, content, content-size, help, robot, size, version, zcat, zstdcat]
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [Tutoriel]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

## Choisissez un canal de distribution {#distribution-channels}

| Canal | Utilisation | Emplacement |
|---|---|---|
| Version officielle | Archives sources et notes de version | [GitHub Releases](https://github.com/darold/pgbadger/releases) |
| Paquet RPM | Distributions Linux basées sur RPM | [PostgreSQL Yum Repository](https://yum.postgresql.org/packages/) |
| Paquet Debian/Ubuntu | Distributions Linux basées sur APT | [PostgreSQL Apt Repository](https://wiki.postgresql.org/wiki/Apt) |
| Code source de développement | Code actuel non encore publié | [darold/pgbadger](https://github.com/darold/pgbadger) |

La dernière version stable vérifiée le 2026-10-23 est [pgBadger 13.2](https://github.com/darold/pgbadger/releases/tag/v13.2), publiée le 2025-12-29. L’exemple d’installation à partir d’une archive ci-dessous installe cette version. Ce manuel couvre également un instantané de développement non publié ; utilisez le checkout fixé à un commit ci-dessous pour reproduire ses nouveaux comportements.

## Conditions requises {#requirements}

Le rapport HTML ne nécessite que :

- une distribution Perl moderne ;
- un navigateur web pour afficher les graphiques JavaScript intégrés.

Les fonctionnalités facultatives ajoutent les dépendances suivantes :

| Fonctionnalité | Dépendance |
|---|---|
| Analyse des journaux CSV de PostgreSQL | `Text::CSV_XS` |
| Génération de sorties au format JSON | `JSON::XS` |
| Lecture de fichiers `.gz`, `.bz2`, `.lz4`, `.xz`, `.zip` ou `.zst` | l'utilitaire correspondant `zcat`, `bzcat`, `lz4cat`, `xz`, `unzip`, ou `zstdcat` |

Installez le support JSON sur Debian ou Ubuntu :

```console
$ sudo apt-get install libjson-xs-perl
```

Sur un système basé sur RPM :

```console
$ sudo yum install perl-JSON-XS
```

Utilisez `--zcat` pour remplacer le chemin du décompresseur. Fournir une commande personnalisée désactive la possibilité d'utiliser plusieurs formats compressés dans la même invocation.

L’utilitaire `xz` doit prendre en charge `--robot` pour que pgBadger puisse lire les métadonnées de l’archive. Compressez les journaux lz4 avec `--content-size` afin que pgBadger puisse déterminer leur taille décompressée.

## Installer à partir d'une archive officielle {#install-from-tarball}

Téléchargez une archive de version, puis compilez et installez le programme à l'aide de la chaîne d'outils standard de Perl :

```console
$ tar xzf pgbadger-13.2.tar.gz
$ cd pgbadger-13.2
$ perl Makefile.PL
$ make
$ sudo make install
```

Le schéma par défaut `site` installe le programme sous le nom `/usr/local/bin/pgbadger` et la page de manuel sous le nom `/usr/local/share/man/man1/pgbadger.1`.

Pour une installation conforme aux conventions des distributions sous `/usr`, générez le fichier Makefile avec :

```console
$ perl Makefile.PL INSTALLDIRS=vendor
$ make
$ sudo make install
```

`INSTALLDIRS=perl` est une autre disposition prise en charge par le projet amont. Vérifiez les chemins générés avant d'installer dans un système géré.

## Installer le code de développement {#install-development-code}

```console
$ git clone https://github.com/darold/pgbadger.git
$ cd pgbadger
$ git checkout --detach f373ac678c756f66a785c5ab4773d1f05f468d67
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

Ce checkout correspond à l’instantané de développement non publié documenté ici : [`f373ac6`](https://github.com/darold/pgbadger/commit/f373ac678c756f66a785c5ab4773d1f05f468d67), dont le commit date du 2026-10-21 (UTC). Il est postérieur à la version stable 13.2 et ne constitue pas une nouvelle version stable. Le code en développement peut contenir des modifications non encore documentées dans les notes de version ; privilégiez une archive associée à une version publiée pour produire des paquets de production.

## Vérifier l'installation {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

Poursuivez avec la [référence de la ligne de commande](/fr/pgbadger/command-line/) et la [configuration de la journalisation PostgreSQL](/fr/pgbadger/postgresql-logging/).
