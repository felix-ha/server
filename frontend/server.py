from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from logic import get_server_data
from config import Config
from pymongo import MongoClient


try:
    client = MongoClient('mongodb', 27017, username='root', password='example')
    db = client["database"]
    collection = db['states']
except Exception as e:
    logging.exception(f"connection to mongodb failed: {str(e)}")


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
import logging

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
