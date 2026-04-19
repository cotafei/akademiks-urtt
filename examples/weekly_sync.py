"""
Weekly sync example — save schedule as Markdown + ICS to a folder.
Run every Monday (e.g. via cron or Task Scheduler).
Run: python examples/weekly_sync.py  (from project root)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from akademiks import fetch_schedule, format_markdown, format_ics, week_monday

GROUP = "is-228"
OUTPUT_DIR = Path("./output")
OUTPUT_DIR.mkdir(exist_ok=True)

monday = week_monday()
days = fetch_schedule(monday, GROUP)

md_path = OUTPUT_DIR / f"schedule_{monday}.md"
md_path.write_text(format_markdown(days, monday, GROUP), encoding="utf-8")
print(f"Markdown: {md_path}")

ics_path = OUTPUT_DIR / f"schedule_{monday}.ics"
ics_path.write_text(format_ics(days, GROUP), encoding="utf-8")
print(f"ICS: {ics_path}")
