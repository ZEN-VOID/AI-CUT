#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
兼容入口：保留旧文件名 `webnovel.py`

说明：
- canonical CLI 已切换为 `story.py`。
- 本文件仅作为 legacy alias，避免旧脚本/旧自动化直接断裂。
"""

from __future__ import annotations

from story import main

from runtime_compat import enable_windows_utf8_stdio


if __name__ == "__main__":
    enable_windows_utf8_stdio(skip_in_pytest=True)
    main()
