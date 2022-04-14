TESTS=tests
PACKAGE=env_var
ALL_PACKAGES=${PACKAGE} ${TESTS}
POETRY_CMD ?= poetry run

# sphinx vars
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = build

.PHONY: docs
docs:
	@$(POETRY_CMD) $(SPHINXBUILD) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: format
format: sort_imports
	$(POETRY_CMD) black ${ALL_PACKAGES}

.PHONY: sort_imports
sort_imports:
	$(POETRY_CMD) isort ${ALL_PACKAGES}

.PHONY: test
test:
	$(POETRY_CMD) pytest --cov-report term-missing --cov=${PACKAGE} ${TESTS}

.PHONY: lint
lint:
	$(POETRY_CMD) pylint ${PACKAGE}