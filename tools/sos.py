#!/usr/bin/env python3
"""Sales-OS command line entry point.

Zero dependencies. Python 3.8+.

    python3 tools/sos.py --help
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from sos.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
