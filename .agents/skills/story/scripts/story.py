#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
story2026 统一入口脚本（无须 `cd`）

用法示例：
  python "<SCRIPTS_DIR>/story.py" preflight
  python "<SCRIPTS_DIR>/story.py" where
  python "<SCRIPTS_DIR>/story.py" index stats

说明：
- 该脚本是用户侧与技能文档中的 canonical CLI 入口。
- 兼容旧入口 `webnovel.py`；两者都会转发到同一个底层模块。
"""

from __future__ import annotations

import sys
from pathlib import Path

from runtime_compat import enable_windows_utf8_stdio


def main() -> None:
    scripts_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(scripts_dir))

    # 延迟导入，避免 sys.path 未就绪
    from data_modules.webnovel import main as _main

    _main()


if __name__ == "__main__":
    enable_windows_utf8_stdio(skip_in_pytest=True)
    main()
