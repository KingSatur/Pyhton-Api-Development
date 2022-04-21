from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from . import util

from .routers import post, unsplash, user, auth, vote, form, accordion


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(unsplash.router)
app.include_router(form.router)
app.include_router(accordion.router)


# Tells sqlalchemy run the create scripts for the models to generate all the tables
# now, is not needed because of alembic
# Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    data = util.openfile("home.md")
    return templates.TemplateResponse("page.html",  {"request": request, "data": data})


@app.get("/pages/{page_name}", response_class=HTMLResponse)
async def root(request: Request, page_name: str):
    data = util.openfile("home" if page_name is None else page_name + ".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
