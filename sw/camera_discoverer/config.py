import json


class Config:

    def __init__(self, path: str):
        with open(path) as fd:
            data = json.loads(fd.read())

        self.HTTP_SERVER_PORT = data["HTTP_SERVER_PORT"]
        self.HTTP_SERVER_IP = data["HTTP_SERVER_IP"]


if __name__ == '__main__':
    config = Config("config.json")
    print(config.HTTP_SERVER_PORT)