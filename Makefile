HUGO ?= hugo
BIND ?= 127.0.0.1
PORT ?= 1313
DESTINATION ?= public

export GOWORK = off
export HUGO_MODULE_WORKSPACE = off

.PHONY: build check dev serve

build:
	env -u HUGO_MODULE_REPLACEMENTS $(HUGO) --environment production \
		--destination "$(DESTINATION)" --gc --minify --cleanDestinationDir \
		--printPathWarnings --panicOnWarning --noBuildLock

dev:
	HUGO_MODULE_REPLACEMENTS='github.com/pgsty/oink -> $(abspath ../oink)' \
		$(HUGO) server --bind "$(BIND)" --port "$(PORT)" --renderToMemory

serve:
	env -u HUGO_MODULE_REPLACEMENTS $(HUGO) server --bind "$(BIND)" \
		--port "$(PORT)" --environment production --minify --disableFastRender \
		--disableLiveReload --renderToMemory --noBuildLock

check:
	HUGO="$(HUGO)" ./scripts/check-site.sh
