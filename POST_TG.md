🌌 **akademiks-urtt** — open-source расписание УРТК

Надоело каждый раз лезть на сайт, чтобы узнать когда пара?
Сделал Python-пакет, который умеет всё что нужно.

**Что умеет:**
→ Скачать расписание любой группы УРТК
→ Экспортировать в `.ics` — открывается в Apple/Google Calendar
→ Сохранить как Markdown — вставляй в Notion, Obsidian, куда угодно
→ Отдать JSON — строй своего бота или приложение

**Установка:**
```
pip install akademiks-urtt
```

**Примеры:**
```
akademiks --group is-228
akademiks --group is-228 --week 2026-04-21 --ics --out ./output
akademiks --groups
```

**Без зависимостей. Только Python 3.10+**

GitHub: github.com/cotafei/akademiks-urtt

#python #уртк #расписание #opensource
