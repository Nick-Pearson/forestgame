import unittest

from forestgame.handlers.game_handler import GameHandler;
from forestgame.handlers.handler_exceptions import BadRequestException;
from forestgame.handlers.handler_exceptions import ResourceNotFoundException;
from forestgame.game_registry import GameRegistry;
from forestgame.request import Request;
from forestgame.data.map_data import Map;

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

    #missing game
    #missing player from game
    #client is none of the players
    #missing data in request
        
    def test_create_game_adds_game_to_registrty_with_that_id(self):
        game = self.game_registry.create_game(CLIENT_ID, GAME_ID)
        game.world.set_size(5, 5);

        resp = self.handler.create_game(Request(CLIENT_ID, {}, {"mapId": "0", "maxPlayers": "2"}));

        game = self.game_registry.get_game_for_id(resp["game_id"]);
        self.assertNotEqual(None, game);
        player = game.get_player_for_client_id(CLIENT_ID);
        self.assertNotEqual(None, player);
        self.assertEqual(CLIENT_ID, game.host);

class GetPlayersTest(unittest.TestCase):
    def __init__(self, methodName):
        super(GetPlayersTest, self).__init__(methodName)

        self.game_registry = GameRegistry();
        self.handler = GameHandler(self.game_registry);
        
    # game not found
    # client not in game

    def test_get_players_returns_players_with_ids_and_colours(self):
        game = self.game_registry.create_game(CLIENT_ID, GAME_ID)
        player = game.get_player_for_client_id(CLIENT_ID)
        player.colour = (255, 0, 0);
        game.world.set_size(5, 5);
        game.add_player("6fb8d67c-fee3-437d-9d08-05c27d8a9d16").colour = (0, 255, 0);
        game.add_player("6fb8d67c-fee3-437d-9d08-05c27d8a9d17").colour = (0, 0, 255);
        game.add_player("6fb8d67c-fee3-437d-9d08-05c27d8a9d18").colour = (255, 255, 0);

        resp = self.handler.get_players(Request(CLIENT_ID, {"game_id": GAME_ID}));

        players = resp["players"];
        self.assertEqual(4, len(players));
        self.assertEqual("0", players[0]["id"]);
        self.assertEqual("#FF0000", players[0]["colour"]);
        self.assertEqual(True, players[0]["me"]);
        self.assertEqual("1", players[1]["id"]);
        self.assertEqual("#00FF00", players[1]["colour"]);
        self.assertEqual(False, players[1]["me"]);
        self.assertEqual("2", players[2]["id"]);
        self.assertEqual("#0000FF", players[2]["colour"]);
        self.assertEqual(False, players[2]["me"]);
        self.assertEqual("3", players[3]["id"]);
        self.assertEqual("#FFFF00", players[3]["colour"]);
        self.assertEqual(False, players[3]["me"]);

class GameDataTest(unittest.TestCase):
    def __init__(self, methodName):
        super(GameDataTest, self).__init__(methodName)

        self.game_registry = GameRegistry();
        self.handler = GameHandler(self.game_registry);

    
    # game not found
    # client not in game

    def test_get_game_data_returns_info(self):
        game = self.game_registry.create_game(CLIENT_ID, GAME_ID);
        mapI = Map("0", "My Map", 10, 10, [(0,0), (1,1), (2,2), (3,3)], {"hill": (0,0)}, []);
        game.init_from_map(mapI, 4);

        resp = self.handler.get_game_data(Request(CLIENT_ID, {"game_id": GAME_ID}));

        self.assertEqual(GAME_ID, resp["gameId"]);
        self.assertEqual(4, resp["maxPlayers"]);
        self.assertEqual(1, resp["numPlayers"]);
        self.assertEqual("0", resp["mapId"]);
        self.assertEqual("King of the Hill", resp["gameModeName"]);