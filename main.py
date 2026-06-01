"""dbt build + snapshot pipeline.

dbt build writes models into Neon DuckLake (metadata, per-dataset schema)
+ R2 (Parquet). Snapshot exports the Neon schema to a standalone DuckDB
file in R2 so that queria-web (DuckDB WASM) can ATTACH it read-only.

Usage:
    python main.py [target]
    # target: "default" (default) or "local"
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

from dbt.cli.main import dbtRunner

SHARED_SCRIPTS = Path(__file__).resolve().parent / "shared" / "scripts"
_spec = importlib.util.spec_from_file_location(
    "snapshot_to_r2", SHARED_SCRIPTS / "snapshot-to-r2.py"
)
assert _spec and _spec.loader
snapshot_to_r2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(snapshot_to_r2)


def main() -> None:
    target = os.environ.get("DBT_TARGET", sys.argv[1] if len(sys.argv) > 1 else "default")

    dbt = dbtRunner()
    for cmd in (
        ["deps"],
        ["build", "--target", target],
        ["docs", "generate", "--target", target],
    ):
        result = dbt.invoke(cmd)
        if not result.success:
            raise SystemExit(f"dbt {' '.join(cmd)} failed")

    snapshot_to_r2.run(target)


if __name__ == "__main__":
    main()
