from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(module)s %(levelname)s - %(message)s")
# file_handler = logging.FileHandler("log.txt")
file_handler = logging.StreamHandler()
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ServerStatus(BaseModel):
    status: bool


app = FastAPI()

ROUTE_SERVER_STATUS = "/status"


@app.get(ROUTE_SERVER_STATUS, response_model=ServerStatus)
def server_is_online():
    logger.info("checked server status")
    return ServerStatus(status=True)

app.mount("/", StaticFiles(directory="static", html = True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)