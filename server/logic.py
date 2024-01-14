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
from email_client import get_email_client
from pymongo import MongoClient
import logging


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

def call_llm(prompt: str, model="phi") -> str:
    answer = ""
    url_server = "https://ollama.api.felix-jobson.net"
    route = "/api/generate"

    options = {"temperature": 5, "seed": int(time.time())}
    data = {"model": model, "stream": False, "prompt": prompt, "options": options}

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

    prompt = "Tell me a joke. Output the only the joke."
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

EMAIL_CLIENT = get_email_client()

def send_mail():
    try:
        logging.info(f'Sending mail')

        prompt = "Tell me a joke. Output the only the joke."
        joke_phi = call_llm(prompt, model="phi")
        joke_mistral = call_llm(prompt, model="mistral:instruct")

        receiver_email = "hauerf98@gmail.com"
        subject = "Update"
        message=f"""
        Joke from phi-2:
        {joke_phi}

        Joke from mistral:
        {joke_mistral}
        """

        EMAIL_CLIENT.send(receiver_email, subject, message)

    except Exception as e:
        logging.exception(f"Sending mail failed: {e}")


if __name__ == '__main__':
    mongo = Mongo()

    #mongo.collection.drop()

    for document in mongo.collection.find():
        print(document)
