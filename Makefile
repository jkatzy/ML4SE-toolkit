UV ?= uv
COMMENT_JUDGE_LANGUAGES ?= python,java,coffeescript
COMMENT_JUDGE_LANGUAGE_COUNT ?=
COMMENT_JUDGE_PER_KIND ?= 20
COMMENT_JUDGE_FILES_PER_LANGUAGE ?=
COMMENT_JUDGE_MAX_RECORDS_PER_LANGUAGE ?=
COMMENT_JUDGE_OUTPUT_ROOT ?= tmp/stack_v2_comment_judge
COMMENT_JUDGE_MANIFEST ?= $(COMMENT_JUDGE_OUTPUT_ROOT)/manifest.jsonl
COMMENT_JUDGE_FAILURES ?= $(COMMENT_JUDGE_OUTPUT_ROOT)/failures.jsonl
COMMENT_JUDGE_REPORT_DIR ?= $(COMMENT_JUDGE_OUTPUT_ROOT)/reports
COMMENT_JUDGE_LEDGER ?= $(COMMENT_JUDGE_OUTPUT_ROOT)/validation_ledger.md
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
COMMENT_JUDGE_SCOPE ?= combined
COMMENT_JUDGE_TEST_NODE ?= tests/test_stack_v2_comment_judge.py::test_stack_v2_comment_extraction_and_cleaning_with_llm_judge
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
COMMENT_CLEANER_JUDGE_OUTPUT_ROOT ?= tmp/stack_v2_comment_cleaner_judge
COMMENT_CLEANER_JUDGE_TEST_NODE ?= tests/test_stack_v2_comment_judge.py::test_stack_v2_comment_cleaning_with_llm_judge
COMMENT_FUZZ_SEED ?= 0xC0FFEE
COMMENT_FUZZ_CASES_PER_LANGUAGE ?= 100
COMMENT_FUZZ_MAX_LENGTH ?= 128
COMMENT_FUZZ_SANITIZER_PAYLOADS_PER_EXAMPLE ?= 4
STACK_V3_FULL_JUDGE_INPUT ?=
STACK_V3_FULL_JUDGE_OUTPUT_ROOT ?= tmp/stack_v3_full_comment_judge
STACK_V3_FULL_JUDGE_MANIFEST ?= $(STACK_V3_FULL_JUDGE_OUTPUT_ROOT)/manifest.jsonl
STACK_V3_FULL_JUDGE_FAILURES ?= $(STACK_V3_FULL_JUDGE_OUTPUT_ROOT)/failures.jsonl
STACK_V3_FULL_JUDGE_REPORT_DIR ?= $(STACK_V3_FULL_JUDGE_OUTPUT_ROOT)/reports
STACK_V3_FULL_JUDGE_LEDGER ?= $(STACK_V3_FULL_JUDGE_OUTPUT_ROOT)/validation_ledger.md
STACK_V3_FULL_JUDGE_MANIFEST_ARGS ?=

ifeq ($(COMMENT_JUDGE_BACKEND),codex)
COMMENT_JUDGE_AGENT_ENV = COMMENT_JUDGE_USE_CODEX=1 COMMENT_JUDGE_CODEX_TIMEOUT=$(COMMENT_JUDGE_CODEX_TIMEOUT)
else
COMMENT_JUDGE_AGENT_ENV = COMMENT_JUDGE_USE_LOCAL=1 COMMENT_JUDGE_LOCAL_PROVIDER=$(COMMENT_JUDGE_LOCAL_PROVIDER) COMMENT_JUDGE_LOCAL_MODEL=$(COMMENT_JUDGE_LOCAL_MODEL) COMMENT_JUDGE_LOCAL_BASE_URL=$(COMMENT_JUDGE_LOCAL_BASE_URL) COMMENT_JUDGE_LOCAL_TIMEOUT=$(COMMENT_JUDGE_LOCAL_TIMEOUT) COMMENT_JUDGE_LOCAL_TEMPERATURE=$(COMMENT_JUDGE_LOCAL_TEMPERATURE)
endif

.PHONY: setup setup-optional test test-optional lint smoke build research-prompts
.PHONY: research-validate
.PHONY: comment-confirmation-prompts comment-test-prompts
.PHONY: comment-cleaner-fixtures comment-fuzz comment-cleaner-fuzz
.PHONY: comment-judge-manifest comment-judge-coverage comment-judge-smoke comment-judge-test
.PHONY: comment-cleaner-judge-manifest comment-cleaner-judge-smoke comment-cleaner-judge-test
.PHONY: comment-judge-generate-tests comment-judge-testgen-pipeline
.PHONY: comment-judge-clear-ledger comment-judge-full-run check-main-branch check-release-version
.PHONY: stack-v3-full-comment-judge-manifest stack-v3-full-comment-judge-coverage
.PHONY: stack-v3-full-comment-judge-smoke stack-v3-full-comment-judge-test

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
	$(UV) run python scripts/build_comment_research_packets.py \
		--output-root tmp/stack_v3_comment_research

research-validate:
	$(UV) run python scripts/validate_comment_research.py --require-reviewed

comment-confirmation-prompts:
	$(UV) run python scripts/build_comment_confirmation_packets.py

comment-test-prompts:
	$(UV) run python scripts/build_comment_test_packets.py

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

comment-judge-manifest:
	$(UV) run --with boto3 --with datasets --with 'smart_open[s3]' \
		python scripts/build_stack_v2_comment_judge_cases.py \
		$(if $(COMMENT_JUDGE_LANGUAGES),--languages $(COMMENT_JUDGE_LANGUAGES),) \
		$(if $(COMMENT_JUDGE_LANGUAGE_COUNT),--language-count $(COMMENT_JUDGE_LANGUAGE_COUNT),) \
		--per-kind $(COMMENT_JUDGE_PER_KIND) \
		$(if $(COMMENT_JUDGE_FILES_PER_LANGUAGE),--files-per-language $(COMMENT_JUDGE_FILES_PER_LANGUAGE),) \
		$(if $(COMMENT_JUDGE_MAX_RECORDS_PER_LANGUAGE),--max-records-per-language $(COMMENT_JUDGE_MAX_RECORDS_PER_LANGUAGE),) \
		--progress-every $(COMMENT_JUDGE_PROGRESS_EVERY) \
		--num-workers $(COMMENT_JUDGE_NUM_WORKERS) \
		--content-prefetch-workers $(COMMENT_JUDGE_CONTENT_PREFETCH_WORKERS) \
		--content-prefetch-buffer-size $(COMMENT_JUDGE_CONTENT_PREFETCH_BUFFER_SIZE) \
		--max-content-chars $(COMMENT_JUDGE_MAX_CONTENT_CHARS) \
		--fetch-stack-v2-content \
		--output-root $(COMMENT_JUDGE_OUTPUT_ROOT) $(COMMENT_JUDGE_MANIFEST_ARGS)

comment-judge-coverage:
	$(MAKE) comment-judge-manifest
	STACK_V2_COMMENT_JUDGE_MANIFEST=$(COMMENT_JUDGE_MANIFEST) \
		STACK_V2_COMMENT_JUDGE_FAILURES=$(COMMENT_JUDGE_FAILURES) \
		STACK_V2_COMMENT_JUDGE_REPORT_DIR=$(COMMENT_JUDGE_REPORT_DIR) \
		COMMENT_JUDGE_LEDGER=0 \
		$(UV) run pytest \
			tests/test_stack_v2_comment_judge.py::test_stack_v2_manifest_generation_has_no_missing_comment_kinds \
			-q --no-cov

comment-judge-smoke:
	STACK_V2_COMMENT_JUDGE_MANIFEST=$(COMMENT_JUDGE_MANIFEST) \
		STACK_V2_COMMENT_JUDGE_FAILURES=$(COMMENT_JUDGE_FAILURES) \
		STACK_V2_COMMENT_JUDGE_REPORT_DIR=$(COMMENT_JUDGE_REPORT_DIR) \
		COMMENT_JUDGE_LEDGER=$(COMMENT_JUDGE_LEDGER) \
		COMMENT_JUDGE_FORCE=$(COMMENT_JUDGE_FORCE) \
		COMMENT_JUDGE_SCOPE=$(COMMENT_JUDGE_SCOPE) \
		$(COMMENT_JUDGE_AGENT_ENV) \
		COMMENT_JUDGE_CASE_LIMIT=1 \
		COMMENT_JUDGE_TIMEOUT=$(COMMENT_JUDGE_TIMEOUT) \
		COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE=$(COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE) \
		$(UV) run pytest \
			tests/test_stack_v2_comment_judge.py::test_stack_v2_manifest_generation_has_no_missing_comment_kinds \
			$(COMMENT_JUDGE_TEST_NODE) \
			-q --no-cov

comment-judge-test:
	STACK_V2_COMMENT_JUDGE_MANIFEST=$(COMMENT_JUDGE_MANIFEST) \
		STACK_V2_COMMENT_JUDGE_FAILURES=$(COMMENT_JUDGE_FAILURES) \
		STACK_V2_COMMENT_JUDGE_REPORT_DIR=$(COMMENT_JUDGE_REPORT_DIR) \
		COMMENT_JUDGE_LEDGER=$(COMMENT_JUDGE_LEDGER) \
		COMMENT_JUDGE_FORCE=$(COMMENT_JUDGE_FORCE) \
		COMMENT_JUDGE_SCOPE=$(COMMENT_JUDGE_SCOPE) \
		$(COMMENT_JUDGE_AGENT_ENV) \
		COMMENT_JUDGE_TIMEOUT=$(COMMENT_JUDGE_TIMEOUT) \
		COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE=$(COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE) \
		COMMENT_JUDGE_CASE_LIMIT=$(COMMENT_JUDGE_CASE_LIMIT) \
		$(UV) run pytest \
			tests/test_stack_v2_comment_judge.py::test_stack_v2_manifest_generation_has_no_missing_comment_kinds \
			$(COMMENT_JUDGE_TEST_NODE) \
			-q --no-cov

stack-v3-full-comment-judge-manifest:
	@test -n "$(STACK_V3_FULL_JUDGE_INPUT)" || \
		(echo "STACK_V3_FULL_JUDGE_INPUT must name a local flat contents-table JSONL export" >&2; exit 2)
	$(UV) run python scripts/build_stack_v3_full_comment_judge_cases.py \
		--input-jsonl "$(STACK_V3_FULL_JUDGE_INPUT)" \
		$(if $(COMMENT_JUDGE_LANGUAGES),--languages $(COMMENT_JUDGE_LANGUAGES),) \
		$(if $(COMMENT_JUDGE_LANGUAGE_COUNT),--language-count $(COMMENT_JUDGE_LANGUAGE_COUNT),) \
		--per-kind $(COMMENT_JUDGE_PER_KIND) \
		$(if $(COMMENT_JUDGE_FILES_PER_LANGUAGE),--files-per-language $(COMMENT_JUDGE_FILES_PER_LANGUAGE),) \
		$(if $(COMMENT_JUDGE_MAX_RECORDS_PER_LANGUAGE),--max-records-per-language $(COMMENT_JUDGE_MAX_RECORDS_PER_LANGUAGE),) \
		--progress-every $(COMMENT_JUDGE_PROGRESS_EVERY) \
		--num-workers $(COMMENT_JUDGE_NUM_WORKERS) \
		--content-prefetch-workers $(COMMENT_JUDGE_CONTENT_PREFETCH_WORKERS) \
		--content-prefetch-buffer-size $(COMMENT_JUDGE_CONTENT_PREFETCH_BUFFER_SIZE) \
		--max-content-chars $(COMMENT_JUDGE_MAX_CONTENT_CHARS) \
		--output-root $(STACK_V3_FULL_JUDGE_OUTPUT_ROOT) \
		$(STACK_V3_FULL_JUDGE_MANIFEST_ARGS)

stack-v3-full-comment-judge-coverage:
	$(MAKE) stack-v3-full-comment-judge-manifest
	STACK_V2_COMMENT_JUDGE_MANIFEST=$(STACK_V3_FULL_JUDGE_MANIFEST) \
		STACK_V2_COMMENT_JUDGE_FAILURES=$(STACK_V3_FULL_JUDGE_FAILURES) \
		STACK_V2_COMMENT_JUDGE_REPORT_DIR=$(STACK_V3_FULL_JUDGE_REPORT_DIR) \
		COMMENT_JUDGE_LEDGER=0 \
		$(UV) run pytest \
			tests/test_stack_v2_comment_judge.py::test_stack_v2_manifest_generation_has_no_missing_comment_kinds \
			-q --no-cov

stack-v3-full-comment-judge-smoke:
	$(MAKE) comment-judge-smoke \
		COMMENT_JUDGE_OUTPUT_ROOT=$(STACK_V3_FULL_JUDGE_OUTPUT_ROOT) \
		COMMENT_JUDGE_MANIFEST=$(STACK_V3_FULL_JUDGE_MANIFEST) \
		COMMENT_JUDGE_FAILURES=$(STACK_V3_FULL_JUDGE_FAILURES) \
		COMMENT_JUDGE_REPORT_DIR=$(STACK_V3_FULL_JUDGE_REPORT_DIR) \
		COMMENT_JUDGE_LEDGER=$(STACK_V3_FULL_JUDGE_LEDGER)

stack-v3-full-comment-judge-test:
	$(MAKE) comment-judge-test \
		COMMENT_JUDGE_OUTPUT_ROOT=$(STACK_V3_FULL_JUDGE_OUTPUT_ROOT) \
		COMMENT_JUDGE_MANIFEST=$(STACK_V3_FULL_JUDGE_MANIFEST) \
		COMMENT_JUDGE_FAILURES=$(STACK_V3_FULL_JUDGE_FAILURES) \
		COMMENT_JUDGE_REPORT_DIR=$(STACK_V3_FULL_JUDGE_REPORT_DIR) \
		COMMENT_JUDGE_LEDGER=$(STACK_V3_FULL_JUDGE_LEDGER)


comment-cleaner-judge-manifest:
	$(MAKE) comment-judge-manifest \
		COMMENT_JUDGE_OUTPUT_ROOT=$(COMMENT_CLEANER_JUDGE_OUTPUT_ROOT)

comment-cleaner-judge-smoke:
	$(MAKE) comment-judge-smoke \
		COMMENT_JUDGE_OUTPUT_ROOT=$(COMMENT_CLEANER_JUDGE_OUTPUT_ROOT) \
		COMMENT_JUDGE_SCOPE=cleaning \
		COMMENT_JUDGE_TEST_NODE=$(COMMENT_CLEANER_JUDGE_TEST_NODE)

comment-cleaner-judge-test:
	$(MAKE) comment-judge-test \
		COMMENT_JUDGE_OUTPUT_ROOT=$(COMMENT_CLEANER_JUDGE_OUTPUT_ROOT) \
		COMMENT_JUDGE_SCOPE=cleaning \
		COMMENT_JUDGE_TEST_NODE=$(COMMENT_CLEANER_JUDGE_TEST_NODE)


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

check-release-version:
	python scripts/check_release_version.py


COMMENT_CLEANER_TWO_STAGE_MANIFEST ?= $(COMMENT_CLEANER_JUDGE_OUTPUT_ROOT)/manifest.jsonl
COMMENT_CLEANER_TWO_STAGE_OUTPUT_ROOT ?= $(COMMENT_CLEANER_JUDGE_OUTPUT_ROOT)/two_stage
COMMENT_CLEANER_TWO_STAGE_BATCH_SIZE ?= 50
COMMENT_CLEANER_TWO_STAGE_MAX_PROMPT_CHARS ?= 80000
COMMENT_CLEANER_TWO_STAGE_WORKERS ?= 4
COMMENT_CLEANER_TWO_STAGE_TIMEOUT ?= 300
COMMENT_CLEANER_TWO_STAGE_ARGS ?=

.PHONY: comment-cleaner-judge-two-stage
comment-cleaner-judge-two-stage:
	$(UV) run python scripts/run_two_stage_comment_cleaner_judge.py \
		--manifest $(COMMENT_CLEANER_TWO_STAGE_MANIFEST) \
		--output-root $(COMMENT_CLEANER_TWO_STAGE_OUTPUT_ROOT) \
		--batch-size $(COMMENT_CLEANER_TWO_STAGE_BATCH_SIZE) \
		--max-prompt-chars $(COMMENT_CLEANER_TWO_STAGE_MAX_PROMPT_CHARS) \
		--workers $(COMMENT_CLEANER_TWO_STAGE_WORKERS) \
		--timeout $(COMMENT_CLEANER_TWO_STAGE_TIMEOUT) $(COMMENT_CLEANER_TWO_STAGE_ARGS)
