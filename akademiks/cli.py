"""
akademiks-urtt CLI
"""

import argparse
import sys
from datetime import date, timedelta, timezone
from pathlib import Path

from .api import fetch_schedule, fetch_groups
from .formatters import format_markdown, format_ics, format_json
from .utils import week_monday, TZ_EKB


def main():
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="akademiks",
        description="Расписание УРТК — CLI клиент для Akademiks API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  akademiks --group is-228
  akademiks --group is-228 --week 2026-04-14 --ics --out ./output
  akademiks --group is-228 --format json
  akademiks --groups
        """,
    )

    parser.add_argument("--group", "-g", metavar="GROUP_ID", help="ID группы, например: is-228")
    parser.add_argument("--week", "-w", metavar="YYYY-MM-DD", help="Дата любого дня нужной недели (по умолчанию — текущая)")
    parser.add_argument("--format", "-f", choices=["markdown", "ics", "json"], default="markdown", help="Формат вывода (по умолчанию: markdown)")
    parser.add_argument("--out", "-o", metavar="DIR", help="Папка для сохранения файла (по умолчанию: вывод в терминал)")
    parser.add_argument("--ics", action="store_true", help="Также сохранить/вывести .ics (только для --format markdown)")
    parser.add_argument("--tz-offset", type=int, default=5, metavar="HOURS", help="UTC-смещение часового пояса (по умолчанию: 5 для Екатеринбурга)")
    parser.add_argument("--tz-name", default="Asia/Yekaterinburg", metavar="TZ", help="Имя часового пояса для ICS (по умолчанию: Asia/Yekaterinburg)")
    parser.add_argument("--groups", action="store_true", help="Показать все группы УРТК")

    args = parser.parse_args()

    tz = timezone(timedelta(hours=args.tz_offset))

    if args.groups:
        print("Загружаю список групп...")
        groups = fetch_groups()
        print(f"\n{'ID':<25} Название")
        print("-" * 50)
        for g in groups:
            print(f"{g['id']:<25} {g.get('title', '')}")
        print(f"\nВсего групп: {len(groups)}")
        return

    if not args.group:
        parser.error("укажи --group (например: akademiks --group is-228) или --groups для списка групп")

    target = date.fromisoformat(args.week) if args.week else date.today()
    monday = week_monday(target)

    print(f"Загружаю расписание [{args.group}] на неделю с {monday.strftime('%d.%m.%Y')}...")
    days = fetch_schedule(monday, args.group, tz)

    out_dir = Path(args.out) if args.out else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    if args.format == "markdown" or (args.format == "markdown" and args.ics):
        md = format_markdown(days, monday, args.group, tz)
        _output(md, out_dir, f"schedule_{monday}.md")

        if args.ics:
            ics = format_ics(days, args.group, args.tz_name, tz)
            _output(ics, out_dir, f"schedule_{monday}.ics")

    elif args.format == "ics":
        ics = format_ics(days, args.group, args.tz_name, tz)
        _output(ics, out_dir, f"schedule_{monday}.ics")

    elif args.format == "json":
        js = format_json(days, monday, args.group, tz)
        _output(js, out_dir, f"schedule_{monday}.json")


def _output(content: str, out_dir: Path | None, filename: str) -> None:
    if out_dir:
        path = out_dir / filename
        path.write_text(content, encoding="utf-8")
        print(f"  Сохранено: {path}")
    else:
        print("\n" + content)
