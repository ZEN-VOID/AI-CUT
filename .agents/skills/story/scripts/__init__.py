"""
story2026 scripts package

This package contains all Python scripts for the story2026 runtime.
"""

from importlib import import_module

__version__ = "5.5.4"
__author__ = "lcy"

__all__ = [
    "security_utils",
    "project_locator",
    "chapter_paths",
]


def __getattr__(name: str):
    """Lazily import heavy helpers so package import stays side-effect free."""
    if name in __all__:
        module = import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
