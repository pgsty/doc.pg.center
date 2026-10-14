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
import struct
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
        self.home_links = []
        self.icons = set()
        self.site_name = ""
        self.title = ""
        self.in_title = False
        self.logos = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "footer":
            self.in_footer = True
        if tag == "title":
            self.in_title = True
        if tag == "meta" and attrs.get("property") == "og:site_name":
            self.site_name = attrs.get("content", "")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href", "")
        if tag == "link" and attrs.get("rel") in ("icon", "apple-touch-icon"):
            self.icons.add(attrs.get("href", ""))
        if tag == "img":
            self.logos.append(attrs.get("src", ""))
        if tag == "a":
            self.links.add(attrs.get("href", ""))
            if attrs.get("data-td-navbar-id") == "home":
                self.home_links.append(attrs)
            if self.in_footer:
                self.footer_links.add(attrs.get("href", ""))
            if "data-fallback-language" in attrs:
                self.fallbacks.append(attrs)

    def handle_endtag(self, tag):
        if tag == "footer":
            self.in_footer = False
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data

for language in languages:
    prefix = "" if language == "en" else language + "/"
    parent = "https://pg.center/zh/" if language == "zh" else "https://pg.center/"
    for route in ("", "search/", "attribution/", *(component + "/" for component in components)):
        page = public / prefix / route / "index.html"
        assert page.is_file() and page.stat().st_size, page
        html = page.read_text()
        parsed = HeadAndLinks(html)
        assert parsed.canonical == "https://doc.pg.center/" + prefix + route, page
        assert parsed.title.endswith("PG.CENTER") and "doc.pg.center" not in parsed.title, page
        assert parsed.site_name == "PG.CENTER", page
        assert "/img/slonik.svg" in parsed.logos, f"PostgreSQL brand logo missing: {page}"
        assert parsed.home_links and all(
            link.get("href") == parent and "target" not in link
            for link in parsed.home_links
        ), f"Incorrect parent Home navigation: {page}"
        assert parsed.icons == {
            "/favicon.ico", "/favicon.svg", "/favicon-32x32.png",
            "/favicon-256x256.png", "/apple-touch-icon.png",
        }, f"Incorrect PostgreSQL icon set: {page}"
        assert "G-D9E4B60JWX" in html, f"Shared production analytics missing: {page}"
        assert "PIG.CENTER" not in html, f"Obsolete site name: {page}"
        assert "https://github.com/pgsty/doc.pg.center" in parsed.footer_links, page
        assert f"/{prefix}attribution/" in parsed.footer_links, page
    home = HeadAndLinks((public / prefix / "index.html").read_text())
    assert not home.fallbacks, f"Unexpected English fallback on {language} home"
    for component in components:
        assert f"/{prefix}{component}/" in home.links, (language, component)
        assert f"/{prefix}{component}/" in home.footer_links, (language, component)
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

assert "https://doc.pg.center/images/postgresql.png" in (public / "index.html").read_text()
assert "/images/postgresql.png" not in (public / "patroni/index.html").read_text()
assert (public / "favicon.svg").read_bytes() == (public / "img/slonik.svg").read_bytes()
for filename, size in (("favicon-32x32.png", 32), ("favicon-256x256.png", 256), ("apple-touch-icon.png", 256)):
    png = (public / filename).read_bytes()
    assert png.startswith(b"\x89PNG\r\n\x1a\n") and struct.unpack_from(">II", png, 16) == (size, size), filename
for obsolete in ("favicon-192x192.png", "favicon-512x512.png", "images/og-doc-pg-center.png"):
    assert not (public / obsolete).exists(), obsolete
print("Validated PG.CENTER branding, PostgreSQL icons, localized Home navigation, canonical URLs, alternate outputs, and static assets.")
PYTHON

python3 "$project_dir/scripts/check-docs-routes.py" "$build_dir/public"
python3 "$project_dir/scripts/check-local-links.py" "$build_dir/public"
node "$project_dir/scripts/check-russian-search.cjs" "$build_dir/public"
node "$project_dir/scripts/test-pgbackrest-search.cjs" "$build_dir/public"
printf 'Site checks passed for all six languages.\n'
