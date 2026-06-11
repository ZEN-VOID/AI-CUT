#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retired validation runner shim.

Story acceptance is now built into `3-初稿` and `4-润色`. This file remains only
to fail old direct imports with an explicit migration message instead of
silently recreating a standalone review stage.
"""

from __future__ import annotations

import sys


RETIREMENT_MESSAGE = (
    "validation_runner is retired; run the owning stage instead: "
    "3-初稿 writes draft acceptance, 4-润色 writes final acceptance."
)


def main(argv: list[str] | None = None) -> int:
    _ = argv
    print(RETIREMENT_MESSAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
