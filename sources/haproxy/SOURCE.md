# HAProxy 3.4 documentation source snapshot

This directory records the complete material used to build the three HAProxy manuals in
`content/docs/haproxy`.

## Snapshot identity

- First imported: 2026-08-16; previous refresh: 2026-08-30 (`v3.4.4`).
- Current English snapshot synchronized: 2026-10-13 (Asia/Shanghai).
- Stable release and current maintenance-branch inputs rechecked: 2026-10-14 (Asia/Shanghai).
- Official manuals: <https://docs.haproxy.org/3.4/>; converted upstream on 2026-10-12.
- Official maintenance repository: <https://git.haproxy.org/?p=haproxy-3.4.git>.
- Latest stable release: `3.4.6`, tag `v3.4.6`, released 2026-09-28.
- Peeled stable tag commit: `56332c50b5291cfbbfd440d958adc988fbf87e2f`.
- Documentation edition: `3.4.6-66`, ref `v3.4.6-66-g16acce1dac1d`.
- Pinned documentation commit: `16acce1dac1dcf1ad5d654204af3a5d45d0e3de8`
  (2026-10-12T15:51:02+02:00).

The official English manuals follow the 3.4 maintenance branch and include changes
after the latest stable release. This edition follows those current manuals,
including their post-release changes, and distinguishes the documentation snapshot
from the stable package version. It does not switch to the 3.5 development branch.

At revalidation on 2026-10-14, the maintenance branch had advanced to
`b6c8fd279985905cfe377b7cf2029e1b1bd3ad9f`. All three manual inputs downloaded
at that head are byte-identical to the pinned `-66` snapshot.
The website's release-download `.txt` copies are older than
the current rendered manuals, so the pinned Git inputs are the source of truth.
Machine-readable identity and per-file checksums are in `SNAPSHOT.json`.

## Transformation

The upstream input comprises 40,216 lines and 2,046,891 bytes across three 80-column text manuals:

- `doc/intro.txt`: 1,695 lines.
- `doc/configuration.txt`: 33,216 lines and 12 top-level chapters.
- `doc/management.txt`: 5,305 lines and 13 top-level chapters.

The local edition preserves the complete manual scope, with the explicitly recorded
editorial corrections below, while adapting the presentation for
Markdown and OINK:

1. The contributor-only formatting note and duplicated plain-text summary are omitted.
2. The Starter Guide becomes nine focused topic pages in the flat HAProxy component root.
3. The Configuration Manual becomes 12 flat chapter pages; all 112 numbered
   sections, including the Summary-omitted section 12.9, are covered.
4. The Management Guide becomes 13 flat chapter pages; all 20 numbered sections are
   covered.
5. Numbered headings become semantic Markdown headings with stable section anchors and local
   cross-references.
6. Keyword and runtime-command signatures become linked definition blocks with fenced syntax.
7. Wrapped paragraphs, nested lists, ASCII matrices, URLs, examples, and placeholders are normalized.
8. Three `_div_*.md` placeholders label the manuals inside one OINK sidebar and one globally weighted
   pager sequence; the placeholders are not rendered pages or pager destinations.

No Chinese translation is included in this snapshot.

## Files and regeneration

- `upstream/intro.txt`: pinned original Starter Guide.
- `upstream/configuration.txt`: pinned complete Configuration Manual.
- `upstream/management.txt`: pinned complete Management Guide.
- `upstream/LICENSE`: HAProxy's license explanation and OpenSSL exception.
- `upstream/GPL-2.0`: complete GNU General Public License version 2 text.
- `upstream/VERSION` and `upstream/VERDATE`: release identity files.
- `SHA256SUMS`: machine-checkable hashes for the complete pinned input.
- `SNAPSHOT.json`: stable-release and documentation-snapshot identities and file hashes.

Run `scripts/import-haproxy.sh` in a tree without an existing snapshot to fetch the original files.
For an authorized refresh, use `scripts/import-haproxy.sh --refresh`; all seven files are
fetched and checked against `SNAPSHOT.json` before the stored inputs are replaced.
Run `scripts/generate-haproxy-docs.py` with Pandoc installed to rebuild 34 reading pages, three
sidebar-divider placeholders, and the HAProxy root page (38 Markdown files total).

## Current English changes (2026-10-13)

All five translated editions follow the regenerated English diff, including:

- `jwt.allow_none_alg`, default rejection of unsigned JWTs, and the explicit opt-in.
- Buffer-size limits and header-block-specific 400/502 behavior.
- Removal of the unsupported `filter-sequence` directive, including its table row,
  signature, explanation, example and links.
- Cache-response eligibility and capture-slot scope in shared `listen` sections.
- Sample types, integer bounds, binary/string/address casts and `hex2i` failure.
- `url_ip`/`url_port` behavior for host names without resolution.
- JSON escaping, the `+utf8` log flag and its terminal-rendering considerations.
- Diagnostic mode `-dD` interaction with `zero-warning` and `-dW`.
- Runtime `show events -s` sanitization.

The three manual divisions and 34 reading pages remain complete. The prior
publication fixes below are retained where the corresponding upstream text
still contains the evidenced defect.

## Publication corrections (2026-10-13)

The pinned upstream inputs are stored verbatim with their `SHA256SUMS`. The generator applies narrow,
reproducible corrections to the published English edition, mirrored in all translations:

- Resolve Management Guide references against that manual and RFC references against
  their RFC, rather than a same-numbered Configuration Manual chapter.
- Preserve fenced-code languages through Pandoc, directive separators such as `bind :25`,
  conditional blocks, backslashes, the FastCGI example, ACL/redirect/rate-limit examples and
  numbered log-field layouts. Omit the incomplete upstream FastCGI `bind *:` line;
  its complete port-80 listener remains.
- Correct IPv6 protocol aliases, the `cap_net_bind_service` privileged-port description,
  unauthorized stats-socket access wording, the October date interpretation, `.ocsp`
  spelling, TLS ticket key byte units and the disabled-by-default `option contstats` typo.
- Correct byte-counter storage to eight bytes, rate-array example syntax, prefix-map
  method names, `src_gpc1_rate`, the 20-bit server-ID hashing period, health-check SNI
  verification fallback and HTTP/1 connection-close wording.
- Mark the CPU chapter's obsolete multiprocess guidance, directing current use to threads.

The implementation evidence is the same pinned commit, including `src/tools.c`,
`src/cfgparse-global.c`, `src/cfgparse-ssl.c`, `src/tcpcheck.c`, `src/ssl_sock.c`,
`src/ssl_ckch.c`, `src/stick_table.c`, `src/map.c`, `src/lb_chash.c` and `src/mux_h1.c`.
The publication ledger at `data/translation-audits/haproxy.json` records the current
source/translation hashes, review boundaries and actual validation results. Earlier
language reviews retain their provenance and have supplemental reviews for these deltas.

## License

HAProxy states that files in its source package are covered by GPLv2 unless expressly stated
otherwise. The complete upstream notice and GPLv2 text are retained here and are also published
under `static/third_party/haproxy/` beside the rendered documentation.
