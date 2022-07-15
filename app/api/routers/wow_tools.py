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
    from . import raider_calc

    try:
        score, best_key, best_key_lvl = raider_calc.GetScore(region, realm, character)
        best_key_lvl = f"+{int(best_key_lvl)}"
    except:
        score = "Unknown character detected, please check entry fields."
        best_key = "N/A"
        best_key_lvl = " "


    data = {
        "character" : character,
        "realm" : realm,
        "region" : region,
        "score" : score,
        "best_key" : best_key,
        "best_key_level" : best_key_lvl 
        }
    return templates.TemplateResponse("/wow_tools/character.html", {"request" : request, "data" : data})
