from datetime import date, datetime, timedelta, timezone

TZ_EKB = timezone(timedelta(hours=5))

WEEKDAYS_FULL = [
    "Понедельник", "Вторник", "Среда",
    "Четверг", "Пятница", "Суббота", "Воскресенье",
]


def week_monday(for_date: date | None = None) -> date:
    d = for_date or date.today()
    return d - timedelta(days=d.weekday())


def to_utc_iso(d: date, tz: timezone = TZ_EKB) -> str:
    dt = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=tz)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def parse_utc(s: str, tz: timezone = TZ_EKB) -> datetime:
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return dt.astimezone(tz)
