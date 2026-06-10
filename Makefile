UV ?= uv
COMMENT_JUDGE_LANGUAGES ?= python,java,coffeescript
COMMENT_JUDGE_LANGUAGE_COUNT ?=
COMMENT_JUDGE_PER_KIND ?= 20
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
COMMENT_JUDGE_NUM_WORKERS ?= 1
COMMENT_JUDGE_CONTENT_PREFETCH_WORKERS ?= 4
COMMENT_JUDGE_CONTENT_PREFETCH_BUFFER_SIZE ?= $(COMMENT_JUDGE_CONTENT_PREFETCH_WORKERS)
COMMENT_JUDGE_MAX_CONTENT_CHARS ?= 1000000
COMMENT_JUDGE_CASE_LIMIT ?=
COMMENT_JUDGE_MANIFEST_ARGS ?=
COMMENT_JUDGE_BACKEND ?= codex
COMMENT_JUDGE_LOCAL_PROVIDER ?= $(COMMENT_JUDGE_BACKEND)
COMMENT_JUDGE_LOCAL_MODEL ?= gemma4:31b
COMMENT_JUDGE_LOCAL_BASE_URL ?=
COMMENT_JUDGE_LOCAL_TIMEOUT ?= 180
COMMENT_JUDGE_LOCAL_TEMPERATURE ?= 0
COMMENT_TESTGEN_CODEX_TIMEOUT ?= 600
COMMENT_TESTGEN_CODEX_SANDBOX ?= workspace-write
COMMENT_TESTGEN_REPORT_LIMIT ?=
COMMENT_TESTGEN_REPORTS ?=
COMMENT_JUDGE_RUN_TESTGEN ?= 1

ifeq ($(COMMENT_JUDGE_BACKEND),codex)
COMMENT_JUDGE_AGENT_ENV = COMMENT_JUDGE_USE_CODEX=1 COMMENT_JUDGE_CODEX_TIMEOUT=$(COMMENT_JUDGE_CODEX_TIMEOUT)
else
COMMENT_JUDGE_AGENT_ENV = COMMENT_JUDGE_USE_LOCAL=1 COMMENT_JUDGE_LOCAL_PROVIDER=$(COMMENT_JUDGE_LOCAL_PROVIDER) COMMENT_JUDGE_LOCAL_MODEL=$(COMMENT_JUDGE_LOCAL_MODEL) COMMENT_JUDGE_LOCAL_BASE_URL=$(COMMENT_JUDGE_LOCAL_BASE_URL) COMMENT_JUDGE_LOCAL_TIMEOUT=$(COMMENT_JUDGE_LOCAL_TIMEOUT) COMMENT_JUDGE_LOCAL_TEMPERATURE=$(COMMENT_JUDGE_LOCAL_TEMPERATURE)
endif

.PHONY: setup setup-optional test test-optional lint smoke research-prompts comment-test-prompts
.PHONY: comment-judge-manifest comment-judge-smoke comment-judge-test
.PHONY: comment-judge-generate-tests comment-judge-testgen-pipeline
.PHONY: comment-judge-clear-ledger comment-judge-full-run check-main-branch

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

research-prompts:
	$(UV) run python scripts/build_comment_research_packets.py

comment-test-prompts:
	$(UV) run python scripts/build_comment_test_packets.py

comment-judge-manifest:
	$(UV) run --with boto3 --with datasets --with 'smart_open[s3]' \
		python scripts/build_stack_v2_comment_judge_cases.py \
		$(if $(COMMENT_JUDGE_LANGUAGES),--languages $(COMMENT_JUDGE_LANGUAGES),) \
		$(if $(COMMENT_JUDGE_LANGUAGE_COUNT),--language-count $(COMMENT_JUDGE_LANGUAGE_COUNT),) \
		--per-kind $(COMMENT_JUDGE_PER_KIND) \
		--progress-every $(COMMENT_JUDGE_PROGRESS_EVERY) \
		--num-workers $(COMMENT_JUDGE_NUM_WORKERS) \
		--content-prefetch-workers $(COMMENT_JUDGE_CONTENT_PREFETCH_WORKERS) \
		--content-prefetch-buffer-size $(COMMENT_JUDGE_CONTENT_PREFETCH_BUFFER_SIZE) \
		--max-content-chars $(COMMENT_JUDGE_MAX_CONTENT_CHARS) \
		--fetch-stack-v2-content \
		--output-root $(COMMENT_JUDGE_OUTPUT_ROOT) $(COMMENT_JUDGE_MANIFEST_ARGS)

comment-judge-smoke:
	STACK_V2_COMMENT_JUDGE_MANIFEST=$(COMMENT_JUDGE_MANIFEST) \
		STACK_V2_COMMENT_JUDGE_FAILURES=$(COMMENT_JUDGE_FAILURES) \
		STACK_V2_COMMENT_JUDGE_REPORT_DIR=$(COMMENT_JUDGE_REPORT_DIR) \
		COMMENT_JUDGE_LEDGER=$(COMMENT_JUDGE_LEDGER) \
		COMMENT_JUDGE_FORCE=$(COMMENT_JUDGE_FORCE) \
		$(COMMENT_JUDGE_AGENT_ENV) \
		COMMENT_JUDGE_CASE_LIMIT=1 \
		COMMENT_JUDGE_TIMEOUT=$(COMMENT_JUDGE_TIMEOUT) \
		COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE=$(COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE) \
		$(UV) run pytest \
			tests/test_stack_v2_comment_judge.py::test_stack_v2_manifest_generation_has_no_missing_comment_kinds \
			tests/test_stack_v2_comment_judge.py::test_stack_v2_comment_extraction_and_cleaning_with_llm_judge \
			-q --no-cov

comment-judge-test:
	STACK_V2_COMMENT_JUDGE_MANIFEST=$(COMMENT_JUDGE_MANIFEST) \
		STACK_V2_COMMENT_JUDGE_FAILURES=$(COMMENT_JUDGE_FAILURES) \
		STACK_V2_COMMENT_JUDGE_REPORT_DIR=$(COMMENT_JUDGE_REPORT_DIR) \
		COMMENT_JUDGE_LEDGER=$(COMMENT_JUDGE_LEDGER) \
		COMMENT_JUDGE_FORCE=$(COMMENT_JUDGE_FORCE) \
		$(COMMENT_JUDGE_AGENT_ENV) \
		COMMENT_JUDGE_TIMEOUT=$(COMMENT_JUDGE_TIMEOUT) \
		COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE=$(COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE) \
		COMMENT_JUDGE_CASE_LIMIT=$(COMMENT_JUDGE_CASE_LIMIT) \
		$(UV) run pytest \
			tests/test_stack_v2_comment_judge.py::test_stack_v2_manifest_generation_has_no_missing_comment_kinds \
			tests/test_stack_v2_comment_judge.py::test_stack_v2_comment_extraction_and_cleaning_with_llm_judge \
			-q --no-cov


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

comment-judge-clear-ledger:
	$(UV) run python scripts/comment_judge_validation_ledger.py clear \
		--ledger $(COMMENT_JUDGE_LEDGER) \
		--yes

comment-judge-full-run:
	COMMENT_JUDGE_LANGUAGES= \
		COMMENT_JUDGE_LANGUAGE_COUNT= \
		COMMENT_JUDGE_BACKEND=ollama \
		COMMENT_JUDGE_LOCAL_PROVIDER=ollama \
		RUN_TESTGEN=$(COMMENT_JUDGE_RUN_TESTGEN) \
		bash scripts/run_stack_v2_comment_judge_pipeline.sh

check-main-branch:
	python scripts/check_main_branch_policy.py
