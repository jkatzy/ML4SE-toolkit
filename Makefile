UV ?= uv

.PHONY: setup setup-optional test test-optional lint smoke research-prompts comment-test-prompts check-main-branch

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

check-main-branch:
	python scripts/check_main_branch_policy.py
