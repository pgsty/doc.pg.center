#!/usr/bin/env bash
set -euo pipefail

project_dir=$(cd "$(dirname "$0")/.." && pwd)
content_dir="$project_dir/content"
build_dir=$(mktemp -d "${TMPDIR:-/tmp}/pgsql-cc-check.XXXXXX")
trap 'rm -rf "$build_dir"' EXIT

bilingual_expected=78
haproxy_expected=38
etcd_markdown_expected=99
etcd_asset_expected=42
english_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger} -type f -name '*.md' ! -name '*.zh.md' | wc -l | tr -d ' ')
chinese_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger} -type f -name '*.zh.md' | wc -l | tr -d ' ')
haproxy_count=$(find "$content_dir/haproxy" -type f -name '*.md' ! -name '*.zh.md' | wc -l | tr -d ' ')
haproxy_chinese_count=$(find "$content_dir/haproxy" -type f -name '*.zh.md' | wc -l | tr -d ' ')
haproxy_divider_count=$(find "$content_dir/haproxy" -maxdepth 1 -type f -name '_div_*.md' | wc -l | tr -d ' ')
haproxy_reading_count=$(find "$content_dir/haproxy" -maxdepth 1 -type f -name '*.md' ! -name '_index.md' ! -name '_div_*.md' | wc -l | tr -d ' ')
etcd_markdown_count=$(find "$content_dir/etcd" -type f -name '*.md' | wc -l | tr -d ' ')
etcd_asset_count=$(find "$content_dir/etcd" -type f ! -name '*.md' | wc -l | tr -d ' ')
haproxy_weights=$(
  {
    while IFS= read -r source_file; do
      sed -n 's/^weight:[[:space:]]*//p' "$source_file"
    done < <(find "$content_dir/haproxy" -maxdepth 1 -type f -name '*.md' ! -name '_index.md' | sort)
  } | sort -n
)

test "$english_count" -eq "$bilingual_expected"
test "$chinese_count" -eq "$bilingual_expected"
test "$haproxy_count" -eq "$haproxy_expected"
test "$haproxy_chinese_count" -eq 0
test "$haproxy_divider_count" -eq 3
test "$haproxy_reading_count" -eq 34
test "$etcd_markdown_count" -eq "$etcd_markdown_expected"
test "$etcd_asset_count" -eq "$etcd_asset_expected"
test "$haproxy_weights" = "$(seq 10 10 370)"
test ! -e "$content_dir/docs"
test ! -e "$content_dir/blog"
for component in patroni pgbackrest pgbouncer pgbadger haproxy etcd; do
  test -d "$content_dir/$component"
  grep -Fq 'type: docs' "$content_dir/$component/_index.md"
  grep -Fq 'sidebar_root_for: self' "$content_dir/$component/_index.md"
done
test -z "$(find "$content_dir/haproxy" -mindepth 1 -type d -print -quit)"

# OINK 0.6.0 upstream attribution: one registry entry per tree, one cascade
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
(
  cd "$content_dir"
  find patroni pgbackrest pgbouncer pgbadger -type f -name '*.md' ! -name '*.zh.md' | sort
) >"$english_list"
(
  cd "$content_dir"
  find patroni pgbackrest pgbouncer pgbadger -type f -name '*.zh.md' | sed 's/\.zh\.md$/.md/' | sort
) >"$chinese_list"
diff -u "$english_list" "$chinese_list"

if rg -n '\]\(/(patroni|pgbackrest|pgbouncer|pgbadger)(/|\))' "$content_dir" -g '*.zh.md'; then
  echo 'Chinese content contains an English-locale component link' >&2
  exit 1
fi

grep -Eq '^require github\.com/pgsty/oink v0\.6\.0$' "$project_dir/go.mod"

test "$(cat "$project_dir/static/CNAME")" = 'pgsql.cc'
grep -Fxq 'baseURL: https://pgsql.cc/' "$project_dir/hugo.yaml"
grep -Fxq '  productionURL: https://pgsql.cc' "$project_dir/hugo.yaml"
grep -Fq 'title: "Patroni 4.1.5 Documentation"' "$content_dir/patroni/_index.md"
grep -Fq 'title: "Patroni 4.1.5 中文文档"' "$content_dir/patroni/_index.zh.md"
grep -Fq 'title: "pgBackRest 2.59.0 Documentation"' "$content_dir/pgbackrest/_index.md"
grep -Fq 'title: "pgBackRest 2.59.0 中文文档"' "$content_dir/pgbackrest/_index.zh.md"
grep -Fq 'title: "PgBouncer 1.25.2 Documentation"' "$content_dir/pgbouncer/_index.md"
grep -Fq 'title: "PgBouncer 1.25.2 中文文档"' "$content_dir/pgbouncer/_index.zh.md"
grep -Fq 'title: "pgBadger 13.2 Documentation"' "$content_dir/pgbadger/_index.md"
grep -Fq 'title: "pgBadger 13.2 中文文档"' "$content_dir/pgbadger/_index.zh.md"
grep -Fq 'title: "HAProxy 3.4.3 Documentation"' "$content_dir/haproxy/_index.md"

python3 "$project_dir/scripts/check-bilingual-parity.py"

hugo --source "$project_dir" --destination "$build_dir/public" --gc --minify --cleanDestinationDir --printPathWarnings --panicOnWarning

for page in \
  index.html \
  zh/index.html \
  search/index.html \
  zh/search/index.html \
  attribution/index.html \
  zh/attribution/index.html \
  patroni/index.html \
  zh/patroni/index.html \
  pgbackrest/index.html \
  zh/pgbackrest/index.html \
  pgbouncer/index.html \
  zh/pgbouncer/index.html \
  pgbadger/index.html \
  zh/pgbadger/index.html \
  haproxy/index.html \
  haproxy/load-balancing/index.html \
  haproxy/http-fundamentals/index.html \
  haproxy/proxies/index.html \
  haproxy/acls-and-samples/index.html \
  haproxy/prerequisites/index.html \
  haproxy/statistics-and-monitoring/index.html \
  haproxy/security/index.html \
  etcd/index.html \
  etcd/quickstart/index.html \
  etcd/op-guide/configuration/index.html \
  etcd/upgrades/upgrade_3_7/index.html \
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
  pgbadger/index.md \
  zh/pgbadger/index.md \
  haproxy/index.md \
  haproxy/proxies/index.md \
  haproxy/statistics-and-monitoring/index.md \
  etcd/index.md \
  etcd/quickstart/index.md \
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
  llms.txt; do
  test -s "$build_dir/public/$page"
done

while IFS= read -r source_file; do
  relative=${source_file#"$content_dir/"}
  if [[ $(basename "$relative") == '_index.md' ]]; then
    route=${relative%/_index.md}
  else
    route=${relative%.md}
  fi
  test -s "$build_dir/public/$route/index.html"
done < <(find "$content_dir/haproxy" -maxdepth 1 -type f -name '*.md' ! -name '*.zh.md' ! -name '_div_*.md' | sort)

while IFS= read -r source_file; do
  relative=${source_file#"$content_dir/"}
  if [[ $relative == *.zh.md ]]; then
    legacy_route="zh/docs/${relative%.zh.md}"
  else
    legacy_route="docs/${relative%.md}"
  fi
  legacy_route=${legacy_route%/_index}
  test -s "$build_dir/public/$legacy_route/index.html"
done < <(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger,haproxy} -type f -name '*.md' ! -name '_div_*.md' | sort)

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
test "$(tr -d '\r\n' < "$project_dir/sources/haproxy/upstream/VERSION")" = '3.4.3'
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

printf 'Validated OINK v0.6.0, six top-level component roots, %s paired EN/ZH pages, %s HAProxy reading pages, %s etcd Markdown pages, and legacy redirects.\n' \
  "$english_count" "$haproxy_reading_count" "$etcd_markdown_count"
