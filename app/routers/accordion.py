
from fastapi import Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/accordion", response_class=HTMLResponse)
async def accordion_home(request: Request):
    result = "Type a number"
    return templates.TemplateResponse("accordion.html", {"request": request, 'result': result})


@router.post("/accordion", response_class=HTMLResponse)
async def post_accordion(request: Request, tag: str = Form(...)):
    return templates.TemplateResponse('accordion.html', context={'request': request, 'tag': tag})
