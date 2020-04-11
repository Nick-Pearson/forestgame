import uuid

class Client:
    id = ""

    def __init__(self, id):
        self.id = id;

class ClientRegistry:
    def add_player(self):
        return Client(str(uuid.uuid4()));