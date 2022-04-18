from fastapi import FastAPI
from pydantic import BaseSettings

from app.database import Base, engine

from .routers import post, user, auth, vote
from .config import Settings


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Tells sqlalchemy run the create scripts for the models to generate all the tables
# now, is not needed because of alembic
# Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Hellow papi"}
