from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from . import models
from .database import engine
from .routers import post, user, auth, vote, front
from .config import settings
import os
from pathlib import Path


# Debug Code: from .debuglog import Debug_log


# ============== Main Code ==================== #

print(settings.database_username)

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["https://www.r4ins.xyz",
           "https://r4ins.xyz",
           "https://www.r4ins.me",
           "https://r4ins.me"]

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
app.include_router(front.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/message")
def hello():
    return {"message": "Push to prod succsessful"}


# ============== Debug Code ==================== #


# Debug Code
#   if __name__ == "__main__":
#       import uvicorn
#       uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
