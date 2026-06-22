from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "research" / "experiments" / script)], check=True)


def main() -> None:
    run("run_benchmarks.py")
    run("run_ablations.py")


if __name__ == "__main__":
    main()
