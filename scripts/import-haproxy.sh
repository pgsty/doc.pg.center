#!/usr/bin/env bash
set -euo pipefail

project_dir=$(cd "$(dirname "$0")/.." && pwd)
snapshot_dir="$project_dir/sources/haproxy"
license_dir="$project_dir/static/third_party/haproxy"
read -r upstream_tag upstream_commit upstream_release upstream_doc_version < <(
  python3 - "$snapshot_dir/SNAPSHOT.json" <<'PY'
import json, sys
snapshot = json.load(open(sys.argv[1]))
print(snapshot['stable_tag'], snapshot['documentation_commit'], snapshot['stable_release'], snapshot['documentation_version'])
PY
)
refresh=false
if [[ $# -gt 0 ]]; then
  if [[ $# -eq 1 && "$1" = --refresh ]]; then
    refresh=true
  else
    echo "Usage: $0 [--refresh]" >&2
    exit 2
  fi
fi
work_dir=$(mktemp -d "${TMPDIR:-/tmp}/doc-pg-center-haproxy.XXXXXX")

trap 'rm -rf "$work_dir"' EXIT

if [[ -e "$snapshot_dir/upstream" && "$refresh" = false ]]; then
  echo "HAProxy snapshot already exists; use --refresh for an authorized pinned-source update." >&2
  exit 1
fi

mkdir -p "$work_dir/upstream"

curl_args=(--fail --location --silent --show-error --retry 2 --connect-timeout 15 --max-time 240)
official_git="https://git.haproxy.org/?p=haproxy-3.4.git;a=blob_plain"

fetch_source() {
  local source_path=$1
  local output_name=$2
  curl "${curl_args[@]}" \
    "$official_git;f=$source_path;hb=$upstream_commit" \
    --output "$work_dir/upstream/$output_name"
}

fetch_source doc/intro.txt intro.txt
fetch_source doc/configuration.txt configuration.txt
fetch_source doc/management.txt management.txt
fetch_source LICENSE LICENSE
fetch_source doc/gpl.txt GPL-2.0
fetch_source VERSION VERSION
fetch_source VERDATE VERDATE

test "$(tr -d '\r\n' < "$work_dir/upstream/VERSION")" = "$upstream_release"
grep -Fq 'HAProxy Starter Guide' "$work_dir/upstream/intro.txt"
grep -Fq 'version 3.4' "$work_dir/upstream/intro.txt"
grep -Fq 'Configuration Manual' "$work_dir/upstream/configuration.txt"
grep -Fq 'HAProxy Management Guide' "$work_dir/upstream/management.txt"
grep -Fq 'GNU GENERAL PUBLIC LICENSE' "$work_dir/upstream/GPL-2.0"
python3 - "$snapshot_dir/SNAPSHOT.json" "$work_dir/upstream" <<'PY'
import hashlib, json, pathlib, sys
snapshot = json.load(open(sys.argv[1]))
directory = pathlib.Path(sys.argv[2])
expected = {'intro.txt', 'configuration.txt', 'management.txt', 'LICENSE', 'GPL-2.0', 'VERSION', 'VERDATE'}
if len(snapshot['files']) != 7 or {entry['file'] for entry in snapshot['files']} != expected:
    raise SystemExit('Pinned snapshot must identify all seven source files exactly once')
for entry in snapshot['files']:
    actual = hashlib.sha256((directory / entry['file']).read_bytes()).hexdigest()
    if actual != entry['sha256']:
        raise SystemExit('Pinned source checksum mismatch: ' + entry['file'])
print('All seven downloads match the pinned English snapshot.')
PY

mkdir -p "$snapshot_dir/upstream" "$license_dir"
cp "$work_dir/upstream/"* "$snapshot_dir/upstream/"
cp "$work_dir/upstream/LICENSE" "$license_dir/LICENSE"
cp "$work_dir/upstream/GPL-2.0" "$license_dir/GPL-2.0"

(
  cd "$snapshot_dir"
  shasum -a 256 upstream/* > SHA256SUMS
)

printf 'Imported the complete HAProxy %s core manual set at %s.\n' \
  "$upstream_doc_version" "$upstream_commit"
