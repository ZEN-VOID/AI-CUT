#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backward-compatible shim for the renamed review runner.

`4-Validation` 已重命名为 `4-Review`，但部分测试或旧命令仍可能导入
`validation_runner`。这里统一转发到 `review_runner`，避免旧入口直接断裂。
"""

import review_runner as _review_runner

globals().update(
    {
        name: value
        for name, value in vars(_review_runner).items()
        if not name.startswith("__")
    }
)


if __name__ == "__main__":
    from review_runner import main

    raise SystemExit(main())
