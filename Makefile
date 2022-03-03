UPDATE_DEPS = app
INSTALL_DEPS = app

.PHONY: tests

tests:
	@docker-compose run --rm tests

update-deps-dev:
	$(foreach app,$(UPDATE_DEPS),pip-compile --upgrade --rebuild --generate-hashes --allow-unsafe --no-emit-index-url $(app)/requirements/dev.in --output-file $(app)/requirements/dev.txt;)
update-deps-prod:
	$(foreach app,$(UPDATE_DEPS),pip-compile --upgrade --rebuild --generate-hashes --allow-unsafe --no-emit-index-url $(app)/requirements/production.in --output-file $(app)/requirements/production.txt;)
update-deps-all: update-deps-dev update-deps-prod

install-deps-dev:
	$(foreach app,$(INSTALL_DEPS),pip install -r $(app)/requirements/dev.txt;)
install-deps-prod:
	$(foreach app,$(INSTALL_DEPS),pip install -r $(app)/requirements/production.txt;)

