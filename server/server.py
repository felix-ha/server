from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pymongo import MongoClient

from logic import update_state, get_server_data
from config import Config

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(module)s %(levelname)s - %(message)s")
file_handler = logging.StreamHandler()
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ServerStatus(BaseModel):
    status: bool


try:
    client = MongoClient('mongodb', 27017, username='root', password='example')
    db = client["database"]
    collection = db['states']
except Exception as e:
    logging.exception(f"connection to mongodb failed: {str(e)}")



scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('interval', minutes=2)
async def update_job():
    update_state(Config())
    logger.info('updated state')

@scheduler.scheduled_job('cron', hour=0, minute=0, second=0)
async def cron_log():
    now = datetime.now()
    logger.info(f'CRON JOB at time: {now}')

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

@app.get("api/status", response_model=ServerStatus)
def server_is_online():
    logger.info("checked server status")
    return ServerStatus(status=True)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    json_data = get_server_data(Config())
    return templates.TemplateResponse("index.html", {"request": request, "json_data": json_data})

@app.get("/table", response_class=HTMLResponse)
async def read_item(request: Request):
    try:    
        records = []
        for document in collection.find():
            records.append({"update_time": document["update_time"], "text": document["text"]})
        records = records[::-1]
    except Exception as e:
        logging.info(f"retrieving entries from mongodb failed: {e}")
        records = [{'update_time': datetime.now(), 'text': 'loading failed'}]
    return templates.TemplateResponse("table.html", {"request": request, "records": records})


if __name__ == "__main__":
    import uvicorn
    import os
    os.environ['PATH_RESOURCES'] = r".\\resources"
    os.environ['STATE_FILE'] = "state.json"
    uvicorn.run(app, host="127.0.0.1", port=8000)
