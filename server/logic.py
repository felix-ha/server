import json
from datetime import datetime
import time
import logging
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import httpx
import logging
from config import Config
from pymongo import MongoClient


class State(BaseModel):
    update_time: str
    text: str


class Mongo:
    def __init__(self, local=False):
       if local:
            self.client = MongoClient('mongodb://root:example@0.0.0.0:27017/')
       else:
            self.client = MongoClient('mongodb', 27017, username='root', password='example')
       self.db = self.client["database"]
       self.collection = self.db['states']

    def insert(self, state: State):
        self.collection.insert_one(state.model_dump())


MONGO = Mongo()
#MONGO.insert(State(update_time="-", text="asdf"))

def call_llm(prompt: str) -> str:
    answer = "Ups, something went wrong."
    url_server = "https://ollama.api.felix-jobson.net"
    route = "/api/generate"

    # TODO: move model to config
    options = {"temperature": 0.3}
    data = {"model": "phi", "stream": False, "prompt": prompt, "options": options}

    try:
        response = httpx.post(f"{url_server}{route}", json=data, headers={"Content-Type": "application/json"}, timeout=None)
        if response.status_code == 200:
            json_response = response.json()
            answer_raw = json_response['response']
            answer = answer_raw.replace("\n", "").replace("\"", "")
        else:
            time.sleep(30)
            response = httpx.post(f"{url_server}{route}", json=data, headers={"Content-Type": "application/json"}, timeout=None)
            if response.status_code == 200:
                json_response = response.json()
                answer_raw = json_response['response']
                answer = answer_raw.replace("\n", "").replace("\"", "")
            else:
                logging.error(f"Server responded with {response.status_code}")
                answer = response.text
    except:
        logging.exception(f"Server is offline.")

    return answer


def update_state(config: Config) -> None:
    Path(config.resources_path).mkdir(parents=True, exist_ok=True)

    prompt = "Write a headline for a homepage."
    answer = call_llm(prompt)

    state = State(update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  text=answer)

    MONGO.insert(state)

    logging.info(f'written state {state} to mongodb')

    file_name = Path(config.resources_path, config.state_file)

    with open(file_name, 'w') as f:
        f.write(state.model_dump_json())

    logging.info(f"written state to {file_name}")



def get_server_data(config: Config):
    state_file = Path(config.resources_path, config.state_file)

    try:
        with open(state_file, 'r') as f:
            json_data = json.load(f)
    except Exception as e:
        logging.exception(e)
        json_data = {'update_time': datetime.now(), 'text': "failed"}
        
    return json_data


if __name__ == '__main__':
    mongo = Mongo()

    #mongo.collection.drop()

    for document in mongo.collection.find():
        print(document)
