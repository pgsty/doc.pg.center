#!/usr/bin/env bash
set -euo pipefail

project_dir=$(cd "$(dirname "$0")/.." && pwd)
snapshot_dir="$project_dir/sources/pgbadger"
example_dir="$project_dir/static/third_party/pgbadger/examples"
logo_dir="$project_dir/static/img/docs/pgbadger"
upstream_commit=a1ad95a035a0c2d246fe632eb1c361d4bde0ddae
upstream_archive_sha256=4c708efdcea2c5953c35d064be7a29fe4da23467c9accfef7f7a82da5fc6dc4c
work_dir=$(mktemp -d "${TMPDIR:-/tmp}/doc-pg-center-pgbadger.XXXXXX")

trap 'rm -rf "$work_dir"' EXIT

if [[ -e "$snapshot_dir" || -e "$example_dir" ]]; then
  echo "pgBadger snapshot already exists; refusing to overwrite it." >&2
  exit 1
fi

mkdir -p \
  "$work_dir/site/rsc" \
  "$work_dir/site/examples/report" \
  "$snapshot_dir/site/rsc" \
  "$snapshot_dir/upstream" \
  "$example_dir" \
  "$logo_dir"

curl_args=(--fail --location --silent --show-error --retry 2 --connect-timeout 15 --max-time 240)

curl "${curl_args[@]}" https://pgbadger.darold.net/index.html \
  --output "$work_dir/site/index.html"
curl "${curl_args[@]}" https://pgbadger.darold.net/documentation.html \
  --output "$work_dir/site/documentation.html"
curl "${curl_args[@]}" https://pgbadger.darold.net/sitemap.xml \
  --output "$work_dir/site/sitemap.xml"
curl "${curl_args[@]}" https://pgbadger.darold.net/logo_pgbadger.png \
  --output "$work_dir/site/logo_pgbadger.png"

for asset in bootstrap.css pgbadger_style.css jquery-3.js bootstrap.js; do
  curl "${curl_args[@]}" "https://pgbadger.darold.net/rsc/$asset" \
    --output "$work_dir/site/rsc/$asset"
done

curl "${curl_args[@]}" --compressed \
  https://pgbadger.darold.net/examples/sample.html \
  --output "$work_dir/site/examples/sample.html"
curl "${curl_args[@]}" --compressed \
  https://pgbadger.darold.net/examples/errors.html \
  --output "$work_dir/site/examples/errors.html"

report_root="$work_dir/site/examples/report/pgbadger.darold.net/examples/report"
mkdir -p "$report_root/11"

report_pages=(
  index.html
  2012/week-49/index.html
  2012/week-50/index.html
  2012/12/06/index.html
  2012/12/07/index.html
  2012/12/08/index.html
  2012/12/09/index.html
  2012/12/10/index.html
  2012/12/11/index.html
  2012/12/12/index.html
)

report_assets=(
  jquery.jqplot.min.css
  bootstrap.min.css
  fontawesome.min.css
  pgbadger.min.css
  bean.min.js
  bootstrap.min.js
  jqplot.barRenderer.min.js
  jqplot.canvasAxisTickRenderer.min.js
  jqplot.canvasTextRenderer.min.js
  jqplot.categoryAxisRenderer.min.js
  jqplot.cursor.min.js
  jqplot.dateAxisRenderer.min.js
  jqplot.highlighter.min.js
  jqplot.pieRenderer.min.js
  jqplot.pointLabels.min.js
  jquery.jqplot.min.js
  jquery.min.js
  pgbadger_slide.min.js
  pgbadger.min.js
  underscore.min.js
)

download_count=0
for page in "${report_pages[@]}"; do
  mkdir -p "$(dirname "$report_root/$page")"
  curl "${curl_args[@]}" --compressed \
    "https://pgbadger.darold.net/examples/report/$page" \
    --output "$report_root/$page" &
  ((download_count += 1))
  if ((download_count % 5 == 0)); then
    wait
  fi
done

for asset in "${report_assets[@]}"; do
  curl "${curl_args[@]}" --compressed \
    "https://pgbadger.darold.net/examples/report/11/$asset" \
    --output "$report_root/11/$asset" &
  ((download_count += 1))
  if ((download_count % 5 == 0)); then
    wait
  fi
done
wait

archive="$work_dir/pgbadger-$upstream_commit.tar.gz"
curl "${curl_args[@]}" \
  "https://codeload.github.com/darold/pgbadger/tar.gz/$upstream_commit" \
  --output "$archive"
printf '%s  %s\n' "$upstream_archive_sha256" "$archive" | shasum -a 256 -c - >/dev/null
tar -xzf "$archive" -C "$work_dir"
upstream_dir="$work_dir/pgbadger-$upstream_commit"

cp "$work_dir/site/index.html" "$snapshot_dir/site/index.html"
cp "$work_dir/site/documentation.html" "$snapshot_dir/site/documentation.html"
cp "$work_dir/site/sitemap.xml" "$snapshot_dir/site/sitemap.xml"
cp "$work_dir/site/logo_pgbadger.png" "$snapshot_dir/site/logo_pgbadger.png"
cp "$work_dir/site/rsc/"* "$snapshot_dir/site/rsc/"

cp "$upstream_dir/README.md" "$snapshot_dir/upstream/README.md"
cp "$upstream_dir/ChangeLog" "$snapshot_dir/upstream/ChangeLog"
cp "$upstream_dir/CONTRIBUTING.md" "$snapshot_dir/upstream/CONTRIBUTING.md"
cp "$upstream_dir/LICENSE" "$snapshot_dir/upstream/LICENSE"
cp "$upstream_dir/resources/LICENSE" "$snapshot_dir/upstream/RESOURCE-LICENSES"
cp "$upstream_dir/doc/pgBadger.pod" "$snapshot_dir/upstream/pgBadger.pod"

cp "$work_dir/site/examples/sample.html" "$example_dir/sample.html"
cp "$work_dir/site/examples/errors.html" "$example_dir/errors.html"
cp -R \
  "$work_dir/site/examples/report/pgbadger.darold.net/examples/report" \
  "$example_dir/report"
cp "$work_dir/site/logo_pgbadger.png" "$logo_dir/logo.png"
cp "$upstream_dir/LICENSE" "$project_dir/static/third_party/pgbadger/LICENSE"
cp "$upstream_dir/resources/LICENSE" \
  "$project_dir/static/third_party/pgbadger/THIRD-PARTY-LICENSES"

echo "Imported pgBadger website and source snapshot at $upstream_commit."
