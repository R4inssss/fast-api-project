from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os

router = APIRouter()

#@router.get("/", response_class=HTMLResponse)
#async def read_index():
#    with open(os.path.join("app/static", "index.html")) as f:
#        html_content = f.read()
#    return HTMLResponse(content=html_content)
#

def load_html(page):
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "pages",  f"{page}.html"))
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


@router.get("/", response_class=HTMLResponse)
async def read_index():
    return load_html("index")


@router.get("/homelab", response_class=HTMLResponse)
async def projects():
    return load_html("homelab")

@router.get("/comp", response_class=HTMLResponse)
async def projects():
    return load_html("comp")

@router.get("/detect", response_class=HTMLResponse)
async def projects():
    return load_html("detect")

@router.get("/prccdc", response_class=HTMLResponse)
async def projects():
    return load_html("prccdc")

# Testing static file directories
# app.mount("/static", StaticFiles(directory="app/static"), name="static")
# app.mount("/pages", StaticFiles(directory="app/static/pages"), name="pages")
# @app.get("/", response_class=HTMLResponse)
# async def landing():
#     with open("/static/pages/index.html", "r") as f:
#         return f.read()