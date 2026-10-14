# pgBadger source snapshot

This directory records the material used to build the pgBadger documentation in `content/docs/pgbadger`.

## Snapshot identity

- Downloaded: 2026-08-15 (Asia/Shanghai)
- Website: <https://pgbadger.darold.net/>
- Source repository: <https://github.com/darold/pgbadger>
- Source commit: `a1ad95a035a0c2d246fe632eb1c361d4bde0ddae`
- Commit date: 2026-07-14T17:54:12Z
- Latest published release observed during import: v13.2, published 2025-12-29

The source archive is pinned to the commit above. The importer downloads it to an external temporary directory, verifies its SHA-256 before extraction, and removes it when the import finishes. The archive is not stored in this repository. The website files are a live-site snapshot and may not correspond to a repository commit.

## Original website structure

The upstream website has no news pagination. `index.html` is one long page with anchor sections in this order:

1. About
2. News
3. Download
4. License
5. Support
6. Sample reports

The main navigation links to those anchors and to one separate `documentation.html` page. The documentation page contains one table of contents followed by the complete manual. The sample-report section links to a complete report, an incremental report hierarchy, and an error-only report.

The home page stops at v12.4 and contains duplicate 11.1, 11.2, and 11.3 headings with conflicting dates. The reorganized Hugo release pages therefore use the pinned upstream `ChangeLog` as the canonical record. They retain the complete v9.0–v13.2 entries, remove duplicate renderings, and order entries newest first inside one page per major series.

## Files

- `site/`: original home page, standalone documentation page, sitemap, logo, and local website assets.
- `upstream/`: the pinned README, POD source, ChangeLog, contribution guide, software license, and resource-license inventory.
- `SHA256SUMS`: machine-checkable hashes for the retained website, source, license, and report-example files.
- `../../static/third_party/pgbadger/examples/`: offline copies of all three report examples and the complete linked incremental-report tree.

The normal Hugo pages do not load the original website's Google Analytics or remote Google Font request. Historical example reports run only their bundled report scripts.

## SHA-256 inventory

| SHA-256 | Bytes | File |
|---|---:|---|
| `e5a6c4abb48e9e0faed28b20929e4df587009aaba36832bc62183b7ce52d462c` | 64,264 | `site/index.html` |
| `6e1bdb64af18d604223b2342fd42ee9e93eac6b2315aa0baff0cc1a6e1683ee2` | 41,203 | `site/documentation.html` |
| `fd4b3dc0a507d55102350114bb4788ae2277befb0b91ef7cd89711bdf2726ba4` | 1,355 | `site/sitemap.xml` |
| `00c73b9b76a95029a68320e268782ade423e400c881f6d0877c0b8db7bceb234` | 8,408 | `site/logo_pgbadger.png` |
| `bda055ee5adf7f81e71bf4573afff9497d1e5c4701ce746f11e4da1b30865b2e` | 39,060 | `upstream/README.md` |
| `e672f136d6582de4ffa9507ad8c3df1e42d4afdb034da7c7c3ef54ce579a9543` | 153,253 | `upstream/ChangeLog` |
| `01c327c9e7452eef4dd230dbbd0a33229c550b2d9230ff3b16af3a2cf041a2ca` | 1,067 | `upstream/CONTRIBUTING.md` |
| `07f9f28b200132ff1eb52448ee588113fa5526d5981860d20953e18b2cf25119` | 910 | `upstream/LICENSE` |
| `28b90b1b6dc87c3b1dcb53c6a2bcf642d3c9fb05b030d49dc0998303cf556f4d` | 7,568 | `upstream/RESOURCE-LICENSES` |
| `0ada1eec00ff9335c2d8e9b3162918abecd62e127031cd1c7d243764dd3debe7` | 36,241 | `upstream/pgBadger.pod` |
| `4c708efdcea2c5953c35d064be7a29fe4da23467c9accfef7f7a82da5fc6dc4c` | 4,374,483 | external source tarball |
| `7f1892cdbc4fb723f2b1a8fa370fded3c8730d13fd5ea865c10fba92d690ac18` | 4,145,862 | complete report example |
| `d107a7a6e3b0778f5f09d105915b0c72b4539c03769dc811bd220592db9fa5da` | 841,478 | error-only report example |
| `40a40de300f360df4f892ca77faa5aae13b5dec30ddeae1318dee3a0bf8361b0` | 8,772 | incremental-report index |

Run `scripts/import-pgbadger.sh` only in a clean tree without an existing snapshot. Run `scripts/generate-pgbadger-reference.py` after importing to rebuild the six English command-reference and release-history pages. Use `--check` for a read-only freshness check. The generator preserves all reviewed translations.

The pinned archive can be downloaded again from `https://codeload.github.com/darold/pgbadger/tar.gz/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae`. Use a directory outside the repository and verify the archive hash listed above.

The English references apply reviewed documentation errata without changing this source snapshot: the misplaced `--anonymize` continuation, `2919-05` → `2019-05`, escaped `jsonlog` delimiters, the 11.5 idle-time formula grouping, a missing code delimiter in 11.0, `--exlucde-time` in 10.0, and misspelled PostgreSQL setting names. They also explain the implemented `--ssh-sudo` option omitted from upstream help and the whole-hour scope of the `pg_dump` exclusion example.

Translated explanations and release notes are maintained separately; command syntax and original diagnostics remain literal. Technical search terms and their query-token forms are maintained in `search_keywords`. Run `scripts/check-pgbadger.py` and `scripts/test-pgbadger.py` to verify the reviewed edition; add `--rendered-dir` to check publication outputs. The final semantic-review fingerprints and acceptance boundaries are recorded in `data/translation-audits/pgbadger.json`.
