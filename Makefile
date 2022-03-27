TESTS=tests
PACKAGE=env_var
ALL_PACKAGES=${PACKAGE} ${TESTS}

# sphinx vars
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = build

.PHONY: docs
docs:
	@$(SPHINXBUILD) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: format
format: sort_imports
	black ${ALL_PACKAGES}

.PHONY: sort_imports
sort_imports:
	isort ${ALL_PACKAGES}

.PHONY: test
test:
	pytest --cov-report term-missing --cov=${PACKAGE} ${TESTS}

.PHONY: lint
lint:
	pylint ${PACKAGE}