HUGO ?= hugo
BIND ?= 127.0.0.1
PORT ?= 1313
DESTINATION ?= public
OINK_DIR ?= $(HOME)/pgsty/oink
OINK_LOCAL ?= $(OINK_DIR)

export GOWORK = off
export HUGO_MODULE_WORKSPACE = off

.PHONY: build check dev serve

build:
	env -u HUGO_MODULE_REPLACEMENTS $(HUGO) --environment production \
		--destination "$(DESTINATION)" --gc --minify --cleanDestinationDir \
		--printPathWarnings --panicOnWarning --noBuildLock

dev: theme-local
	HUGO_MODULE_REPLACEMENTS='github.com/pgsty/oink -> $(abspath $(OINK_LOCAL))' \
		$(HUGO) server --ignoreVendorPaths=github.com/pgsty/oink --bind "$(BIND)" --port "$(PORT)" --renderToMemory --noBuildLock

serve:
	env -u HUGO_MODULE_REPLACEMENTS $(HUGO) server --bind "$(BIND)" \
		--port "$(PORT)" --environment production --minify --disableFastRender \
		--disableLiveReload --renderToMemory --noBuildLock

check:
	HUGO="$(HUGO)" ./scripts/check-site.sh

# Fail explicitly if a local theme was requested but is unavailable.
theme-local:
	@test -f "$(OINK_LOCAL)/hugo.yaml" || { echo "Set OINK_LOCAL to an OINK checkout (default: ~/pgsty/oink)." >&2; exit 1; }

.PHONY: theme-local
