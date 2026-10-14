---
title: "Download and Installation"
linkTitle: "Download & Install"
weight: 20
description: "Official releases, packages, requirements, and source installation"
search_keywords: [--content-size, --help, --robot, --version, --zcat, JSON::XS, Text::CSV_XS, content, content-size, help, robot, size, version, zcat, zstdcat]
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [Tutorial]
aliases: [/pgbadger/download/]
upstream_link: "https://pgbadger.darold.net/#download"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

## Choose a distribution channel {#distribution-channels}

| Channel | Use it for | Location |
|---|---|---|
| Official release | Source tarballs and release notes | [GitHub Releases](https://github.com/darold/pgbadger/releases) |
| RPM package | RPM-based Linux distributions | [PostgreSQL Yum Repository](https://yum.postgresql.org/packages/) |
| Debian/Ubuntu package | APT-based Linux distributions | [PostgreSQL Apt Repository](https://wiki.postgresql.org/wiki/Apt) |
| Development source | Current unreleased code | [darold/pgbadger](https://github.com/darold/pgbadger) |

The installation examples use pgBadger 13.2. Check the release page before choosing a version.

## Requirements {#requirements}

The HTML report path needs only:

- a modern Perl distribution;
- a web browser to render the embedded JavaScript charts.

Optional capabilities add the following dependencies:

| Capability | Dependency |
|---|---|
| Parse PostgreSQL CSV logs | `Text::CSV_XS` |
| Write JSON output | `JSON::XS` |
| Read `.gz`, `.bz2`, `.lz4`, `.xz`, `.zip`, or `.zst` input | the matching `zcat`, `bzcat`, `lz4cat`, `xz`, `unzip`, or `zstdcat` utility |

Install JSON support on Debian or Ubuntu:

```console
$ sudo apt-get install libjson-xs-perl
```

On an RPM-based system:

```console
$ sudo yum install perl-JSON-XS
```

Use `--zcat` to override a decompressor path. Supplying one custom command disables mixing different compressed formats in the same invocation.

The `xz` utility must support `--robot` so pgBadger can read archive metadata. Compress lz4 logs with `--content-size` so pgBadger can determine their uncompressed size.

## Install from an official tarball {#install-from-tarball}

Download a release archive, then build and install it with Perl's standard toolchain:

```console
$ tar xzf pgbadger-13.2.tar.gz
$ cd pgbadger-13.2
$ perl Makefile.PL
$ make
$ sudo make install
```

The default `site` layout installs the program as `/usr/local/bin/pgbadger` and the manual page as `/usr/local/share/man/man1/pgbadger.1`.

For a distribution-style installation under `/usr`, generate the Makefile with:

```console
$ perl Makefile.PL INSTALLDIRS=vendor
$ make
$ sudo make install
```

`INSTALLDIRS=perl` is another upstream-supported layout. Inspect the generated paths before installing into a managed system.

## Install development code {#install-development-code}

```console
$ git clone https://github.com/darold/pgbadger.git
$ cd pgbadger
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

Development code may contain changes not yet covered by a release note. Prefer a tagged archive for reproducible production packaging.

## Verify the installation {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

Continue with the [command-line reference](/docs/pgbadger/command-line/) and [PostgreSQL logging configuration](/docs/pgbadger/postgresql-logging/).
