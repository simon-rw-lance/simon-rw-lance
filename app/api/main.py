from fastapi import FastAPI, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Tuple
import os
import pandas as pd

from . import settings
from .auth import auth_route, manager
from .components import components_route


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(auth_route, prefix="/auth")
app.include_router(components_route, prefix="/components")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return settings.templates.TemplateResponse(
        "pages/overview.html", {"request": request}
    )


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return settings.templates.TemplateResponse("pages/login.html", {"request": request})


@app.get("/new_campaign/{name}", response_class=HTMLResponse)
async def new_campaign(request: Request, name: str):
    return settings.templates.TemplateResponse(
        "pages/new_campaign.html", {"request": request, "campaign_name": name}
    )


class Parameterisation(BaseModel):
    inputs: Tuple[List[str], List[float], List[float]]
    outputs: Tuple[List[str], List[float], List[float]]


@app.post("/create_campaign/{name}", response_class=HTMLResponse)
async def create_campaign(name: str, params: Parameterisation, user=Depends(manager)):
    path = os.path.join(settings.CAMPAIGNS_DIR, user["tag"], name + ".csv")
    with open(path, "w") as f:
        f.write(f"{','.join(params.inputs[0])},>,{','.join(params.outputs[0])}\n")
        f.write(
            f"{','.join(str(x) for x in params.inputs[1])},>,{','.join(str(x) for x in params.outputs[1])}\n"
        )
        f.write(
            f"{','.join(str(x) for x in params.inputs[2])},>,{','.join(str(x) for x in params.outputs[2])}\n"
        )

    return "Success"


@app.get("/campaign/{name}", response_class=HTMLResponse)
async def resume_campaign(request: Request, name: str):
    return settings.templates.TemplateResponse(
        "pages/campaign.html", {"request": request, "campaign_name": name}
    )


@app.get("/campaign_data/{name}")
async def load_campaign(name: str, user=Depends(manager)):
    path = os.path.join(settings.CAMPAIGNS_DIR, user["tag"], name + ".csv")
    df = pd.read_csv(path)
    return Response(df.to_json(orient="records"), media_type="application/json")
