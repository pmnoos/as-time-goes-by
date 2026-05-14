from fastapi.templating import Jinja2Templates
from datetime import datetime
from .schemas import CATEGORIES
import re

templates = Jinja2Templates(directory="app/templates")


def strip_html(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text or '')


def reading_time(html_text: str) -> int:
    text = strip_html(html_text or "")
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return minutes


def highlight(text: str, query: str) -> str:
    """Wrap query terms in <mark> tags for search result highlighting."""
    if not query or not text:
        return text
    escaped = re.escape(query.strip())
    highlighted = re.sub(
        f'({escaped})',
        r'<mark class="search-highlight">\1</mark>',
        text,
        flags=re.IGNORECASE
    )
    return highlighted


# ── Jinja2 globals — available in every template automatically ──
templates.env.globals["strip_html"] = strip_html
templates.env.globals["CATEGORIES"] = CATEGORIES
templates.env.globals["now"] = datetime.utcnow()
templates.env.globals["reading_time"] = reading_time

# ── Jinja2 filters ──
templates.env.filters["highlight"] = highlight
