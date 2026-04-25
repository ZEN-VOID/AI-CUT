#!/usr/bin/env python3
"""Shared guard for mechanical design helper scripts."""

from __future__ import annotations

import argparse


LEGACY_SCRIPT_AUTHORSHIP_ERROR = (
    "This helper is not allowed to author canonical creative design truth. "
    "Use --allow-legacy-script-authorship only for audited legacy recovery."
)


def add_legacy_guard(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--allow-legacy-script-authorship",
        action="store_true",
        help="Audited legacy recovery only; scripts must not author creative truth.",
    )


def enforce_no_script_authorship(allow_legacy_script_authorship: bool) -> None:
    if allow_legacy_script_authorship:
        raise SystemExit(LEGACY_SCRIPT_AUTHORSHIP_ERROR)
