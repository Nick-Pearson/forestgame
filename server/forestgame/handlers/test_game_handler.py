import unittest

from forestgame.handlers.game_handler import GameHandler;
from forestgame.handlers.handler_exceptions import BadRequestException;
from forestgame.handlers.handler_exceptions import ResourceNotFoundException;
from forestgame.game_registry import GameRegistry;
from forestgame.request import Request;

GAME_ID = "9ced424f-91c2-47b2-a8ea-6a4bb38f2d2b";
CLIENT_ID = "6fb8d67c-fee3-437d-9d08-05c27d8a9d15";

class GameWorldTest(unittest.TestCase):
    def __init__(self, methodName):
        super(GameHandler, self).__init__(methodName)

        self.game_registry = GameRegistry();
        self.handler = GameHandler(self.game_registry);

    def test_get_for_non_existant_game_returns_not_found(self):
        with self.assertRaises(ResourceNotFoundException) as context:
            self.handler.get_name(Request(CLIENT_ID, {"game_id": GAME_ID}));

        self.assertEquals("Game not found", context.exception.message)