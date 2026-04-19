"""
akademiks-urtt — Python client for the Akademiks URTK schedule API.
"""

from .api import fetch_schedule, fetch_groups
from .formatters import format_markdown, format_ics, format_json
from .utils import week_monday, parse_utc, to_utc_iso

__version__ = "1.0.0"
__all__ = [
    "fetch_schedule",
    "fetch_groups",
    "format_markdown",
    "format_ics",
    "format_json",
    "week_monday",
    "parse_utc",
    "to_utc_iso",
]
