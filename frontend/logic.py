import json
from pathlib import Path
from config import Config


def get_server_data(config: Config):
    state_file = Path(config.resources_path, config.state_file)

    with open(state_file, 'r') as f:
        json_data = json.load(f)
    
    return json_data

if __name__ == '__main__':
    import os
    os.environ['PATH_RESOURCES'] = r".\\resources"
    os.environ['STATE_FILE'] = "state.json"
    config = Config()
    json_data = get_server_data(config)
    print(json_data)
