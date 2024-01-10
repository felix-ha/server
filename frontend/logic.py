from datetime import datetime


def get_server_data():
    json_data = {
        "text": str(datetime.now())
    }
    return json_data
