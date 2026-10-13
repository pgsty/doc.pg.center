#!/usr/bin/env bash
set -euo pipefail

project_dir=$(cd "$(dirname "$0")/.." && pwd)
snapshot_dir="$project_dir/sources/haproxy"
license_dir="$project_dir/static/third_party/haproxy"
upstream_tag=v3.4.4
upstream_commit=7f03ae65c28605152c7a1a9ba7d9d0bcfb50f8b0
work_dir=$(mktemp -d "${TMPDIR:-/tmp}/pig-center-haproxy.XXXXXX")

trap 'rm -rf "$work_dir"' EXIT

if [[ -e "$snapshot_dir/upstream" ]]; then
  echo "HAProxy snapshot already exists; refusing to overwrite it." >&2
  exit 1
fi

mkdir -p "$work_dir/upstream"

curl_args=(--fail --location --silent --show-error --retry 2 --connect-timeout 15 --max-time 240)
github_raw="https://raw.githubusercontent.com/haproxy/haproxy/$upstream_commit"

fetch_source() {
  local source_path=$1
  local output_name=$2
  curl "${curl_args[@]}" \
    "$github_raw/$source_path" \
    --output "$work_dir/upstream/$output_name"
}

fetch_source doc/intro.txt intro.txt
fetch_source doc/configuration.txt configuration.txt
fetch_source doc/management.txt management.txt
fetch_source LICENSE LICENSE
fetch_source doc/gpl.txt GPL-2.0
fetch_source VERSION VERSION
fetch_source VERDATE VERDATE

test "$(tr -d '\r\n' < "$work_dir/upstream/VERSION")" = '3.4.4'
grep -Fq 'HAProxy Starter Guide' "$work_dir/upstream/intro.txt"
grep -Fq 'version 3.4' "$work_dir/upstream/intro.txt"
grep -Fq 'Configuration Manual' "$work_dir/upstream/configuration.txt"
grep -Fq 'HAProxy Management Guide' "$work_dir/upstream/management.txt"
grep -Fq 'GNU GENERAL PUBLIC LICENSE' "$work_dir/upstream/GPL-2.0"

mkdir -p "$snapshot_dir/upstream" "$license_dir"
cp "$work_dir/upstream/"* "$snapshot_dir/upstream/"
cp "$work_dir/upstream/LICENSE" "$license_dir/LICENSE"
cp "$work_dir/upstream/GPL-2.0" "$license_dir/GPL-2.0"

(
  cd "$snapshot_dir"
  shasum -a 256 upstream/* > SHA256SUMS
)

printf 'Imported the complete HAProxy %s core manual set at %s.\n' \
  "$upstream_tag" "$upstream_commit"
