from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from logic import get_server_data
from config import Config

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
import logging

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    json_data = get_server_data(Config())
    return templates.TemplateResponse("index.html", {"request": request, "json_data": json_data})


if __name__ == "__main__":
    import uvicorn
    import os
    os.environ['PATH_RESOURCES'] = r".\\resources"
    os.environ['STATE_FILE'] = "state.json"
    uvicorn.run(app, host="127.0.0.1", port=8000)
