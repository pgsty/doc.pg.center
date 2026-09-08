#!/usr/bin/env bash
set -euo pipefail

project_dir=$(cd "$(dirname "$0")/.." && pwd)
content_dir="$project_dir/content"
build_dir=$(mktemp -d "${TMPDIR:-/tmp}/pgsql-cc-check.XXXXXX")
trap 'rm -rf "$build_dir"' EXIT

legacy_complete_expected=78
total_complete_expected=215
haproxy_expected=38
etcd_markdown_expected=99
etcd_asset_expected=42
legacy_english_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger} -type f -name '*.md' ! -name '*.zh.md' ! -name '*.fr.md' ! -name '*.ja.md' ! -name '*.de.md' ! -name '*.ru.md' | wc -l | tr -d ' ')
legacy_chinese_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger} -type f -name '*.zh.md' | wc -l | tr -d ' ')
legacy_french_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger} -type f -name '*.fr.md' | wc -l | tr -d ' ')
english_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger,haproxy,etcd} -type f -name '*.md' ! -name '*.zh.md' ! -name '*.fr.md' ! -name '*.ja.md' ! -name '*.de.md' ! -name '*.ru.md' | wc -l | tr -d ' ')
chinese_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger,haproxy,etcd} -type f -name '*.zh.md' | wc -l | tr -d ' ')
french_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger,haproxy,etcd} -type f -name '*.fr.md' | wc -l | tr -d ' ')
japanese_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger,haproxy,etcd} -type f -name '*.ja.md' | wc -l | tr -d ' ')
german_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger,haproxy,etcd} -type f -name '*.de.md' | wc -l | tr -d ' ')
russian_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger,haproxy,etcd} -type f -name '*.ru.md' | wc -l | tr -d ' ')
haproxy_count=$(find "$content_dir/haproxy" -type f -name '*.md' ! -name '*.zh.md' ! -name '*.fr.md' ! -name '*.ja.md' ! -name '*.de.md' ! -name '*.ru.md' | wc -l | tr -d ' ')
haproxy_chinese_count=$(find "$content_dir/haproxy" -type f -name '*.zh.md' | wc -l | tr -d ' ')
haproxy_french_count=$(find "$content_dir/haproxy" -type f -name '*.fr.md' | wc -l | tr -d ' ')
haproxy_divider_count=$(find "$content_dir/haproxy" -maxdepth 1 -type f -name '_div_*.md' ! -name '*.zh.md' ! -name '*.fr.md' ! -name '*.ja.md' ! -name '*.de.md' ! -name '*.ru.md' | wc -l | tr -d ' ')
haproxy_chinese_divider_count=$(find "$content_dir/haproxy" -maxdepth 1 -type f -name '_div_*.zh.md' | wc -l | tr -d ' ')
haproxy_french_divider_count=$(find "$content_dir/haproxy" -maxdepth 1 -type f -name '_div_*.fr.md' | wc -l | tr -d ' ')
haproxy_reading_count=$(find "$content_dir/haproxy" -maxdepth 1 -type f -name '*.md' ! -name '*.zh.md' ! -name '*.fr.md' ! -name '*.ja.md' ! -name '*.de.md' ! -name '*.ru.md' ! -name '_index.md' ! -name '_div_*.md' | wc -l | tr -d ' ')
etcd_markdown_count=$(find "$content_dir/etcd" -type f -name '*.md' ! -name '*.zh.md' ! -name '*.fr.md' ! -name '*.ja.md' ! -name '*.de.md' ! -name '*.ru.md' | wc -l | tr -d ' ')
etcd_chinese_count=$(find "$content_dir/etcd" -type f -name '*.zh.md' | wc -l | tr -d ' ')
etcd_french_count=$(find "$content_dir/etcd" -type f -name '*.fr.md' | wc -l | tr -d ' ')
etcd_asset_count=$(find "$content_dir/etcd" -type f ! -name '*.md' | wc -l | tr -d ' ')
haproxy_weights=$(
  {
    while IFS= read -r source_file; do
      sed -n 's/^weight:[[:space:]]*//p' "$source_file"
    done < <(find "$content_dir/haproxy" -maxdepth 1 -type f -name '*.md' ! -name '*.zh.md' ! -name '*.fr.md' ! -name '*.ja.md' ! -name '*.de.md' ! -name '*.ru.md' ! -name '_index.md' | sort)
  } | sort -n
)

test "$legacy_english_count" -eq "$legacy_complete_expected"
test "$legacy_chinese_count" -eq "$legacy_complete_expected"
test "$legacy_french_count" -eq "$legacy_complete_expected"
test "$english_count" -eq "$total_complete_expected"
test "$chinese_count" -eq "$total_complete_expected"
test "$french_count" -eq "$total_complete_expected"
test "$japanese_count" -eq 105
test "$german_count" -eq 31
test "$russian_count" -eq 187
test "$(find "$content_dir/pgbouncer" -type f -name '*.ja.md' | wc -l | tr -d ' ')" -eq 9
test "$(find "$content_dir/pgbadger" -type f -name '*.de.md' | wc -l | tr -d ' ')" -eq 16
test "$(find "$content_dir/patroni" -type f -name '*.ru.md' | wc -l | tr -d ' ')" -eq 24
test "$(find "$content_dir/pgbouncer" -type f -name '*.ru.md' | wc -l | tr -d ' ')" -eq 9
test "$(find "$content_dir/pgbadger" -type f -name '*.ru.md' | wc -l | tr -d ' ')" -eq 16
test "$(find "$content_dir/etcd" -type f -name '*.ru.md' | wc -l | tr -d ' ')" -eq 99
test "$haproxy_count" -eq "$haproxy_expected"
test "$haproxy_chinese_count" -eq "$haproxy_expected"
test "$haproxy_french_count" -eq "$haproxy_expected"
test "$haproxy_divider_count" -eq 3
test "$haproxy_chinese_divider_count" -eq 3
test "$haproxy_french_divider_count" -eq 3
test "$haproxy_reading_count" -eq 34
test "$etcd_markdown_count" -eq "$etcd_markdown_expected"
test "$etcd_chinese_count" -eq "$etcd_markdown_expected"
test "$etcd_french_count" -eq "$etcd_markdown_expected"
test "$etcd_asset_count" -eq "$etcd_asset_expected"
test "$haproxy_weights" = "$(seq 10 10 370)"
test ! -e "$content_dir/docs"
test ! -e "$content_dir/blog"
for component in patroni pgbackrest pgbouncer pgbadger haproxy etcd; do
  test -d "$content_dir/$component"
  grep -Fq 'type: docs' "$content_dir/$component/_index.md"
  grep -Fq 'sidebar_root_for: self' "$content_dir/$component/_index.md"
  grep -Fq 'outputs: [HTML, RSS, print, markdown, LLMSFULL]' "$content_dir/$component/_index.md"
  grep -Fq 'outputs: [HTML, RSS, print, markdown, LLMSFULL]' "$content_dir/$component/_index.zh.md"
  grep -Fq 'outputs: [HTML, RSS, print, markdown, LLMSFULL]' "$content_dir/$component/_index.fr.md"
done
test -z "$(find "$content_dir/haproxy" -mindepth 1 -type d -print -quit)"

# OINK 1.0 site surface: the bespoke Hero keeps its six-component navigator
# and orbit. Project link resolvers keep partial locales on translated pages
# where available and fall back to the matching English route for gaps.
test -s "$project_dir/layouts/_partials/pgsql/hero-orbit.html"
test -s "$project_dir/layouts/_partials/pgsql/link-target.html"
test -s "$project_dir/layouts/_partials/pgsql/capabilities.html"
test -s "$project_dir/layouts/_markup/render-link.html"
test -s "$project_dir/layouts/_partials/navbar-entry-link.html"
test -s "$project_dir/layouts/_partials/footer.html"
test -s "$project_dir/assets/scss/_styles_project.scss"
for language in en zh fr ja de ru; do
  test -s "$project_dir/data/home/$language.yaml"
  test -s "$project_dir/data/footer/$language.yaml"
  grep -Fq '    partial: pgsql/hero-orbit.html' "$project_dir/data/home/$language.yaml"
  grep -Fq '    key: components' "$project_dir/data/home/$language.yaml"
  grep -Fq '    partial: pgsql/capabilities.html' "$project_dir/data/home/$language.yaml"
done
grep -Fq 'home: [HTML, RSS, markdown, LLMS, NAVJSON]' "$project_dir/hugo.yaml"
grep -Fq '    backlinks: true' "$project_dir/hugo.yaml"
grep -Fq '{.cards}' "$content_dir/haproxy/_index.md"
grep -Fq '{.cards}' "$content_dir/haproxy/_index.zh.md"
if grep -Fq '{{< cards' "$content_dir/haproxy/_index.md" "$content_dir/haproxy/_index.zh.md"; then
  echo 'HAProxy root pages reverted to shortcode cards' >&2
  exit 1
fi

# OINK upstream attribution: one registry entry per tree, one cascade
# that names it, and one upstream_link on every page inside the tree.
for component in patroni pgbackrest pgbouncer pgbadger haproxy etcd; do
  grep -Eq "^${component}:\$" "$project_dir/data/upstreams.yaml"
  grep -Fq "  upstream_source: $component" "$content_dir/$component/_index.md"
done
missing_upstream=$(
  while IFS= read -r source_file; do
    grep -q '^upstream_link:' "$source_file" || echo "$source_file"
  done < <(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger,haproxy,etcd} -type f -name '*.md')
)
if [[ -n "$missing_upstream" ]]; then
  echo 'Pages in a vendored tree without upstream_link front matter:' >&2
  echo "$missing_upstream" >&2
  exit 1
fi

english_list="$build_dir/english.txt"
chinese_list="$build_dir/chinese.txt"
french_list="$build_dir/french.txt"
japanese_pgbouncer_list="$build_dir/japanese-pgbouncer.txt"
english_pgbouncer_list="$build_dir/english-pgbouncer.txt"
(
  cd "$content_dir"
  find patroni pgbackrest pgbouncer pgbadger haproxy etcd -type f -name '*.md' ! -name '*.zh.md' ! -name '*.fr.md' ! -name '*.ja.md' ! -name '*.de.md' ! -name '*.ru.md' | sort
) >"$english_list"
(
  cd "$content_dir"
  find patroni pgbackrest pgbouncer pgbadger haproxy etcd -type f -name '*.zh.md' | sed 's/\.zh\.md$/.md/' | sort
) >"$chinese_list"
(
  cd "$content_dir"
  find patroni pgbackrest pgbouncer pgbadger haproxy etcd -type f -name '*.fr.md' | sed 's/\.fr\.md$/.md/' | sort
) >"$french_list"
diff -u "$english_list" "$chinese_list"
diff -u "$english_list" "$french_list"
(
  cd "$content_dir"
  find pgbouncer -type f -name '*.md' ! -name '*.zh.md' ! -name '*.fr.md' ! -name '*.ja.md' ! -name '*.de.md' ! -name '*.ru.md' | sort
) >"$english_pgbouncer_list"
(
  cd "$content_dir"
  find pgbouncer -type f -name '*.ja.md' | sed 's/\.ja\.md$/.md/' | sort
) >"$japanese_pgbouncer_list"
diff -u "$english_pgbouncer_list" "$japanese_pgbouncer_list"

bad_component_links=$(
  git -C "$project_dir" grep -n -E \
    '\]\(/(patroni|pgbackrest|pgbouncer|pgbadger|haproxy|etcd)/|^\[[^]]+\]:[[:space:]]+/(haproxy|etcd)/' \
    -- ':(glob)content/**/*.zh.md' \
    | grep -E -v '\.(png|gif|svg|json|txt)([?#][^)]*)?\)?$' \
    || true
)
if [[ -n "$bad_component_links" ]]; then
  echo "$bad_component_links" >&2
  echo 'Chinese content contains an English-locale component link' >&2
  exit 1
fi

bad_french_component_links=$(
  git -C "$project_dir" grep -n -E \
    '\]\(/(patroni|pgbackrest|pgbouncer|pgbadger|haproxy|etcd)/|^\[[^]]+\]:[[:space:]]+/(patroni|pgbackrest|pgbouncer|pgbadger|haproxy|etcd)/' \
    -- ':(glob)content/**/*.fr.md' \
    | grep -E -v '\.(png|gif|svg|json|txt)([?#][^)]*)?\)?$' \
    || true
)
if [[ -n "$bad_french_component_links" ]]; then
  echo "$bad_french_component_links" >&2
  echo 'French content contains an English-locale component link' >&2
  exit 1
fi

grep -Eq '^require github\.com/pgsty/oink v1\.0\.0$' "$project_dir/go.mod"

test "$(cat "$project_dir/static/CNAME")" = 'pgsql.cc'
grep -Fxq 'baseURL: https://pgsql.cc/' "$project_dir/hugo.yaml"
grep -Fxq '  productionURL: https://pgsql.cc' "$project_dir/hugo.yaml"
grep -Fq 'title: "Patroni 4.1.5 Documentation"' "$content_dir/patroni/_index.md"
grep -Fq 'title: "Patroni 4.1.5 中文文档"' "$content_dir/patroni/_index.zh.md"
grep -Fq 'title: "pgBackRest 2.59.1 Documentation"' "$content_dir/pgbackrest/_index.md"
grep -Fq 'title: "pgBackRest 2.59.1 中文文档"' "$content_dir/pgbackrest/_index.zh.md"
grep -Fq 'title: "PgBouncer 1.25.2 Documentation"' "$content_dir/pgbouncer/_index.md"
grep -Fq 'title: "PgBouncer 1.25.2 中文文档"' "$content_dir/pgbouncer/_index.zh.md"
grep -Fq 'title: "pgBadger 13.2 Documentation"' "$content_dir/pgbadger/_index.md"
grep -Fq 'title: "pgBadger 13.2 中文文档"' "$content_dir/pgbadger/_index.zh.md"
grep -Fq 'title: "HAProxy 3.4.4 Documentation"' "$content_dir/haproxy/_index.md"
grep -Fq 'title: "HAProxy 3.4.4 中文文档"' "$content_dir/haproxy/_index.zh.md"
grep -Fq 'title: "etcd 3.7 Documentation"' "$content_dir/etcd/_index.md"
grep -Fq 'title: "etcd 3.7 中文文档"' "$content_dir/etcd/_index.zh.md"

python3 "$project_dir/scripts/check-bilingual-parity.py"

hugo --source "$project_dir" --destination "$build_dir/public" --gc --minify --cleanDestinationDir --printPathWarnings --panicOnWarning

TRANSLATION_RENDERED_DIR="$build_dir/public" \
  python3 "$project_dir/scripts/check-component-translations.py" haproxy etcd
python3 "$project_dir/scripts/check-german-parity.py" --allow-partial --rendered-dir "$build_dir/public"
python3 "$project_dir/scripts/check-german-prose.py"
python3 "$project_dir/scripts/check-russian-parity.py" --allow-partial

for page in \
  index.html \
  zh/index.html \
  fr/index.html \
  ja/index.html \
  de/index.html \
  ru/index.html \
  search/index.html \
  zh/search/index.html \
  fr/search/index.html \
  ja/search/index.html \
  de/search/index.html \
  ru/search/index.html \
  attribution/index.html \
  zh/attribution/index.html \
  fr/attribution/index.html \
  ja/attribution/index.html \
  de/attribution/index.html \
  ru/attribution/index.html \
  patroni/index.html \
  zh/patroni/index.html \
  fr/patroni/index.html \
  pgbackrest/index.html \
  zh/pgbackrest/index.html \
  fr/pgbackrest/index.html \
  pgbouncer/index.html \
  zh/pgbouncer/index.html \
  fr/pgbouncer/index.html \
  ja/pgbouncer/index.html \
  de/pgbouncer/index.html \
  ru/pgbouncer/index.html \
  ja/pgbouncer/usage/index.html \
  de/pgbouncer/usage/index.html \
  ru/pgbouncer/usage/index.html \
  pgbadger/index.html \
  zh/pgbadger/index.html \
  fr/pgbadger/index.html \
  de/pgbadger/index.html \
  ru/pgbadger/index.html \
  de/pgbadger/command-line/index.html \
  ru/pgbadger/command-line/index.html \
  haproxy/index.html \
  zh/haproxy/index.html \
  fr/haproxy/index.html \
  haproxy/load-balancing/index.html \
  zh/haproxy/load-balancing/index.html \
  haproxy/http-fundamentals/index.html \
  zh/haproxy/http-fundamentals/index.html \
  haproxy/proxies/index.html \
  zh/haproxy/proxies/index.html \
  fr/haproxy/proxies/index.html \
  haproxy/acls-and-samples/index.html \
  zh/haproxy/acls-and-samples/index.html \
  haproxy/prerequisites/index.html \
  zh/haproxy/prerequisites/index.html \
  haproxy/statistics-and-monitoring/index.html \
  zh/haproxy/statistics-and-monitoring/index.html \
  haproxy/security/index.html \
  zh/haproxy/security/index.html \
  etcd/index.html \
  zh/etcd/index.html \
  fr/etcd/index.html \
  ru/etcd/index.html \
  etcd/quickstart/index.html \
  zh/etcd/quickstart/index.html \
  fr/etcd/quickstart/index.html \
  de/etcd/quickstart/index.html \
  ru/etcd/quickstart/index.html \
  etcd/op-guide/configuration/index.html \
  zh/etcd/op-guide/configuration/index.html \
  fr/etcd/op-guide/configuration/index.html \
  etcd/upgrades/upgrade_3_7/index.html \
  zh/etcd/upgrades/upgrade_3_7/index.html \
  haproxy/intro/index.html \
  haproxy/intro/load-balancing/index.html \
  haproxy/configuration/index.html \
  haproxy/configuration/proxies/index.html \
  haproxy/configuration/acls-and-samples/index.html \
  haproxy/management/index.html \
  haproxy/management/statistics-and-monitoring/index.html \
  haproxy/management/security/index.html \
  pgbadger/command-line/index.html \
  zh/pgbadger/command-line/index.html \
  pgbadger/releases/13/index.html \
  zh/pgbadger/releases/13/index.html \
  patroni/index.md \
  zh/patroni/index.md \
  fr/patroni/index.md \
  ru/patroni/index.md \
  de/patroni/security/index.html \
  ru/patroni/security/index.html \
  de/haproxy/prerequisites/index.html \
  _print/patroni/index.html \
  _print/pgbackrest/index.html \
  _print/pgbouncer/index.html \
  _print/pgbadger/index.html \
  _print/haproxy/index.html \
  _print/etcd/index.html \
  zh/_print/patroni/index.html \
  zh/_print/pgbackrest/index.html \
  zh/_print/pgbouncer/index.html \
  zh/_print/pgbadger/index.html \
  zh/_print/haproxy/index.html \
  zh/_print/etcd/index.html \
  fr/_print/patroni/index.html \
  fr/_print/pgbackrest/index.html \
  fr/_print/pgbouncer/index.html \
  fr/_print/pgbadger/index.html \
  fr/_print/haproxy/index.html \
  fr/_print/etcd/index.html \
  ja/_print/pgbouncer/index.html \
  de/_print/pgbouncer/index.html \
  de/_print/pgbadger/index.html \
  ru/_print/patroni/index.html \
  ru/_print/pgbouncer/index.html \
  ru/_print/pgbadger/index.html \
  ru/_print/etcd/index.html \
  pgbadger/index.md \
  zh/pgbadger/index.md \
  de/pgbadger/index.md \
  ru/pgbadger/index.md \
  haproxy/index.md \
  zh/haproxy/index.md \
  fr/haproxy/index.md \
  haproxy/proxies/index.md \
  zh/haproxy/proxies/index.md \
  haproxy/statistics-and-monitoring/index.md \
  zh/haproxy/statistics-and-monitoring/index.md \
  etcd/index.md \
  zh/etcd/index.md \
  fr/etcd/index.md \
  ru/etcd/index.md \
  etcd/quickstart/index.md \
  zh/etcd/quickstart/index.md \
  third_party/pgbadger/examples/sample.html \
  third_party/pgbadger/examples/errors.html \
  third_party/pgbadger/examples/report/index.html \
  third_party/pgbadger/LICENSE \
  third_party/pgbadger/THIRD-PARTY-LICENSES \
  third_party/haproxy/LICENSE \
  third_party/haproxy/GPL-2.0 \
  img/docs/pgbadger/logo.png \
  img/slonik.svg \
  images/og.png \
  CNAME \
  favicon.ico \
  zh/llms.txt \
  fr/llms.txt \
  ja/llms.txt \
  de/llms.txt \
  ru/llms.txt \
  llms.txt \
  navigation.json \
  zh/navigation.json \
  fr/navigation.json \
  ja/navigation.json \
  de/navigation.json \
  ru/navigation.json \
  patroni/llms-full.txt \
  zh/patroni/llms-full.txt \
  fr/patroni/llms-full.txt \
  ru/patroni/llms-full.txt \
  pgbackrest/llms-full.txt \
  zh/pgbackrest/llms-full.txt \
  pgbouncer/llms-full.txt \
  zh/pgbouncer/llms-full.txt \
  fr/pgbouncer/llms-full.txt \
  ja/pgbouncer/llms-full.txt \
  de/pgbouncer/llms-full.txt \
  ru/pgbouncer/llms-full.txt \
  pgbadger/llms-full.txt \
  zh/pgbadger/llms-full.txt \
  fr/pgbadger/llms-full.txt \
  de/pgbadger/llms-full.txt \
  ru/pgbadger/llms-full.txt \
  haproxy/llms-full.txt \
  zh/haproxy/llms-full.txt \
  fr/haproxy/llms-full.txt \
  etcd/llms-full.txt \
  zh/etcd/llms-full.txt \
  fr/etcd/llms-full.txt \
  ru/etcd/llms-full.txt; do
  test -s "$build_dir/public/$page"
done

python3 - \
  "$build_dir/public/navigation.json" \
  "$build_dir/public/zh/navigation.json" \
  "$build_dir/public/fr/navigation.json" \
  "$build_dir/public/ja/navigation.json" \
  "$build_dir/public/de/navigation.json" \
  "$build_dir/public/ru/navigation.json" <<'PY'
import json
import sys
from pathlib import Path

complete_roots = {
    "/patroni/",
    "/pgbackrest/",
    "/pgbouncer/",
    "/pgbadger/",
    "/haproxy/",
    "/etcd/",
}
expected_roots = {
    "en": complete_roots,
    "zh": complete_roots,
    "fr": complete_roots,
    "ja": complete_roots,
    "de": {"/patroni/", "/pgbouncer/", "/pgbadger/", "/haproxy/", "/etcd/"},
    "ru": complete_roots,
}
for filename, language in zip(sys.argv[1:], expected_roots):
    payload = json.loads(Path(filename).read_text(encoding="utf-8"))
    assert payload["schemaVersion"] == 1
    assert payload["language"] == language
    roots = {child["id"] for child in payload["root"]["children"]}
    assert expected_roots[language] <= roots
PY

for language_root in "" zh/ fr/ ja/ de/ ru/; do
  grep -Fq 'navigation.json' "$build_dir/public/${language_root}llms.txt"
done
grep -Fq 'Source: https://pgsql.cc/patroni/index.md' "$build_dir/public/patroni/llms-full.txt"
grep -Fq 'Source: https://pgsql.cc/zh/patroni/index.md' "$build_dir/public/zh/patroni/llms-full.txt"
grep -Fq 'Source: https://pgsql.cc/fr/patroni/index.md' "$build_dir/public/fr/patroni/llms-full.txt"
grep -Fq 'td-shell-backlinks' "$build_dir/public/patroni/config/index.html"
grep -Fq 'td-shell-backlinks' "$build_dir/public/zh/patroni/config/index.html"
grep -Fq 'Backlinks:' "$build_dir/public/patroni/config/index.md"
grep -Fq '反链：' "$build_dir/public/zh/patroni/config/index.md"

python3 - "$build_dir/public" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import sys


class Anchors(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self.items.append({key: value or "" for key, value in attrs})


def home(language: str) -> tuple[str, list[dict[str, str]]]:
    path = Path(sys.argv[1]) / (f"{language}/index.html" if language != "en" else "index.html")
    text = path.read_text(encoding="utf-8")
    parser = Anchors()
    parser.feed(text)
    return text, parser.items


def has_link(items: list[dict[str, str]], href: str, fallback: str = "") -> bool:
    return any(
        item.get("href") == href
        and item.get("data-fallback-language", "") == fallback
        for item in items
    )


for language in ("en", "zh", "fr"):
    _, items = home(language)
    assert not any("data-fallback-language" in item for item in items), language

for language in ("ja", "de", "ru"):
    text, items = home(language)
    assert "pgsql-link-fallback" in text, language
    assert any(item.get("data-fallback-language") == "en" for item in items), language

_, ja = home("ja")
assert has_link(ja, "/ja/pgbouncer/")
assert has_link(ja, "/ja/patroni/")
assert has_link(ja, "/pgbackrest/user-guide/", "en")

_, de = home("de")
assert has_link(de, "/de/pgbadger/")
assert has_link(de, "/de/patroni/")
assert has_link(de, "/pgbackrest/", "en")

_, ru = home("ru")
assert has_link(ru, "/ru/etcd/")
assert has_link(ru, "/ru/patroni/")
assert has_link(ru, "/ru/haproxy/")
assert has_link(ru, "/haproxy/proxies/", "en")
PY

while IFS= read -r source_file; do
  relative=${source_file#"$content_dir/"}
  if [[ $relative == *.zh.md ]]; then
    route="zh/${relative%.zh.md}"
  elif [[ $relative == *.fr.md ]]; then
    route="fr/${relative%.fr.md}"
  elif [[ $relative == *.ja.md ]]; then
    route="ja/${relative%.ja.md}"
  elif [[ $relative == *.de.md ]]; then
    route="de/${relative%.de.md}"
  elif [[ $relative == *.ru.md ]]; then
    route="ru/${relative%.ru.md}"
  else
    route=${relative%.md}
  fi
  if [[ $(basename "$route") == '_index' || $(basename "$route") == 'index' ]]; then
    route=${route%/*index}
  fi
  route=$(printf '%s' "$route" | tr '[:upper:]' '[:lower:]')
  test -s "$build_dir/public/$route/index.html"
done < <(find "$content_dir/haproxy" -maxdepth 1 -type f -name '*.md' ! -name '_div_*.md' | sort)

while IFS= read -r source_file; do
  relative=${source_file#"$content_dir/"}
  if [[ $relative == *.zh.md ]]; then
    route="zh/${relative%.zh.md}"
  elif [[ $relative == *.fr.md ]]; then
    route="fr/${relative%.fr.md}"
  elif [[ $relative == *.ja.md ]]; then
    route="ja/${relative%.ja.md}"
  elif [[ $relative == *.de.md ]]; then
    route="de/${relative%.de.md}"
  elif [[ $relative == *.ru.md ]]; then
    route="ru/${relative%.ru.md}"
  else
    route=${relative%.md}
  fi
  if [[ $(basename "$route") == '_index' || $(basename "$route") == 'index' ]]; then
    route=${route%/*index}
  fi
  route=$(printf '%s' "$route" | tr '[:upper:]' '[:lower:]')
  test -s "$build_dir/public/$route/index.html"
done < <(find "$content_dir/etcd" -type f -name '*.md' | sort)

for language in ja de ru; do
  while IFS= read -r source_file; do
    relative=${source_file#"$content_dir/"}
    route="$language/${relative%.$language.md}"
    if [[ $(basename "$route") == '_index' || $(basename "$route") == 'index' ]]; then
      route=${route%/*index}
    fi
    route=$(printf '%s' "$route" | tr '[:upper:]' '[:lower:]')
    test -s "$build_dir/public/$route/index.html"
  done < <(find "$content_dir" -type f -name "*.$language.md" ! -name "_div_*.md" | sort)
done

while IFS= read -r source_file; do
  relative=${source_file#"$content_dir/"}
  if [[ $relative == *.zh.md ]]; then
    legacy_route="zh/docs/${relative%.zh.md}"
  else
    legacy_route="docs/${relative%.md}"
  fi
  legacy_route=${legacy_route%/_index}
  test -s "$build_dir/public/$legacy_route/index.html"
done < <(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger,haproxy} -type f -name '*.md' ! -name '*.fr.md' ! -name '*.ja.md' ! -name '*.de.md' ! -name '*.ru.md' ! -name '_div_*.md' | sort)

for divider in intro configuration management; do
  test ! -e "$build_dir/public/haproxy/_div_$divider/index.html"
done

for source_file in \
  sources/pgbadger/SOURCE.md \
  sources/pgbadger/SHA256SUMS \
  sources/pgbadger/site/index.html \
  sources/pgbadger/site/documentation.html \
  sources/pgbadger/upstream/README.md \
  sources/pgbadger/upstream/ChangeLog \
  sources/pgbadger/upstream/LICENSE \
  sources/pgbadger/upstream/RESOURCE-LICENSES \
  sources/pgbadger/pgbadger-a1ad95a035a0c2d246fe632eb1c361d4bde0ddae.tar.gz; do
  test -s "$project_dir/$source_file"
done

for source_file in \
  sources/haproxy/SOURCE.md \
  sources/haproxy/SHA256SUMS \
  sources/haproxy/upstream/intro.txt \
  sources/haproxy/upstream/configuration.txt \
  sources/haproxy/upstream/management.txt \
  sources/haproxy/upstream/LICENSE \
  sources/haproxy/upstream/GPL-2.0 \
  sources/haproxy/upstream/VERSION \
  sources/haproxy/upstream/VERDATE; do
  test -s "$project_dir/$source_file"
done

(cd "$project_dir/sources/pgbadger" && shasum -a 256 -c SHA256SUMS >/dev/null)
(cd "$project_dir/sources/haproxy" && shasum -a 256 -c SHA256SUMS >/dev/null)
test "$(tr -d '\r\n' < "$project_dir/sources/haproxy/upstream/VERSION")" = '3.4.4'
grep -Fq 'HAProxy Starter Guide' "$project_dir/sources/haproxy/upstream/intro.txt"
grep -Fq 'Configuration Manual' "$project_dir/sources/haproxy/upstream/configuration.txt"
grep -Fq 'HAProxy Management Guide' "$project_dir/sources/haproxy/upstream/management.txt"
cmp "$project_dir/sources/haproxy/upstream/LICENSE" "$project_dir/static/third_party/haproxy/LICENSE"
cmp "$project_dir/sources/haproxy/upstream/GPL-2.0" "$project_dir/static/third_party/haproxy/GPL-2.0"

grep -q 'https://pgsql.cc/images/og.png' "$build_dir/public/index.html"
grep -q 'https://pgsql.cc/images/og.png' "$build_dir/public/zh/index.html"
if grep -q '/images/og.png' "$build_dir/public/patroni/index.html"; then
  echo 'A detail page inherited the homepage social image' >&2
  exit 1
fi

python3 "$project_dir/scripts/check-local-links.py" "$build_dir/public"

printf 'Validated OINK v1.0.0 landing and fallback navigation across six locales, backlinks, agent indexes, %s complete EN/ZH/FR component pages, %s JA, %s DE, %s RU component translations, %s HAProxy reading pages, %s etcd Markdown pages, and legacy redirects.\n' \
  "$english_count" "$japanese_count" "$german_count" "$russian_count" "$haproxy_reading_count" "$etcd_markdown_count"
