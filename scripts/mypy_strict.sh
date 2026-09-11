#!/usr/bin/env bash
# Run mypy in strict mode against one Saleor package and report only the
# errors located inside that package (tests and migrations are excluded by
# the project mypy config). Exit code is non-zero when any error remains.
#
# Usage: scripts/mypy_strict.sh <package>   e.g. scripts/mypy_strict.sh checkout
set -uo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <package>" >&2
  exit 2
fi

pkg="$1"
path="saleor/${pkg}"

if [[ ! -d "${path}" ]]; then
  echo "no such package: ${path}" >&2
  exit 2
fi

runner=()
if command -v uv >/dev/null 2>&1; then
  runner=(uv run)
fi

output="$("${runner[@]}" mypy --strict --no-pretty --no-error-summary "${path}" 2>&1)"
errors="$(printf '%s\n' "${output}" | grep -E "^${path}/.*: error:" | grep -vE "^${path}/(.*/)?tests/" || true)"

if [[ -n "${errors}" ]]; then
  printf '%s\n' "${errors}"
fi

count=0
if [[ -n "${errors}" ]]; then
  count="$(printf '%s\n' "${errors}" | wc -l | tr -d ' ')"
fi
echo "${path}: ${count} strict mypy error(s)"

[[ "${count}" -eq 0 ]]
