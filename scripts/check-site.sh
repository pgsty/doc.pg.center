#!/usr/bin/env bash
set -euo pipefail

project_dir=$(cd "$(dirname "$0")/.." && pwd)
content_dir="$project_dir/content/docs"
build_dir=$(mktemp -d "${TMPDIR:-/tmp}/pgsql-cc-check.XXXXXX")
trap 'rm -rf "$build_dir"' EXIT

expected=78
english_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger} -type f -name '*.md' ! -name '*.zh.md' | wc -l | tr -d ' ')
chinese_count=$(find "$content_dir"/{patroni,pgbackrest,pgbouncer,pgbadger} -type f -name '*.zh.md' | wc -l | tr -d ' ')

test "$english_count" -eq "$expected"
test "$chinese_count" -eq "$expected"

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

if rg -n '\]\(/docs/(patroni|pgbackrest|pgbouncer|pgbadger)' "$content_dir" -g '*.zh.md'; then
  echo 'Chinese content contains an English-locale component link' >&2
  exit 1
fi

grep -Eq '^require github\.com/pgsty/oink v0\.4\.1$' "$project_dir/go.mod"

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

python3 "$project_dir/scripts/check-bilingual-parity.py"

hugo --source "$project_dir" --destination "$build_dir/public" --gc --minify --cleanDestinationDir --printPathWarnings --panicOnWarning

for page in \
  index.html \
  zh/index.html \
  search/index.html \
  zh/search/index.html \
  docs/patroni/index.html \
  zh/docs/patroni/index.html \
  docs/pgbackrest/index.html \
  zh/docs/pgbackrest/index.html \
  docs/pgbouncer/index.html \
  zh/docs/pgbouncer/index.html \
  docs/pgbadger/index.html \
  zh/docs/pgbadger/index.html \
  docs/pgbadger/command-line/index.html \
  zh/docs/pgbadger/command-line/index.html \
  docs/pgbadger/releases/13/index.html \
  zh/docs/pgbadger/releases/13/index.html \
  blog/releases/pgsql-cc-first-edition/index.html \
  zh/blog/releases/pgsql-cc-first-edition/index.html \
  docs/patroni/index.md \
  zh/docs/patroni/index.md \
  _print/docs/patroni/index.html \
  _print/docs/pgbackrest/index.html \
  _print/docs/pgbouncer/index.html \
  _print/docs/pgbadger/index.html \
  zh/_print/docs/patroni/index.html \
  zh/_print/docs/pgbackrest/index.html \
  zh/_print/docs/pgbouncer/index.html \
  zh/_print/docs/pgbadger/index.html \
  docs/pgbadger/index.md \
  zh/docs/pgbadger/index.md \
  third_party/pgbadger/examples/sample.html \
  third_party/pgbadger/examples/errors.html \
  third_party/pgbadger/examples/report/index.html \
  third_party/pgbadger/LICENSE \
  third_party/pgbadger/THIRD-PARTY-LICENSES \
  img/docs/pgbadger/logo.png \
  images/og.png \
  CNAME \
  favicon.ico \
  zh/llms.txt \
  llms.txt; do
  test -s "$build_dir/public/$page"
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

(cd "$project_dir/sources/pgbadger" && shasum -a 256 -c SHA256SUMS >/dev/null)

grep -q 'https://pgsql.cc/images/og.png' "$build_dir/public/index.html"
grep -q 'https://pgsql.cc/images/og.png' "$build_dir/public/zh/index.html"
if grep -q '/images/og.png' "$build_dir/public/docs/patroni/index.html"; then
  echo 'A detail page inherited the homepage social image' >&2
  exit 1
fi

python3 "$project_dir/scripts/check-local-links.py" "$build_dir/public"

printf 'Validated OINK v0.4.1, %s EN pages, %s ZH pages, and required rendered routes.\n' "$english_count" "$chinese_count"
