#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Legacy alias for the renamed `context_return_manager.py`.

`5-Loopback` has been renamed to `5-上下文回流`. Keep this thin wrapper so
older scripts can still invoke the manager while all canonical contracts move
to `story-context-return`.
"""

from __future__ import annotations

from context_return_manager import main
from runtime_compat import enable_windows_utf8_stdio


if __name__ == "__main__":
    enable_windows_utf8_stdio(skip_in_pytest=True)
    main()
