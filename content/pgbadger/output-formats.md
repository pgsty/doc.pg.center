---
title: "Output Formats"
linkTitle: "Output Formats"
weight: 70
description: "Choose HTML, text, binary, JSON, or raw CSV output and combine intermediate files"
search_keywords: [--anonymize, --csv-separator, --dump-all-queries, --dump-raw-csv, --extension, --extra-files, --last-parsed, --normalized-only, --outfile, --prettify-json, --query-numbering, JSON::XS, all, anonymize, csv, csv-separator, dump, dump-all-queries, dump-raw-csv, extension, extra, extra-files, files, json, last, last-parsed, normalized, normalized-only, numbering, only, outfile, parsed, prettify, prettify-json, queries, query, query-numbering, raw, separator]
icon: fa-solid fa-file-export
module: [PGBADGER]
categories: [Reference]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger selects output from the filename extension or from `-x` / `--extension`. Use `-o` / `--outfile` more than once to create multiple formats from the same parse.

| Format | Typical extension | Best use |
|---|---|---|
| HTML | `.html` | interactive, human-readable report with charts |
| Text | `.txt` | terminal review and plain archival output |
| Binary | `.bin` | mergeable intermediate statistics and report rebuilds |
| JSON | `.json` | integration with other software; requires `JSON::XS` |
| Raw CSV | chosen output file | row-oriented extraction with `--dump-raw-csv` |

## HTML and text {#html-and-text}

The default output is `out.html`:

```console
$ pgbadger postgresql.log -o report.html
```

HTML normally embeds the scripts, styles, fonts, and report data needed for standalone viewing. `-X` / `--extra-files` moves shared JavaScript and CSS out of incremental reports; keep those assets beside the HTML tree.

Generate text explicitly:

```console
$ pgbadger -x text -o report.txt postgresql.log
```

Use `-` as the output filename to write a supported format to standard output.

## Binary intermediate data {#binary-format}

Binary output separates parsing from presentation. Generate hourly increments from one growing daily log:

```console
$ pgbadger --last-parsed .pgbadger_last_state \
    -o sunday/hour01.bin \
    /var/log/pgsql/postgresql-Sun.log
```

Merge one or more binary files into a fresh report:

```console
$ pgbadger -o sunday.html sunday/*.bin
```

When the server writes one log file per hour, create one binary file for each rotation, then rebuild the cumulative HTML whenever required:

```console
$ pgbadger -o day1/hour01.bin postgresql-2026-08-15_01.log
$ pgbadger -o day1/hour02.bin postgresql-2026-08-15_02.log
$ pgbadger -o day1/hour03.bin postgresql-2026-08-15_03.log
$ pgbadger -o day1.html day1/*.bin
```

Keep binary files from compatible pgBadger versions together. Read the release notes for incremental-format compatibility before upgrading a long-lived report directory.

## JSON {#json-format}

JSON output is intended for programmatic consumers such as monitoring or reporting pipelines:

```console
$ pgbadger -o report.json postgresql.log
```

Install `JSON::XS` first. Add `--prettify-json` for readability when file size and generation time are secondary.

## Raw and query-oriented exports {#raw-exports}

The command reference also provides specialized exports:

- `--dump-raw-csv` parses the log and writes row-oriented CSV without building a report;
- `--csv-separator` changes the raw CSV delimiter, which defaults to a comma in 13.2;
- `--dump-all-queries` emits every query after replacing bind parameters;
- `--normalized-only` writes normalized queries;
- `--query-numbering` numbers query-oriented text output.

These modes may contain application SQL, identifiers, users, client addresses, or literal values. Review the output before sharing it and use `--anonymize` when the intended analysis does not require literals.

