UV ?= uv
COMMENT_JUDGE_LANGUAGES ?= python,java,coffeescript
COMMENT_JUDGE_PER_KIND ?= 10
COMMENT_JUDGE_OUTPUT_ROOT ?= tmp/stack_v2_comment_judge
COMMENT_JUDGE_MANIFEST ?= $(COMMENT_JUDGE_OUTPUT_ROOT)/manifest.jsonl
COMMENT_JUDGE_FAILURES ?= $(COMMENT_JUDGE_OUTPUT_ROOT)/failures.jsonl
COMMENT_JUDGE_REPORT_DIR ?= $(COMMENT_JUDGE_OUTPUT_ROOT)/reports
COMMENT_JUDGE_LEDGER ?= docs/comment_testing/stack_v2_judge_validation_ledger.md
COMMENT_JUDGE_FORCE ?= 0
COMMENT_JUDGE_CODEX_TIMEOUT ?= 180
COMMENT_JUDGE_TIMEOUT ?= 240
COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE ?= 88
COMMENT_JUDGE_PROGRESS_EVERY ?= 10
COMMENT_JUDGE_CASE_LIMIT ?=
COMMENT_JUDGE_MANIFEST_ARGS ?=
COMMENT_TESTGEN_CODEX_TIMEOUT ?= 600
COMMENT_TESTGEN_CODEX_SANDBOX ?= workspace-write
COMMENT_TESTGEN_REPORT_LIMIT ?=
COMMENT_TESTGEN_REPORTS ?=

.PHONY: setup setup-optional test test-optional lint smoke build research-prompts comment-test-prompts
.PHONY: comment-judge-manifest comment-judge-smoke comment-judge-test
.PHONY: comment-judge-generate-tests comment-judge-testgen-pipeline check-main-branch check-release-version

setup:
	$(UV) sync --group dev

setup-optional:
	$(UV) sync --group dev --extra treesitter

test:
	$(UV) run pytest -m "not optional_dependency"

test-optional:
	$(UV) run pytest -m "optional_dependency" --no-cov

lint:
	$(UV) run ruff check src tests examples

smoke:
	$(UV) run pytest tests/test_smoke.py -q --no-cov

build:
	$(UV) build

research-prompts:
	$(UV) run python scripts/build_comment_research_packets.py

comment-test-prompts:
	$(UV) run python scripts/build_comment_test_packets.py

comment-judge-manifest:
	$(UV) run --with boto3 --with 'smart_open[s3]' \
		python scripts/build_stack_v2_comment_judge_cases.py \
		--languages $(COMMENT_JUDGE_LANGUAGES) \
		--per-kind $(COMMENT_JUDGE_PER_KIND) \
		--progress-every $(COMMENT_JUDGE_PROGRESS_EVERY) \
		--fetch-stack-v2-content \
		--output-root $(COMMENT_JUDGE_OUTPUT_ROOT) $(COMMENT_JUDGE_MANIFEST_ARGS)

comment-judge-smoke:
	STACK_V2_COMMENT_JUDGE_MANIFEST=$(COMMENT_JUDGE_MANIFEST) \
		STACK_V2_COMMENT_JUDGE_FAILURES=$(COMMENT_JUDGE_FAILURES) \
		STACK_V2_COMMENT_JUDGE_REPORT_DIR=$(COMMENT_JUDGE_REPORT_DIR) \
		COMMENT_JUDGE_LEDGER=$(COMMENT_JUDGE_LEDGER) \
		COMMENT_JUDGE_FORCE=$(COMMENT_JUDGE_FORCE) \
		COMMENT_JUDGE_USE_CODEX=1 \
		COMMENT_JUDGE_CASE_LIMIT=1 \
		COMMENT_JUDGE_CODEX_TIMEOUT=$(COMMENT_JUDGE_CODEX_TIMEOUT) \
		COMMENT_JUDGE_TIMEOUT=$(COMMENT_JUDGE_TIMEOUT) \
		COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE=$(COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE) \
		$(UV) run pytest tests/test_stack_v2_comment_judge.py -q --no-cov

comment-judge-test:
	STACK_V2_COMMENT_JUDGE_MANIFEST=$(COMMENT_JUDGE_MANIFEST) \
		STACK_V2_COMMENT_JUDGE_FAILURES=$(COMMENT_JUDGE_FAILURES) \
		STACK_V2_COMMENT_JUDGE_REPORT_DIR=$(COMMENT_JUDGE_REPORT_DIR) \
		COMMENT_JUDGE_LEDGER=$(COMMENT_JUDGE_LEDGER) \
		COMMENT_JUDGE_FORCE=$(COMMENT_JUDGE_FORCE) \
		COMMENT_JUDGE_USE_CODEX=1 \
		COMMENT_JUDGE_CODEX_TIMEOUT=$(COMMENT_JUDGE_CODEX_TIMEOUT) \
		COMMENT_JUDGE_TIMEOUT=$(COMMENT_JUDGE_TIMEOUT) \
		COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE=$(COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE) \
		COMMENT_JUDGE_CASE_LIMIT=$(COMMENT_JUDGE_CASE_LIMIT) \
		$(UV) run pytest tests/test_stack_v2_comment_judge.py -q --no-cov


comment-judge-generate-tests:
	COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE=$(COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE) \
		$(UV) run python scripts/run_codex_comment_test_generator.py \
		--report-dir $(COMMENT_JUDGE_REPORT_DIR) \
		--timeout $(COMMENT_TESTGEN_CODEX_TIMEOUT) \
		--codex-sandbox $(COMMENT_TESTGEN_CODEX_SANDBOX) \
		$(if $(COMMENT_TESTGEN_REPORT_LIMIT),--limit $(COMMENT_TESTGEN_REPORT_LIMIT),) \
		$(COMMENT_TESTGEN_REPORTS)

comment-judge-testgen-pipeline:
	-$(MAKE) comment-judge-test
	$(MAKE) comment-judge-generate-tests

check-main-branch:
	python scripts/check_main_branch_policy.py

check-release-version:
	python scripts/check_release_version.py
