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
        super(GameWorldTest, self).__init__(methodName)

        self.game_registry = GameRegistry();
        self.handler = GameHandler(self.game_registry);

    #missing game
    #missing player from game

    def test_get_world_with_initialised_data(self):
        game = self.game_registry.create_game(CLIENT_ID, GAME_ID)
        game.world.set_size(5, 5);

        resp = self.handler.get_world(Request(CLIENT_ID, {"game_id": GAME_ID}));

        expectedTiles = [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ];
        self.assertEqual(expectedTiles, resp["tileData"]);


class DeforestTest(unittest.TestCase):
    def __init__(self, methodName):
        super(DeforestTest, self).__init__(methodName)

        self.game_registry = GameRegistry();
        self.handler = GameHandler(self.game_registry);
    
    #missing game
    #missing player from game
    #non int
    #missing data

    def test_deforest_removes_forest_for_that_tile_and_increments_player_wood(self):
        game = self.game_registry.create_game(CLIENT_ID, GAME_ID)
        game.world.set_size(5, 5);

        resp = self.handler.action_deforest(Request(CLIENT_ID, {"game_id": GAME_ID}, {"x": 0, "y": 0}));

        self.assertEqual(resp, {});
        player = game.get_player_for_client_id(CLIENT_ID);
        self.assertEqual(10, player.wood);
        resp = self.handler.get_world(Request(CLIENT_ID, {"game_id": GAME_ID}));
        expectedTiles = [
            [2, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ];
        self.assertEqual(expectedTiles, resp["tileData"]);

class BuildTest(unittest.TestCase):
    def __init__(self, methodName):
        super(BuildTest, self).__init__(methodName)

        self.game_registry = GameRegistry();
        self.handler = GameHandler(self.game_registry);

    #missing game
    #missing player from game
    #invalid building id
    #not a clearing
    #already building there
    #not enough money

    def test_build_removes_clearing_for_that_tile_and_sets_building_and_decrements_player_resource(self):
        game = self.game_registry.create_game(CLIENT_ID, GAME_ID)
        game.world.set_size(5, 5);
        game.world.set_tile_at(0, 0, 2);
        player = game.get_player_for_client_id(CLIENT_ID);
        player.wood = 40;

        resp = self.handler.action_build(Request(CLIENT_ID, {"game_id": GAME_ID}, {"x": 0, "y": 0, "buildingId": 1}));

        self.assertEqual(resp, {});
        player = game.get_player_for_client_id(CLIENT_ID);
        self.assertEqual(20, player.wood);
        resp = self.handler.get_world(Request(CLIENT_ID, {"game_id": GAME_ID}));
        expectedTiles = [
            [0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ];
        self.assertEqual(expectedTiles, resp["tileData"]);


class CreateGameTest(unittest.TestCase):
    def __init__(self, methodName):
        super(CreateGameTest, self).__init__(methodName)

        self.game_registry = GameRegistry();
        self.handler = GameHandler(self.game_registry);

    # invalid map id
    # invalid max players
        
    def test_create_game_adds_game_to_registrty_with_that_id(self):
        game = self.game_registry.create_game(CLIENT_ID, GAME_ID)
        game.world.set_size(5, 5);

        resp = self.handler.create_game(Request(CLIENT_ID, {}, {"mapId": "0", "maxPlayers": "2"}));

        game = self.game_registry.get_game_for_id(resp["game_id"]);
        self.assertNotEqual(None, game);
        player = game.get_player_for_client_id(CLIENT_ID);
        self.assertNotEqual(None, player);
        self.assertEqual(CLIENT_ID, game.host);