"""Ensure know package is importable for architecture fitness tests.

The know module is installed as an editable dependency via .pth file, but paths
with spaces (iCloud's 'Mobile Documents') can cause .pth processing to fail.
This conftest adds the know/src path to sys.path as a workaround.
"""

from __future__ import annotations

import sys
from pathlib import Path

_KNOW_SRC = Path(__file__).resolve().parents[1] / ".." / "know" / "src"
if _KNOW_SRC.exists() and str(_KNOW_SRC.resolve()) not in sys.path:
    sys.path.insert(0, str(_KNOW_SRC.resolve()))
