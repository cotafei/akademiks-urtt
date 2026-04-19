# akademiks-urtt

Python client and CLI for the **[Akademiks URTK](https://akademiks.urtt.ru)** schedule API.

Works for **any group** at URTK (Uralsky Radio-Technical College). Zero dependencies — pure stdlib.

## Install

```bash
pip install akademiks-urtt
```

Or from source:

```bash
git clone https://github.com/your-username/akademiks-urtt
cd akademiks-urtt
pip install -e .
```

## CLI

```bash
# Show schedule for current week
akademiks --group is-228

# Specific week
akademiks --group is-228 --week 2026-04-14

# Save to folder (Markdown + ICS)
akademiks --group is-228 --out ./output --ics

# JSON output
akademiks --group is-228 --format json

# List all groups
akademiks --groups
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--group`, `-g` | required | Group ID, e.g. `is-228` |
| `--week`, `-w` | current week | Any date in the target week (`YYYY-MM-DD`) |
| `--format`, `-f` | `markdown` | Output format: `markdown`, `ics`, `json` |
| `--out`, `-o` | stdout | Directory to save output files |
| `--ics` | off | Also export `.ics` when format is `markdown` |
| `--tz-offset` | `5` | UTC offset in hours (default: Yekaterinburg UTC+5) |
| `--tz-name` | `Asia/Yekaterinburg` | IANA timezone name for ICS headers |
| `--groups` | — | List all available groups |

## Python API

```python
from datetime import date
from akademiks import fetch_schedule, fetch_groups
from akademiks import format_markdown, format_ics, format_json
from akademiks import week_monday

# Fetch schedule
monday = week_monday()                    # Monday of current week
days = fetch_schedule(monday, "is-228")   # list of day dicts

# Format
md  = format_markdown(days, monday, "is-228")
ics = format_ics(days, "is-228")
js  = format_json(days, monday, "is-228")

# List all groups
groups = fetch_groups()
# [{"id": "is-228", "title": "ИС-228"}, ...]
```

### Custom timezone

```python
from datetime import timezone, timedelta
from akademiks import fetch_schedule, format_markdown, week_monday

tz_moscow = timezone(timedelta(hours=3))
monday = week_monday()
days = fetch_schedule(monday, "is-228", tz=tz_moscow)
md = format_markdown(days, monday, "is-228", tz=tz_moscow)
```

## Data structure

`fetch_schedule()` returns a list of day objects:

```json
[
  {
    "start": "2026-04-13T19:00:00.000Z",
    "lessons": [
      {
        "id": "...",
        "index": 1,
        "title": "Математика",
        "start": "2026-04-14T03:30:00.000Z",
        "end":   "2026-04-14T05:00:00.000Z",
        "subgroup": null,
        "Teacher":   {"id": "...", "name": "Иванов И.И."},
        "Classroom": {"id": "...", "name": "305", "address": "ул. Студенческая 3"}
      }
    ]
  }
]
```

## Automating with Task Scheduler (Windows)

Save `examples/weekly_sync.py`, then in PowerShell (as admin):

```powershell
schtasks /Create /F /TN "AkademiksSync" `
  /TR "python C:\path\to\weekly_sync.py" `
  /SC WEEKLY /D MON /ST 07:00
```

## Automating with cron (Linux/macOS)

```cron
0 7 * * 1 /usr/bin/python3 /path/to/weekly_sync.py
```

## Notes

- The Akademiks `schedule.get` and `groups.get` endpoints require **no authentication**.
- Timezone defaults to **UTC+5 (Yekaterinburg)**. Use `--tz-offset` to override for other regions.
- Requires Python **3.10+** (uses `date | None` union syntax).

## License

MIT
