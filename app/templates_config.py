from fastapi.templating import Jinja2Templates
from datetime import datetime
from .schemas import CATEGORIES
import re

templates = Jinja2Templates(directory="app/templates")


def strip_html(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text or '')


# ── Jinja2 globals — available in every template automatically ──
templates.env.globals["strip_html"] = strip_html
templates.env.globals["CATEGORIES"] = CATEGORIES

# now() as a callable so it returns the current time on every request
# Use it in templates as: {{ now().year }} or {{ now().strftime('%Y') }}
templates.env.globals["now"] = datetime.utcnow()
