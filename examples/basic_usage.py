"""
Basic usage example — fetch and print schedule for a group.
Run: python examples/basic_usage.py  (from project root)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from akademiks import fetch_schedule, format_markdown, week_monday

group = "is-228"
monday = week_monday()  # current week

days = fetch_schedule(monday, group)
md = format_markdown(days, monday, group)
print(md)
