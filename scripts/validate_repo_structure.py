#!/usr/bin/env python3
import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]

GENERATED_NAMES = {".DS_Store", "__pycache__"}
GENERATED_SUFFIXES = {".pyc", ".pyo", ".pyd"}

REQUIRED_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "docs/README.md",
    "docs/requirements.md",
    "docs/team-roadmap.md",
    "docs/github-workflow.md",
    "docs/engineering/definition-of-done.md",
    "docs/learning/onboarding-journey.md",
    "docs/runbooks/service-health-checklist.md",
    "docs/runbooks/startup-shutdown.md",
    "docs/security/poc-vs-production.md",
    "scenarios.json",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail(f"Missing required files: {missing}")


def check_generated_files() -> None:
    offenders = []
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        paths = [
            ROOT / path.decode("utf-8")
            for path in result.stdout.split(b"\0")
            if path
        ]
    except (subprocess.CalledProcessError, FileNotFoundError):
        paths = [path for path in ROOT.rglob("*") if ".git" not in path.parts]

    for path in paths:
        if path.name in GENERATED_NAMES or path.suffix in GENERATED_SUFFIXES:
            offenders.append(path.relative_to(ROOT).as_posix())

    if offenders:
        fail(f"Generated files should not be committed: {offenders}")


def check_python_syntax() -> None:
    for path in ROOT.rglob("*.py"):
        if ".git" in path.parts:
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            fail(f"Python syntax error in {path.relative_to(ROOT)}: {exc}")


def container_path_to_repo_path(path: str) -> Optional[Path]:
    mappings = {
        "/home/iceberg/jobs/": "spark/jobs/",
        "/tmp/sql/": "sql/",
    }

    for container_prefix, repo_prefix in mappings.items():
        if path.startswith(container_prefix):
            return ROOT / repo_prefix / path.removeprefix(container_prefix)

    return None


def check_scenario_manifest() -> None:
    manifest_path = ROOT / "scenarios.json"
    with manifest_path.open(encoding="utf-8") as fh:
        manifest = json.load(fh)

    ids = []
    slugs = []
    for scenario in manifest.get("scenarios", []):
        scenario_id = scenario.get("id")
        slug = scenario.get("slug")
        executor = scenario.get("executor")
        doc = scenario.get("doc")

        if not scenario_id or not slug or not executor or not doc:
            fail(f"Scenario is missing required fields: {scenario}")

        ids.append(scenario_id)
        slugs.append(slug)

        doc_path = ROOT / doc
        if not doc_path.exists():
            fail(f"Scenario doc does not exist for {scenario_id}: {doc}")

        if executor == "manual":
            continue

        if executor not in {"spark", "trino_file"}:
            fail(f"Unsupported executor for scenario {scenario_id}: {executor}")

        runnable_path = scenario.get("path")
        if not runnable_path:
            fail(f"Automated scenario {scenario_id} is missing path")

        repo_path = container_path_to_repo_path(runnable_path)
        if repo_path is None or not repo_path.exists():
            fail(f"Automated scenario {scenario_id} path cannot be resolved: {runnable_path}")

    if len(ids) != len(set(ids)):
        fail("Duplicate scenario IDs found")

    if len(slugs) != len(set(slugs)):
        fail("Duplicate scenario slugs found")


def main() -> None:
    check_required_files()
    check_generated_files()
    check_python_syntax()
    check_scenario_manifest()
    print("Repository structure validation passed")


if __name__ == "__main__":
    main()
