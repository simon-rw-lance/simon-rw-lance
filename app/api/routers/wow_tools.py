from fastapi import Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/wow_tools", response_class=HTMLResponse)
async def wow_tools(request : Request):
    return templates.TemplateResponse("wow_tools.html", {"request": request})

@router.get("/wow_tools/character")
async def character(request: Request):
    # data = {
    #     "character" : character,
    #     "realm" : realm,
    #     "region" : region
    #     }
    data = "Enter character details"
    return templates.TemplateResponse("/wow_tools/character.html", {"request" : request, "data" : data})

@router.post("/wow_tools/character")
async def character(request: Request, region: str = Form(None), realm: str = Form(None), character: str = Form(None)):
    data = {
        "character" : character,
        "realm" : realm,
        "region" : region
        }
    return templates.TemplateResponse("/wow_tools/character.html", {"request" : request, "data" : data})
