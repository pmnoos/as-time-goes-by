from fastapi.templating import Jinja2Templates
from datetime import datetime
from .schemas import CATEGORIES
import re

templates = Jinja2Templates(directory="app/templates")

def strip_html(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text or '')

templates.env.globals["strip_html"] = strip_html
templates.env.globals["now"] = datetime.utcnow()
templates.env.globals["CATEGORIES"] = CATEGORIES