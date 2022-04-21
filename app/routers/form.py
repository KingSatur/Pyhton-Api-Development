
from fastapi import Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
import asyncio

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/form", response_class=HTMLResponse)
async def form_home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@router.post("/create_one", response_class=HTMLResponse)
async def form_home(request: Request, number: int = Form(...)):
    result = number + 2
    response = await httpx.AsyncClient().get('http://localhost:8000/posts/test2')
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result, 'yournum': number})


@router.post("/create_two", response_class=HTMLResponse)
async def form_home(request: Request, number: int = Form(...)):
    result = number + 100
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result, 'yournum': number})
