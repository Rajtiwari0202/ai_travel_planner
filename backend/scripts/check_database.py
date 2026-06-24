from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.session import check_database


def main() -> None:
    check_database()
    print("database=ok")


if __name__ == "__main__":
    main()
