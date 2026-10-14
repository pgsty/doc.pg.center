#!/usr/bin/env bash
set -euo pipefail

project_dir=$(cd "$(dirname "$0")/.." && pwd)
build_dir=$(mktemp -d "${TMPDIR:-/tmp}/doc-pg-center-check.XXXXXX")
trap 'rm -rf "$build_dir"' EXIT
export PYTHONPYCACHEPREFIX="$build_dir/python-cache"
export HUGO_RESOURCEDIR="$build_dir/resources"
export HUGO_CACHEDIR="${HUGO_CACHEDIR:-$build_dir/cache}"
export GOWORK=off HUGO_MODULE_WORKSPACE=off
unset HUGO_MODULE_REPLACEMENTS

python3 "$project_dir/scripts/check-content.py"
python3 "$project_dir/scripts/report-coverage.py"
make -C "$project_dir" build HUGO="${HUGO:-hugo}" DESTINATION="$build_dir/public"

python3 - "$project_dir" "$build_dir/public" <<'PYTHON'
from pathlib import Path
from html.parser import HTMLParser
import json
import sys

project, public = map(Path, sys.argv[1:])
languages = ("en", "zh", "fr", "ja", "de", "ru")
components = ("patroni", "pgbackrest", "pgbouncer", "pgbadger", "haproxy", "etcd")

class HeadAndLinks(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.canonical = ""
        self.links = set()
        self.footer_links = set()
        self.in_footer = False
        self.fallbacks = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "footer":
            self.in_footer = True
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href", "")
        if tag == "a":
            self.links.add(attrs.get("href", ""))
            if self.in_footer:
                self.footer_links.add(attrs.get("href", ""))
            if "data-fallback-language" in attrs:
                self.fallbacks.append(attrs)

    def handle_endtag(self, tag):
        if tag == "footer":
            self.in_footer = False

for language in languages:
    prefix = "" if language == "en" else language + "/"
    for route in ("", "search/", "attribution/"):
        page = public / prefix / route / "index.html"
        assert page.is_file() and page.stat().st_size, page
        html = page.read_text()
        parsed = HeadAndLinks(html)
        assert parsed.canonical == "https://doc.pg.center/" + prefix + route, page
        assert "G-D9E4B60JWX" in html, f"Shared production analytics missing: {page}"
        assert "PIG.CENTER" not in html, f"Obsolete site name: {page}"
        assert "https://github.com/pgsty/doc.pg.center" in parsed.footer_links, page
        assert f"/{prefix}attribution/" in parsed.footer_links, page
    home = HeadAndLinks((public / prefix / "index.html").read_text())
    assert not home.fallbacks, f"Unexpected English fallback on {language} home"
    for component in components:
        assert f"/{prefix}{component}/" in home.links, (language, component)
        assert f"/{prefix}{component}/" in home.footer_links, (language, component)
    parent = "https://pg.center/zh/" if language == "zh" else "https://pg.center/"
    assert parent in home.footer_links, f"Parent site missing from {language} footer"
    for output in ("index.md", "llms.txt", "navigation.json"):
        path = public / prefix / output
        assert path.is_file() and path.stat().st_size, path
    json.loads((public / prefix / "navigation.json").read_text())
    for divider in ("intro", "configuration", "management"):
        assert not (public / prefix / f"haproxy/_div_{divider}/index.html").exists()

# All published static assets, including third-party notices and sample reports,
# must survive the build unchanged.
for source in (project / "static").rglob("*"):
    if source.is_file():
        target = public / source.relative_to(project / "static")
        assert target.is_file() and target.read_bytes() == source.read_bytes(), target

assert "https://doc.pg.center/images/og-doc-pg-center.png" in (public / "index.html").read_text()
assert "/images/og-doc-pg-center.png" not in (public / "patroni/index.html").read_text()
print("Validated localized landing pages, canonical URLs, navigation, alternate outputs, and static assets.")
PYTHON

python3 "$project_dir/scripts/check-docs-routes.py" "$build_dir/public"
python3 "$project_dir/scripts/check-local-links.py" "$build_dir/public"
node "$project_dir/scripts/check-russian-search.cjs" "$build_dir/public"
node "$project_dir/scripts/test-pgbackrest-search.cjs" "$build_dir/public"
printf 'Site checks passed for all six languages.\n'
