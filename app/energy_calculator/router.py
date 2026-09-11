# This router will handle the energy calculator endpoints

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader
from datetime import datetime
from app.auth.dependencies import get_current_user
import logging
from pathlib import Path

router = APIRouter()

app_root = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(app_root / "templates"))
templates.env.loader = ChoiceLoader([
    FileSystemLoader(str(app_root / "energy_calculator" / "templates")),
    FileSystemLoader(str(app_root / "templates")),
])

logging.warning(f"[DEBUG] Type of templates after creation: {type(templates)}")

@router.get("/energy-calculator", response_class=HTMLResponse)
def energy_calculator(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(
        request,
        "energy_calculator/energy-calculator.html",
        {
            "current_user": current_user,
            "now": datetime.now(),
        }
    )
