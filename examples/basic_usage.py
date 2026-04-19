"""
Basic usage example — fetch and print schedule for a group.
"""

from datetime import date
from akademiks import fetch_schedule, format_markdown, week_monday

group = "is-228"
monday = week_monday()  # current week

days = fetch_schedule(monday, group)
md = format_markdown(days, monday, group)
print(md)
