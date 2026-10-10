UV ?= uv
COMMENT_FUZZ_SEED ?= 0xC0FFEE
COMMENT_FUZZ_CASES_PER_LANGUAGE ?= 100
COMMENT_FUZZ_MAX_LENGTH ?= 128
COMMENT_FUZZ_SANITIZER_PAYLOADS_PER_EXAMPLE ?= 4

.PHONY: setup setup-optional test test-optional lint smoke build docs docs-serve
.PHONY: comment-cleaner-fixtures comment-fuzz comment-cleaner-fuzz
.PHONY: check-main-branch check-release-version

setup:
	$(UV) sync --group dev

setup-optional:
	$(UV) sync --group dev --extra treesitter --extra datasets

test:
	$(UV) run pytest -m "not optional_dependency"

test-optional:
	$(UV) run pytest -m "optional_dependency" --no-cov

lint:
	$(UV) run ruff check src tests examples
	$(UV) run ruff format --check src tests examples scripts

smoke:
	$(UV) run pytest tests/test_smoke.py -q --no-cov

build:
	$(UV) build

docs:
	$(UV) run --group docs mkdocs build --strict

docs-serve:
	$(UV) run --group docs mkdocs serve

comment-cleaner-fixtures:
	$(UV) run python scripts/build_comment_cleaning_fixtures.py --force

comment-fuzz:
	$(UV) run python scripts/fuzz_comment_parsers.py \
		--seed $(COMMENT_FUZZ_SEED) \
		--cases-per-language $(COMMENT_FUZZ_CASES_PER_LANGUAGE) \
		--max-length $(COMMENT_FUZZ_MAX_LENGTH) \
		--sanitizer-payloads-per-example $(COMMENT_FUZZ_SANITIZER_PAYLOADS_PER_EXAMPLE) \
		--campaign all

comment-cleaner-fuzz:
	$(UV) run python scripts/fuzz_comment_parsers.py \
		--seed $(COMMENT_FUZZ_SEED) \
		--cases-per-language $(COMMENT_FUZZ_CASES_PER_LANGUAGE) \
		--max-length $(COMMENT_FUZZ_MAX_LENGTH) \
		--sanitizer-payloads-per-example $(COMMENT_FUZZ_SANITIZER_PAYLOADS_PER_EXAMPLE) \
		--campaign sanitizer

check-main-branch:
	python scripts/check_main_branch_policy.py

check-release-version:
	python scripts/check_release_version.py
