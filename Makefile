HUGO ?= hugo
BIND ?= 127.0.0.1
PORT ?= 1313

.PHONY: build check dev serve

build:
	$(HUGO) --gc --minify --cleanDestinationDir --printPathWarnings

dev:
	HUGO_MODULE_REPLACEMENTS='github.com/pgsty/oink -> $(abspath ../oink)' \
		$(HUGO) server --bind "$(BIND)" --port "$(PORT)" --renderToMemory

serve:
	$(HUGO) server --bind "$(BIND)" --port "$(PORT)" --environment production \
		--minify --disableFastRender --disableLiveReload

check:
	./scripts/check-site.sh
