---
title: Maintenance and coverage
description: Reading features, translation coverage, and validation scope.
weight: 30
upstream_source: pgedge
upstream_link: https://github.com/pgEdge/spock/tree/4ac1aec2f0807dc7ee806ab99a6e99a4556186df
type: docs
---


## Reading and feedback {#reading}

Search for function names, settings, or terms. Page controls provide light/dark modes, Paper / Slate / Ink / Terminal presets, Markdown, and print views. Paired translations support Duo View.

This site maintains documentation, not pgEdge software support. Report software issues to the relevant upstream repository. Documentation updates compare the pinned snapshot with a new revision before updating the import manifest.

## Coverage {#coverage}

English content covers the four docs directories in the pinned snapshots, including function references and release notes. Chinese coverage prioritizes getting started, conflicts, replication management, and companion extensions. Untranslated pages have explicit English links. SQL examples were not executed against a database; a successful site build does not validate deployment instructions.

## Known upstream issues {#upstream-issues}

- Step 3 of the [two-node tutorial](/pgedge/spock/two-node/) asks readers to edit `pg_hba.conf`, but its example path ends in `postgresql.conf`. Authentication rules belong in the instance's actual `pg_hba.conf`; `SHOW hba_file;` reports its location.
- The [limitations page](/pgedge/spock/limitations/#ddl-statements-not-replicated) lists `CREATE TABLE...AS...` under statements that are not replicated, then says that it is replicated. This contradiction is preserved from the snapshot; verify behavior for the version in use.

These issues occur in the pinned source snapshot and have not been submitted upstream by this site. Editorial notes are identified separately from the source text.
