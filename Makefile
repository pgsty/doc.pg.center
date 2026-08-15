HUGO ?= hugo
BIND ?= 127.0.0.1
PORT ?= 1313

.PHONY: build check dev

build:
	$(HUGO) --gc --minify --cleanDestinationDir --printPathWarnings

dev:
	$(HUGO) server --bind "$(BIND)" --port "$(PORT)" --disableFastRender --renderToMemory --cleanDestinationDir --environment dev

check:
	./scripts/check-site.sh
