import os
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import httpx
import logging
from config import Config


class State(BaseModel):
    update_time: str
    text: str


def call_llm(prompt: str) -> str:
    answer = "Ups, something went wrong."
    url_server = "https://ollama.api.felix-jobson.net" 
    route = "/api/generate"

    # TODO: move model to config
    options = {"temperature": 0.7}
    data = {"model": "phi", "stream": False, "prompt": prompt, "options": options}

    try:
        response = httpx.post(f"{url_server}{route}", json=data, headers={"Content-Type": "application/json"}, timeout=None)
        if response.status_code == 200:
            json_response = response.json()
            answer_raw = json_response['response']
            answer = answer_raw.replace("\n", "").replace("\"", "")
    except:
        logging.exception(f"Server is offline.")
    
    return answer


def update_state(config: Config) -> None:
    Path(config.resources_path).mkdir(parents=True, exist_ok=True)

    prompt = "Write a headline for a homepage."
    answer = call_llm(prompt) 

    state = State(update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                  text=answer)

    file_name = Path(config.resources_path, config.state_file) 

    with open(file_name, 'w') as f:
        f.write(state.model_dump_json())

    logging.info(f"updated state: {state} at {file_name}")


if __name__ == '__main__':
    os.environ['PATH_RESOURCES'] = r".\\resources"
    os.environ['STATE_FILE'] = "state.json"
    config = Config()
    update_state(config)
