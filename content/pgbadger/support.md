---
title: "Support and Contributing"
linkTitle: "Support"
weight: 100
description: "Report bugs, request features, contribute patches, and find professional PostgreSQL support"
icon: fa-solid fa-life-ring
module: [PGBADGER]
categories: [Task]
aliases: [/docs/pgbadger/support/]
upstream_link: "https://pgbadger.darold.net/#support"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

pgBadger is maintained as an open project. Bug reports, feature proposals, documentation fixes, and patches are handled through the upstream GitHub repository.

## Bugs and feature requests {#bugs-and-features}

1. Upgrade to the newest released version and confirm the behavior still occurs.
2. Search [open issues](https://github.com/darold/pgbadger/issues) and [closed issues](https://github.com/darold/pgbadger/issues?q=is%3Aissue+is%3Aclosed) for an existing answer.
3. Reduce the problem to the smallest safe log sample and command line that still reproduces it.
4. Remove credentials, sensitive SQL, bind values, host names, addresses, and business data.
5. Open a [new issue](https://github.com/darold/pgbadger/issues/new) with the pgBadger version, operating system, input format, exact options, observed result, and expected result.

For crashes or parser mistakes, include only the minimum sanitized log lines needed to reproduce the boundary. A complete production log or generated report is rarely appropriate for a public issue.

## Contribute a patch {#contribute-a-patch}

The project includes an `.editorconfig` file for consistent spacing. Keep command help, POD, and generated Markdown documentation aligned when a change affects user-visible behavior.

The upstream documentation workflow is:

```console
$ perl Makefile.PL
$ make README
```

`doc/pgBadger.pod` is the primary long-form source. `pgbadger --help` supplies the synopsis, while the README files are generated views. Run the relevant tests before submitting a pull request.

- [Source repository](https://github.com/darold/pgbadger)
- [Pull requests](https://github.com/darold/pgbadger/pulls)
- [Contribution guide](https://github.com/darold/pgbadger/blob/master/CONTRIBUTING.md)
- [Development notes](https://github.com/darold/pgbadger/blob/master/HACKING.md)

## Commercial support {#commercial-support}

The pgBadger project does not promise maintenance or support under its license. For paid help with PostgreSQL logging, performance analysis, or report automation, consult the [PostgreSQL professional services directory](https://www.postgresql.org/support/professional_support/).

