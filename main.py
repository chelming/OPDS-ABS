"""Routes for the OPDS feed"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from opds_feed import OPDSFeed

app = FastAPI()
opds_feed = OPDSFeed()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Base path loading page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/opds/{username}")
async def opds_root(username: str):
    """Returns a list of libraries for a specific user"""
    return await opds_feed.generate_root_feed(username)

@app.get("/opds/{username}/library/{library_id}")
async def opds_nav(username: str, library_id: str):
    """Returns navigation menu for a library"""
    return await opds_feed.generate_nav_feed(username, library_id)

@app.get("/opds/{username}/library/{library_id}/items")
async def opds_library(username: str, library_id: str, sort: str = None):
    """List of books in a specific library for a specific user"""
    return await opds_feed.generate_library_feed(username, library_id, sort)
