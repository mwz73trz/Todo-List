from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import task

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task.router)

@app.get("/")
async def root():
    return {"message": "My Todo List on Fast API!"}