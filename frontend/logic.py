import json
from pathlib import Path
from config import Config
from datetime import datetime
import logging


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
    import os
    os.environ['PATH_RESOURCES'] = r".\\resources"
    os.environ['STATE_FILE'] = "state.json"
    config = Config()
    json_data = get_server_data(config)
    print(json_data)
