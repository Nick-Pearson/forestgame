import unittest

from handlers.player_handler import PlayerHandler;
from handlers.handler_exceptions import BadRequestException;
from handlers.handler_exceptions import ResourceNotFoundException;
from game_registry import GameRegistry;
from request import Request;

GAME_ID = "d01823a0-8667-41dc-a63f-0af11564fd87";
CLIENT_ID = "21fd7079-c7d8-48a7-8663-db924724f98e";

class PlayerNameTest(unittest.TestCase):
    def __init__(self, methodName):
        super(PlayerNameTest, self).__init__(methodName)

        self.game_registry = GameRegistry();
        self.handler = PlayerHandler(self.game_registry);

    def test_get_for_non_existant_game_returns_not_found(self):
        with self.assertRaises(ResourceNotFoundException) as context:
            self.handler.get_name(Request(CLIENT_ID, {"game_id": GAME_ID}));

        self.assertEqual("Game not found", context.exception.message)
    
    def test_get_for_existant_game_but_not_this_client_returns_not_found(self):
        game = self.game_registry.create_game(GAME_ID)

        with self.assertRaises(ResourceNotFoundException) as context:
            self.handler.get_name(Request(CLIENT_ID, {"game_id": GAME_ID}));

        self.assertEqual("Game not found", context.exception.message)

    def test_get_returns_player_name(self):
        game = self.game_registry.create_game(GAME_ID)
        game.add_player(CLIENT_ID);

        getResp = self.handler.get_name(Request(CLIENT_ID, {"game_id": GAME_ID}));

        self.assertEqual("Player 0", getResp["name"])
    
    def test_put_for_non_existant_game_returns_not_found(self):
        with self.assertRaises(ResourceNotFoundException) as context:
            self.handler.change_name(Request(CLIENT_ID, {"game_id": GAME_ID}, {"name": "New Name"}));

        self.assertEqual("Game not found", context.exception.message)
    
    def test_put_for_existant_game_but_not_this_client_returns_not_found(self):
        game = self.game_registry.create_game(GAME_ID)

        with self.assertRaises(ResourceNotFoundException) as context:
            self.handler.change_name(Request(CLIENT_ID, {"game_id": GAME_ID}, {"name": "New Name"}));

        self.assertEqual("Game not found", context.exception.message)

    def test_put_with_no_name_raises_bad_request(self):
        with self.assertRaises(BadRequestException) as context:
            self.handler.change_name(Request(CLIENT_ID, {"game_id": GAME_ID}, {}));
        
        self.assertEqual("New name must be provided", context.exception.message)
    
    def test_put_with_too_short_name_raises_bad_request(self):
        with self.assertRaises(BadRequestException) as context:
            self.handler.change_name(Request(CLIENT_ID, {"game_id": GAME_ID}, {"name": "a"}));
        
        self.assertEqual("New name must be at least 2 characters", context.exception.message)
    
    def test_put_with_non_string_name_raises_bad_request(self):
        with self.assertRaises(BadRequestException) as context:
            self.handler.change_name(Request(CLIENT_ID, {"game_id": GAME_ID}, {"name": 1234}));
        
        self.assertEqual("New name must be a string", context.exception.message)

    def test_put_changes_name_and_returns_new_name(self):
        game = self.game_registry.create_game(GAME_ID)
        game.add_player(CLIENT_ID);

        putResp = self.handler.change_name(Request(CLIENT_ID, {"game_id": GAME_ID}, {"name": "New Name"}));

        self.assertEqual("New Name", putResp["name"])
        getResp = self.handler.get_name(Request(CLIENT_ID, {"game_id": GAME_ID}, None));
        self.assertEqual("New Name", getResp["name"])

class PlayerStatsTest(unittest.TestCase):
    def __init__(self, methodName):
        super(PlayerStatsTest, self).__init__(methodName)

        self.game_registry = GameRegistry();
        self.handler = PlayerHandler(self.game_registry);

    def test_get_for_non_existant_game_returns_not_found(self):
        with self.assertRaises(ResourceNotFoundException) as context:
            self.handler.get_player_stats(Request(CLIENT_ID, {"game_id": GAME_ID}));
        
        self.assertEqual("Game not found", context.exception.message)
    
    def test_get_for_existant_game_but_not_this_client_returns_not_found(self):
        game = self.game_registry.create_game(GAME_ID)

        with self.assertRaises(ResourceNotFoundException) as context:
            self.handler.get_player_stats(Request(CLIENT_ID, {"game_id": GAME_ID}));

        self.assertEqual("Game not found", context.exception.message)
    
    def test_get_stats_returns_current_stats(self):
        game = self.game_registry.create_game(GAME_ID)
        player = game.add_player(CLIENT_ID);
        player.population = 10;
        player.wood = 20;
        player.coin = 30;
        player.food = 40;

        getResp = self.handler.get_player_stats(Request(CLIENT_ID, {"game_id": GAME_ID}));

        stats = getResp["stats"];
        self.assertEqual(10, stats["population"]);
        self.assertEqual(20, stats["wood"]);
        self.assertEqual(30, stats["coin"]);
        self.assertEqual(40, stats["food"]);


if __name__ == '__main__':
    unittest.main()