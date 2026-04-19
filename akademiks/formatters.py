import json
from datetime import date, datetime, timedelta, timezone

from .utils import TZ_EKB, WEEKDAYS_FULL, parse_utc, week_monday


def format_markdown(
    days: list[dict],
    week_start: date,
    group_id: str,
    tz: timezone = TZ_EKB,
) -> str:
    week_end = week_start + timedelta(days=6)
    lines = [
        f"# Расписание {group_id.upper()}",
        f"**Неделя:** {week_start.strftime('%d.%m')} – {week_end.strftime('%d.%m.%Y')}",
        f"**Источник:** akademiks.urtt.ru",
        "",
    ]

    has_lessons = False
    for day in days:
        lessons = day.get("lessons", [])
        if not lessons:
            continue
        has_lessons = True

        day_dt = parse_utc(day["start"], tz)
        wd = WEEKDAYS_FULL[day_dt.weekday()]
        lines.append(f"## {wd} ({day_dt.strftime('%d.%m')})")
        lines.append("")
        lines.append("| # | Время | Предмет | Преподаватель | Кабинет |")
        lines.append("|---|-------|---------|---------------|---------|")

        for les in sorted(lessons, key=lambda x: x["start"]):
            start = parse_utc(les["start"], tz).strftime("%H:%M")
            end = parse_utc(les["end"], tz).strftime("%H:%M")
            title = les.get("title", "—")
            teacher = les.get("Teacher", {}).get("name", "—")
            room = les.get("Classroom", {}).get("name", "—")
            addr = les.get("Classroom", {}).get("address", "")
            room_full = f"{room} ({addr})" if addr else room
            subgroup = f" [{les['subgroup']}]" if les.get("subgroup") else ""
            idx = les.get("index", "?")
            lines.append(
                f"| {idx} | {start}–{end} | {title}{subgroup} | {teacher} | {room_full} |"
            )

        lines.append("")

    if not has_lessons:
        lines.append("> На этой неделе занятий нет.")
        lines.append("")

    lines.append("---")
    lines.append(
        f"*Сгенерировано: {datetime.now(tz).strftime('%Y-%m-%d %H:%M')}*"
    )
    return "\n".join(lines)


def format_ics(
    days: list[dict],
    group_id: str,
    tz_name: str = "Asia/Yekaterinburg",
    tz: timezone = TZ_EKB,
) -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//akademiks-urtt//Schedule//RU",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{group_id.upper()} Расписание",
        f"X-WR-TIMEZONE:{tz_name}",
    ]

    for day in days:
        for les in day.get("lessons", []):
            start_dt = parse_utc(les["start"], tz)
            end_dt = parse_utc(les["end"], tz)
            title = les.get("title", "Пара")
            teacher = les.get("Teacher", {}).get("name", "")
            room = les.get("Classroom", {}).get("name", "")
            addr = les.get("Classroom", {}).get("address", "")
            subgroup = les.get("subgroup")

            summary = title + (f" [{subgroup}]" if subgroup else "")
            location = f"{room}, {addr}" if addr else room
            description = f"Преподаватель: {teacher}\\nГруппа: {group_id}"

            lines += [
                "BEGIN:VEVENT",
                f"UID:{les['id']}@akademiks.urtt.ru",
                f"DTSTAMP:{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
                f"DTSTART;TZID={tz_name}:{start_dt.strftime('%Y%m%dT%H%M%S')}",
                f"DTEND;TZID={tz_name}:{end_dt.strftime('%Y%m%dT%H%M%S')}",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{description}",
                f"LOCATION:{location}",
                "END:VEVENT",
            ]

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)


def format_json(days: list[dict], week_start: date, group_id: str, tz: timezone = TZ_EKB) -> str:
    result = []
    for day in days:
        lessons = day.get("lessons", [])
        if not lessons:
            continue
        day_dt = parse_utc(day["start"], tz)
        result.append({
            "date": day_dt.strftime("%Y-%m-%d"),
            "weekday": WEEKDAYS_FULL[day_dt.weekday()],
            "lessons": [
                {
                    "index": les.get("index"),
                    "title": les.get("title"),
                    "start": parse_utc(les["start"], tz).strftime("%H:%M"),
                    "end": parse_utc(les["end"], tz).strftime("%H:%M"),
                    "teacher": les.get("Teacher", {}).get("name"),
                    "room": les.get("Classroom", {}).get("name"),
                    "address": les.get("Classroom", {}).get("address"),
                    "subgroup": les.get("subgroup"),
                }
                for les in sorted(lessons, key=lambda x: x["start"])
            ],
        })
    return json.dumps({"group": group_id, "week_start": str(week_start), "days": result}, ensure_ascii=False, indent=2)
