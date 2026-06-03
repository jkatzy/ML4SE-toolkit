#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

# Language/sample scope.
export COMMENT_JUDGE_LANGUAGES="${COMMENT_JUDGE_LANGUAGES:-}"
export COMMENT_JUDGE_LANGUAGE_COUNT="${COMMENT_JUDGE_LANGUAGE_COUNT:-10}"
export COMMENT_JUDGE_PER_KIND="${COMMENT_JUDGE_PER_KIND:-20}"
export COMMENT_JUDGE_PROGRESS_EVERY="${COMMENT_JUDGE_PROGRESS_EVERY:-10}"
export COMMENT_JUDGE_NUM_WORKERS="${COMMENT_JUDGE_NUM_WORKERS:-50}"
export COMMENT_JUDGE_CONTENT_PREFETCH_WORKERS="${COMMENT_JUDGE_CONTENT_PREFETCH_WORKERS:-8}"
export COMMENT_JUDGE_CONTENT_PREFETCH_BUFFER_SIZE="${COMMENT_JUDGE_CONTENT_PREFETCH_BUFFER_SIZE:-128}"
export COMMENT_JUDGE_MAX_CONTENT_CHARS="${COMMENT_JUDGE_MAX_CONTENT_CHARS:-500000}"
export COMMENT_JUDGE_MANIFEST_ARGS="${COMMENT_JUDGE_MANIFEST_ARGS:-}"

# Generated artifact locations.
export COMMENT_JUDGE_OUTPUT_ROOT="${COMMENT_JUDGE_OUTPUT_ROOT:-tmp/stack_v2_comment_judge}"
export COMMENT_JUDGE_MANIFEST="${COMMENT_JUDGE_MANIFEST:-${COMMENT_JUDGE_OUTPUT_ROOT}/manifest.jsonl}"
export COMMENT_JUDGE_FAILURES="${COMMENT_JUDGE_FAILURES:-${COMMENT_JUDGE_OUTPUT_ROOT}/failures.jsonl}"
export COMMENT_JUDGE_REPORT_DIR="${COMMENT_JUDGE_REPORT_DIR:-${COMMENT_JUDGE_OUTPUT_ROOT}/reports}"
export COMMENT_JUDGE_LEDGER="${COMMENT_JUDGE_LEDGER:-docs/comment_testing/stack_v2_judge_validation_ledger.md}"

# Judge backend.
export COMMENT_JUDGE_BACKEND="${COMMENT_JUDGE_BACKEND:-ollama}"
export COMMENT_JUDGE_LOCAL_PROVIDER="${COMMENT_JUDGE_LOCAL_PROVIDER:-ollama}"
export COMMENT_JUDGE_LOCAL_MODEL="${COMMENT_JUDGE_LOCAL_MODEL:-gemma4:31b}"
export COMMENT_JUDGE_LOCAL_BASE_URL="${COMMENT_JUDGE_LOCAL_BASE_URL:-}"
export COMMENT_JUDGE_LOCAL_TIMEOUT="${COMMENT_JUDGE_LOCAL_TIMEOUT:-180}"
export COMMENT_JUDGE_LOCAL_TEMPERATURE="${COMMENT_JUDGE_LOCAL_TEMPERATURE:-0}"
export COMMENT_JUDGE_TIMEOUT="${COMMENT_JUDGE_TIMEOUT:-240}"
export COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE="${COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE:-88}"
export COMMENT_JUDGE_FORCE="${COMMENT_JUDGE_FORCE:-0}"
export COMMENT_JUDGE_CASE_LIMIT="${COMMENT_JUDGE_CASE_LIMIT:-}"

# Test-generation agent settings. These are used only if RUN_TESTGEN=1.
export COMMENT_TESTGEN_CODEX_TIMEOUT="${COMMENT_TESTGEN_CODEX_TIMEOUT:-600}"
export COMMENT_TESTGEN_CODEX_SANDBOX="${COMMENT_TESTGEN_CODEX_SANDBOX:-workspace-write}"
export COMMENT_TESTGEN_REPORT_LIMIT="${COMMENT_TESTGEN_REPORT_LIMIT:-}"
export COMMENT_TESTGEN_REPORTS="${COMMENT_TESTGEN_REPORTS:-}"

# Pipeline persistence. Each language gets an isolated output root so completed
# work survives later language failures and can be skipped on rerun.
export COMMENT_JUDGE_PIPELINE_RESUME="${COMMENT_JUDGE_PIPELINE_RESUME:-1}"
export COMMENT_JUDGE_PIPELINE_STATUS="${COMMENT_JUDGE_PIPELINE_STATUS:-${COMMENT_JUDGE_OUTPUT_ROOT}/pipeline_status.tsv}"

pipeline_output_root="${COMMENT_JUDGE_OUTPUT_ROOT}"
pipeline_manifest="${COMMENT_JUDGE_MANIFEST}"
pipeline_failures="${COMMENT_JUDGE_FAILURES}"
pipeline_report_dir="${COMMENT_JUDGE_REPORT_DIR}"
pipeline_status="${COMMENT_JUDGE_PIPELINE_STATUS}"

truthy() {
  case "${1,,}" in
    1|true|yes|on) return 0 ;;
    *) return 1 ;;
  esac
}

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "${value}"
}

language_slug() {
  local slug="${1,,}"
  slug="${slug//+/plus}"
  slug="${slug//\#/sharp}"
  slug="${slug// /-}"
  slug="$(printf '%s' "${slug}" | sed -E 's/[^a-z0-9._-]+/-/g; s/^-+//; s/-+$//')"
  printf '%s' "${slug:-language}"
}

selected_languages() {
  if [[ -n "${COMMENT_JUDGE_LANGUAGES}" ]]; then
    local raw_language
    local emitted=0
    IFS=',' read -r -a raw_languages <<< "${COMMENT_JUDGE_LANGUAGES}"
    for raw_language in "${raw_languages[@]}"; do
      raw_language="$(trim "${raw_language}")"
      if [[ -z "${raw_language}" ]]; then
        continue
      fi
      printf '%s\n' "${raw_language}"
      emitted=$((emitted + 1))
      if [[ -n "${COMMENT_JUDGE_LANGUAGE_COUNT}" ]] \
        && [[ "${emitted}" -ge "${COMMENT_JUDGE_LANGUAGE_COUNT}" ]]; then
        break
      fi
    done
    return
  fi

  "${UV:-uv}" run python - <<'PY'
import os

from ml4setk.Parsing.Comments import get_supported_comment_languages

languages = get_supported_comment_languages()
language_count = os.environ.get("COMMENT_JUDGE_LANGUAGE_COUNT")
if language_count:
    languages = languages[: int(language_count)]
for language in languages:
    print(language)
PY
}

append_language_outputs() {
  local language_manifest="$1"
  local language_failures="$2"
  local language_report_dir="$3"

  if [[ -s "${language_manifest}" ]]; then
    cat "${language_manifest}" >> "${pipeline_manifest}"
  fi
  if [[ -s "${language_failures}" ]]; then
    cat "${language_failures}" >> "${pipeline_failures}"
  fi
  copy_language_reports "${language_report_dir}"
}

copy_language_reports() {
  local language_report_dir="$1"

  if [[ -d "${language_report_dir}" ]]; then
    find "${language_report_dir}" -type f -name '*.md' -exec cp {} "${pipeline_report_dir}/" \;
  fi
}

record_status() {
  local language="$1"
  local status="$2"
  local manifest_exit="$3"
  local judge_exit="$4"
  local testgen_exit="$5"
  local language_output_root="$6"

  printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
    "${language}" \
    "${status}" \
    "${manifest_exit}" \
    "${judge_exit}" \
    "${testgen_exit}" \
    "${language_output_root}" >> "${pipeline_status}"
}

write_language_status() {
  local status_file="$1"
  local language="$2"
  local status="$3"
  local manifest_exit="$4"
  local judge_exit="$5"
  local testgen_exit="$6"

  {
    printf 'language=%s\n' "${language}"
    printf 'status=%s\n' "${status}"
    printf 'manifest_exit=%s\n' "${manifest_exit}"
    printf 'judge_exit=%s\n' "${judge_exit}"
    printf 'testgen_exit=%s\n' "${testgen_exit}"
    printf 'updated_at=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  } > "${status_file}"
}

language_completed() {
  local status_file="$1"
  local language_manifest="$2"

  truthy "${COMMENT_JUDGE_PIPELINE_RESUME}" \
    && [[ -s "${language_manifest}" ]] \
    && [[ -f "${status_file}" ]] \
    && grep -qx 'status=passed' "${status_file}"
}

if [[ -n "${COMMENT_JUDGE_LANGUAGE_COUNT}" ]]; then
  if ! [[ "${COMMENT_JUDGE_LANGUAGE_COUNT}" =~ ^[0-9]+$ ]] \
    || [[ "${COMMENT_JUDGE_LANGUAGE_COUNT}" -lt 1 ]]; then
    echo "[comment-judge-pipeline] COMMENT_JUDGE_LANGUAGE_COUNT must be a positive integer" >&2
    exit 2
  fi
fi

mapfile -t languages < <(selected_languages)
if [[ "${#languages[@]}" -eq 0 ]]; then
  echo "[comment-judge-pipeline] no languages selected" >&2
  exit 2
fi

mkdir -p \
  "${pipeline_output_root}/languages" \
  "$(dirname "${pipeline_manifest}")" \
  "$(dirname "${pipeline_failures}")" \
  "${pipeline_report_dir}" \
  "$(dirname "${pipeline_status}")"
: > "${pipeline_manifest}"
: > "${pipeline_failures}"
printf 'language\tstatus\tmanifest_exit\tjudge_exit\ttestgen_exit\toutput_root\n' > "${pipeline_status}"

pipeline_failures_seen=0
usage_limit_seen=0

for language in "${languages[@]}"; do
  slug="$(language_slug "${language}")"
  language_output_root="${pipeline_output_root}/languages/${slug}"
  language_manifest="${language_output_root}/manifest.jsonl"
  language_failures="${language_output_root}/failures.jsonl"
  language_report_dir="${language_output_root}/reports"
  language_status="${language_output_root}/pipeline.status"

  mkdir -p "${language_output_root}" "${language_report_dir}"

  if language_completed "${language_status}" "${language_manifest}"; then
    echo "[comment-judge-pipeline] skipping ${language}; saved pass exists"
    append_language_outputs "${language_manifest}" "${language_failures}" "${language_report_dir}"
    record_status "${language}" "skipped" 0 0 "skipped" "${language_output_root}"
    continue
  fi

  echo "[comment-judge-pipeline] ${language}: generating manifest"
  if COMMENT_JUDGE_LANGUAGES="${language}" \
    COMMENT_JUDGE_LANGUAGE_COUNT= \
    COMMENT_JUDGE_OUTPUT_ROOT="${language_output_root}" \
    COMMENT_JUDGE_MANIFEST="${language_manifest}" \
    COMMENT_JUDGE_FAILURES="${language_failures}" \
    COMMENT_JUDGE_REPORT_DIR="${language_report_dir}" \
    make comment-judge-manifest; then
    manifest_exit=0
  else
    manifest_exit=$?
  fi

  append_language_outputs "${language_manifest}" "${language_failures}" "${language_report_dir}"

  if [[ "${manifest_exit}" -ne 0 ]]; then
    echo "[comment-judge-pipeline] ${language}: manifest failed exit=${manifest_exit}" >&2
    write_language_status "${language_status}" "${language}" "manifest_failed" "${manifest_exit}" "skipped" "skipped"
    record_status "${language}" "manifest_failed" "${manifest_exit}" "skipped" "skipped" "${language_output_root}"
    pipeline_failures_seen=1
    continue
  fi

  echo "[comment-judge-pipeline] ${language}: running judge suite"
  if COMMENT_JUDGE_LANGUAGES="${language}" \
    COMMENT_JUDGE_LANGUAGE_COUNT= \
    COMMENT_JUDGE_OUTPUT_ROOT="${language_output_root}" \
    COMMENT_JUDGE_MANIFEST="${language_manifest}" \
    COMMENT_JUDGE_FAILURES="${language_failures}" \
    COMMENT_JUDGE_REPORT_DIR="${language_report_dir}" \
    make comment-judge-test; then
    judge_exit=0
  else
    judge_exit=$?
  fi

  copy_language_reports "${language_report_dir}"

  testgen_exit="skipped"
  if [[ "${RUN_TESTGEN:-0}" == "1" ]] \
    && [[ "${judge_exit}" -ne "${COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE}" ]]; then
    echo "[comment-judge-pipeline] ${language}: generating deterministic tests from reports"
    if COMMENT_JUDGE_OUTPUT_ROOT="${language_output_root}" \
      COMMENT_JUDGE_MANIFEST="${language_manifest}" \
      COMMENT_JUDGE_FAILURES="${language_failures}" \
      COMMENT_JUDGE_REPORT_DIR="${language_report_dir}" \
      make comment-judge-generate-tests; then
      testgen_exit=0
    else
      testgen_exit=$?
    fi
  fi

  if [[ "${judge_exit}" -eq 0 ]] \
    && [[ "${testgen_exit}" != "skipped" ]] \
    && [[ "${testgen_exit}" -ne 0 ]]; then
    status="testgen_failed"
  elif [[ "${judge_exit}" -eq 0 ]]; then
    status="passed"
  else
    status="judge_failed"
  fi

  write_language_status \
    "${language_status}" \
    "${language}" \
    "${status}" \
    "${manifest_exit}" \
    "${judge_exit}" \
    "${testgen_exit}"
  record_status \
    "${language}" \
    "${status}" \
    "${manifest_exit}" \
    "${judge_exit}" \
    "${testgen_exit}" \
    "${language_output_root}"

  if [[ "${judge_exit}" -eq "${COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE}" ]]; then
    echo "[comment-judge-pipeline] ${language}: usage limit reached; stopping remaining languages" >&2
    usage_limit_seen=1
    pipeline_failures_seen=1
    break
  fi

  if [[ "${status}" != "passed" ]]; then
    pipeline_failures_seen=1
  fi
done

echo "[comment-judge-pipeline] wrote aggregate manifest ${pipeline_manifest}"
echo "[comment-judge-pipeline] wrote per-language status ${pipeline_status}"

if [[ "${usage_limit_seen}" -eq 1 ]]; then
  exit "${COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE}"
fi
if [[ "${pipeline_failures_seen}" -ne 0 ]]; then
  exit 1
fi
