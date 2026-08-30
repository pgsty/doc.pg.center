# HAProxy 3.4 documentation source snapshot

This directory records the complete material used to build the three HAProxy manuals in
`content/haproxy`.

## Snapshot identity

- Imported: 2026-08-16; refreshed: 2026-08-30 (Asia/Shanghai)
- Official rendered guide: <https://docs.haproxy.org/3.4/intro.html>
- Official maintenance repository: <https://git.haproxy.org/?p=haproxy-3.4.git>
- Upstream tag: `v3.4.4`
- Peeled tag commit: `7f03ae65c28605152c7a1a9ba7d9d0bcfb50f8b0`
- Upstream release date: 2026-08-27

The rendered Starter, Configuration, and Management pages identify themselves as HAProxy
`3.4.4`. The pinned source tag is the corresponding public HAProxy `3.4.4`
release and avoids silently following later 3.4 maintenance changes.

## Transformation

The upstream input comprises 40,128 lines and 2,040,685 bytes across three 80-column text manuals:

- `doc/intro.txt`: 1,695 lines.
- `doc/configuration.txt`: 33,148 lines and 12 top-level chapters.
- `doc/management.txt`: 5,285 lines and 13 top-level chapters.

The local edition preserves their complete English prose while adapting the presentation for
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

Run `scripts/import-haproxy.sh` in a tree without an existing snapshot to fetch the original files.
Run `scripts/generate-haproxy-docs.py` with Pandoc installed to rebuild 34 reading pages, three
sidebar-divider placeholders, and the HAProxy root page (38 Markdown files total).

## License

HAProxy states that files in its source package are covered by GPLv2 unless expressly stated
otherwise. The complete upstream notice and GPLv2 text are retained here and are also published
under `static/third_party/haproxy/` beside the rendered documentation.
