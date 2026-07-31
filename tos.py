from __future__ import annotations

import sys

from runtime.launcher import Launcher
from runtime.runtime_mode import RuntimeMode


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python tos.py <command>")
        return 1

    try:
        mode = RuntimeMode(sys.argv[1].lower())
    except ValueError:
        print(f"Unknown command: {sys.argv[1]}")
        return 1

    return Launcher().run(mode)


if __name__ == "__main__":
    raise SystemExit(main())
