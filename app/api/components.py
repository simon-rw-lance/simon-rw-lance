from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from pathlib import Path
import os

from . import settings
from .auth import manager


components_route = APIRouter()


@components_route.get("/campaigns", response_class=HTMLResponse)
async def campaigns_list(request: Request, user=Depends(manager)):

    campaign_names = [
        os.path.basename(name).split(".")[0]
        for name in Path(os.path.join(settings.CAMPAIGNS_DIR, user["tag"])).glob(
            "*.csv"
        )
    ]

    return settings.templates.TemplateResponse(
        "components/campaign_list.html",
        {"request": request, "campaign_names": campaign_names},
    )
