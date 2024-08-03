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
@router.get("/", response_class=HTMLResponse)
async def read_index():
    # Resolve the absolute path to the index.html file
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "index.html"))
    with open(file_path, "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

