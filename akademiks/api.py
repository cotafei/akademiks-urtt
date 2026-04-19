import json
import urllib.parse
import urllib.request
from datetime import date, timezone

from .utils import to_utc_iso

API_BASE = "https://akademiks.urtt.ru/api/trpc"
_UA = "akademiks-urtt/1.0 (github.com/your-username/akademiks-urtt)"


def _get(url: str, timeout: int = 15) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    raw = urllib.request.urlopen(req, timeout=timeout).read()
    return json.loads(raw.decode("utf-8"))


def fetch_schedule(
    week_start: date,
    group_id: str,
    tz: timezone | None = None,
) -> list[dict]:
    """
    Returns a list of day objects for the given week and group.

    Each day: {"start": ISO8601, "lessons": [{...}]}
    Each lesson fields: id, title, start, end, index, subgroup,
                        Teacher: {id, name}, Classroom: {id, name, address}
    """
    from .utils import TZ_EKB
    _tz = tz or TZ_EKB
    payload = {
        "0": {
            "json": {
                "weekStart": to_utc_iso(week_start, _tz),
                "groupId": group_id,
            },
            "meta": {"values": {"weekStart": ["Date"]}},
        }
    }
    inp = urllib.parse.quote(json.dumps(payload))
    url = f"{API_BASE}/schedule.get?batch=1&input={inp}"
    data = _get(url)
    return data[0]["result"]["data"]["json"]["data"]


def fetch_groups() -> list[dict]:
    """
    Returns all groups from URTK: [{"id": "is-228", "title": "ИС-228"}, ...]
    """
    payload = {"0": {"json": None}}
    inp = urllib.parse.quote(json.dumps(payload))
    url = f"{API_BASE}/groups.get?batch=1&input={inp}"
    data = _get(url)
    return data[0]["result"]["data"]["json"]
