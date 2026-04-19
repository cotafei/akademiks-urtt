# akademiks-urtt

Python-клиент и CLI для получения расписания через **[Akademiks УРТК](https://akademiks.urtt.ru)**.

Работает для **любой группы** Уральского радиотехнического колледжа. Никаких зависимостей — только стандартная библиотека Python.

---

## Для кого и зачем

Сайт akademiks.urtt.ru неудобен: нельзя экспортировать расписание, нет API-документации, интерфейс сделан под мышку. Этот инструмент решает проблему:

- **Студенты** — получают расписание в Markdown, импортируют в Notion/Obsidian или в телефонный календарь через `.ics`
- **Разработчики** — используют как библиотеку в своих ботах, автоматизациях, приложениях
- **Все группы УРТК** — не только ИС-228, работает с любой группой колледжа

---

## Установка

```bash
pip install akademiks-urtt
```

Или из исходников:

```bash
git clone https://github.com/cotafei/akademiks-urtt
cd akademiks-urtt
pip install -e .
```

**Требования:** Python 3.10+, интернет-соединение. Больше ничего.

---

## CLI — быстрый старт

```bash
# Расписание на текущую неделю
akademiks --group is-228

# Конкретная неделя
akademiks --group is-228 --week 2026-04-14

# Сохранить в папку (Markdown + ICS для Apple/Google Calendar)
akademiks --group is-228 --out ./расписание --ics

# Вывод в JSON
akademiks --group is-228 --format json

# Список всех групп УРТК
akademiks --groups
```

### Все параметры

| Флаг | По умолчанию | Описание |
|------|-------------|----------|
| `--group`, `-g` | обязательный | ID группы, например `is-228` |
| `--week`, `-w` | текущая неделя | Любая дата нужной недели (`YYYY-MM-DD`) |
| `--format`, `-f` | `markdown` | Формат вывода: `markdown`, `ics`, `json` |
| `--out`, `-o` | вывод в терминал | Папка для сохранения файлов |
| `--ics` | выключен | Также экспортировать `.ics` при формате `markdown` |
| `--tz-offset` | `5` | Сдвиг UTC в часах (по умолчанию Екатеринбург UTC+5) |
| `--tz-name` | `Asia/Yekaterinburg` | Имя часового пояса для заголовков ICS |
| `--groups` | — | Показать все группы УРТК |

---

## Python API

```python
from datetime import date
from akademiks import fetch_schedule, fetch_groups
from akademiks import format_markdown, format_ics, format_json
from akademiks import week_monday

# Получить расписание
monday = week_monday()                    # понедельник текущей недели
days = fetch_schedule(monday, "is-228")   # список дней

# Форматировать
md  = format_markdown(days, monday, "is-228")
ics = format_ics(days, "is-228")
js  = format_json(days, monday, "is-228")

# Все группы
groups = fetch_groups()
# [{"id": "is-228", "title": "ИС-228"}, ...]
```

### Другой часовой пояс

```python
from datetime import timezone, timedelta
from akademiks import fetch_schedule, format_markdown, week_monday

tz_moscow = timezone(timedelta(hours=3))
monday = week_monday()
days = fetch_schedule(monday, "it-101", tz=tz_moscow)
md = format_markdown(days, monday, "it-101", tz=tz_moscow)
```

---

## Структура данных

`fetch_schedule()` возвращает список объектов-дней:

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

---

## Автосинхронизация

### Windows (Task Scheduler)

Сохрани `examples/weekly_sync.py`, затем в PowerShell (от администратора):

```powershell
schtasks /Create /F /TN "AkademiksSync" `
  /TR "python C:\path\to\weekly_sync.py" `
  /SC WEEKLY /D MON /ST 07:00
```

### Linux / macOS (cron)

```cron
0 7 * * 1 /usr/bin/python3 /path/to/weekly_sync.py
```

---

## Заметки

- Эндпоинты `schedule.get` и `groups.get` работают **без авторизации** — официальный публичный API.
- По умолчанию часовой пояс **UTC+5 (Екатеринбург)**. Для других городов используй `--tz-offset`.
- Требуется Python **3.10+**.

---

## Лицензия

MIT
