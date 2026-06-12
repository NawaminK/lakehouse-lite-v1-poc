#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="${ROOT_DIR}/scenarios.json"

SPARK=(docker compose exec -T spark-iceberg spark-submit)
TRINO=(docker compose exec -T trino trino --server http://localhost:8080)

mapfile -t RUNNABLE_SCENARIOS < <(
  python3 - "$MANIFEST" <<'PY'
import json
import sys

manifest_path = sys.argv[1]
with open(manifest_path, encoding="utf-8") as fh:
    manifest = json.load(fh)

for scenario in manifest["scenarios"]:
    executor = scenario["executor"]
    if executor == "manual":
        continue
    print(
        "\t".join([
            scenario["id"],
            scenario["name"],
            executor,
            scenario["path"],
        ])
    )
PY
)

for scenario in "${RUNNABLE_SCENARIOS[@]}"; do
  IFS=$'\t' read -r id name executor path <<< "$scenario"
  echo "[${id}] ${name}"

  case "$executor" in
    spark)
      "${SPARK[@]}" "$path"
      ;;
    trino_file)
      "${TRINO[@]}" --file "$path"
      ;;
    *)
      echo "ERROR: Unsupported scenario executor: ${executor}" >&2
      exit 1
      ;;
  esac
done

echo "All POC scenarios completed."
